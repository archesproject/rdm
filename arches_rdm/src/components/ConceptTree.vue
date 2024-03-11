<script setup lang="ts">
import { computed, ref } from "vue";

import { useGettext } from "vue3-gettext";

import { useToast } from "primevue/usetoast";
import Tree from "primevue/tree";

import { bestLabel } from "@/utils";

import type { Ref } from "vue";
import type {
    TreeContext,
    TreeExpandedKeys,
    TreeNode,
    TreeSelectionKeys,
} from "primevue/tree/Tree";
import type { Concept, Scheme } from "@/types";

const expandedKeys: Ref<TreeExpandedKeys> = ref({});
const selectionKeys: Ref<TreeSelectionKeys> = ref({});
const filterValue = ref("");
const schemes: Ref<Scheme[]> = ref([]);

const toast = useToast();
const { $gettext } = useGettext();

const lightGray = "#f4f4f4";
const ERROR = "error";
const SCHEME_LABEL = $gettext("Scheme");
const GUIDE_LABEL = $gettext("Guide Item");
const INDEXABLE_LABEL = $gettext("Indexable Item");

import { DJANGO_HOST } from "@/main";

const onFilter = (emitted) => {
    filterValue.value = emitted.value;
};

const highlightedLabel = (text: string) => {
    if (!filterValue.value) {
        return text;
    }
    const regex = new RegExp(`(${filterValue.value})`, "gi");
    return text.replace(regex, "<b>$1</b>");
};

const onNodeExpand = (node: TreeNode) => {
    node.children.forEach((child: TreeNode) => {
        const grandchildren = child.children;
        if ((node.children.length + grandchildren.length) < 7) {
            expandedKeys.value[child.key] = true;
        }
    });
};

function conceptAsNode(concept: Concept): TreeNode {
    return {
        key: concept.id,
        label: bestLabel(concept, 'en').value,
        children: concept.narrower.map(child => conceptAsNode(child)),
        data: concept,
        icon: concept.guide ? "fa fa-folder-open" : "fa fa-hand-pointer-o",
        iconLabel: concept.guide ? GUIDE_LABEL : INDEXABLE_LABEL,
    };
}

function schemeAsNode(scheme: Scheme): TreeNode {
    return {
        key: scheme.id,
        label: bestLabel(scheme, 'en').value,
        children: scheme.top_concepts.map(top => conceptAsNode(top)),
        data: scheme,
        icon: "fa fa-list",
        iconLabel: SCHEME_LABEL,
    };
}

const conceptTree = computed(() => {
    return schemes.value.map((scheme: Scheme) => schemeAsNode(scheme));
});

const fetchSchemes = async () => {
    let errorText;
    const url = new URL("concept_trees/", DJANGO_HOST);
    try {
        const response = await fetch(url, { credentials: "include" });
        if (!response.ok) {
            errorText = response.statusText;
            const body = await response.json();
            errorText = body.message;
            throw new Error();
        } else {
            await response.json().then((data) => {
                schemes.value = data.schemes;
            });
        }
    } catch {
        toast.add({
            severity: ERROR,
            summary: errorText || $gettext("Unable to fetch schemes"),
        });
    }
};

await fetchSchemes();
</script>

<template>
    <Tree
        v-model:selectionKeys="selectionKeys"
        :value="conceptTree"
        :expanded-keys
        :filter="true"
        filter-mode="lenient"
        selection-mode="single"
        :pt="{
            root: { style: { flexGrow: 1 } },
            input: {
                placeholder: $gettext('Find'),
                style: { height: '2rem', fontSize: '14px' },
            },
            container: { style: { fontSize: '14px' } },
            content: ({ context }): { context: TreeContext } => ({
                style: {
                    background: context.selected ? lightGray : '',
                    height: '2rem',
                },
                tabindex: '0',
            }),
            label: { style: { textWrap: 'nowrap' } },
        }"
        @node-expand="onNodeExpand"
        @filter="onFilter"
    >
        <template #default="slotProps">
            <span v-html="highlightedLabel(slotProps.node.label)">
            </span>
        </template>
    </Tree>
</template>
