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
} from "primevue/tree/Tree";
import type { Concept, Scheme } from "@/types";

const expandedKeys: Ref<TreeExpandedKeys> = ref({});

const toast = useToast();
const { $gettext } = useGettext();

const ERROR = "error";
import { DJANGO_HOST } from "@/main";

const schemes: Ref<Scheme[]> = ref([]);

function conceptAsNode(concept: Concept): TreeNode {
    return {
        key: concept.id,
        label: bestLabel(concept, 'en').value,
        children: concept.narrower.map(child => conceptAsNode(child)),
        data: concept,
    };
}

function schemeAsNode(scheme: Scheme): TreeNode {
    return {
        key: scheme.id,
        label: bestLabel(scheme, 'en').value,
        children: scheme.top_concepts.map(top => conceptAsNode(top)),
        data: scheme,
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
        :value="conceptTree"
        :expanded-keys
        :filter="true"
        filter-mode="lenient"
        selection-mode="single"
        :pt="{
            root: { style: { flexGrow: 1 } },
            input: {
                placeholder: $gettext('Find'),
                style: { height: '3.5rem', fontSize: '14px' },
            },
            container: { style: { fontSize: '14px' } },
            content: ({ context }): { context: TreeContext } => ({
                style: {
                    background: context.selected ? lightGray : '',
                    height: '3.5rem',
                },
                tabindex: '0',
            }),
            label: { style: { textWrap: 'nowrap' } },
        }"
    />
</template>
