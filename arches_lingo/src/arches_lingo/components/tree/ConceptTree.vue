<script setup lang="ts">
import { computed, inject, ref } from "vue";
import { useGettext } from "vue3-gettext";

import { useToast } from "primevue/usetoast";
import Tree from "primevue/tree";

import PresentationControls from "@/arches_references/components/tree/PresentationControls.vue";
import {
    DEFAULT_ERROR_TOAST_LIFE,
    ERROR,
    displayedRowKey,
    selectedLanguageKey,
} from "@/arches_references/constants.ts";
import { fetchConcepts } from "@/arches_lingo/api.ts";
import { bestLabel } from "@/arches_lingo/utils.ts";
import LetterCircle from "arches_lingo/arches_lingo/src/arches_references/components/misc/LetterCircle.vue";

import type { Language } from "@/arches/types";
import type { ComponentPublicInstance, Ref } from "vue";
import type { TreeExpandedKeys, TreeSelectionKeys } from "primevue/tree";
import type { TreeNode } from "primevue/treenode";
import type { RowSetter } from "@/arches_references/types";
import type {
    Concept,
    Labellable,
    NodeAndParentInstruction,
    Scheme,
} from "@/arches_lingo/types";

const toast = useToast();
const { $gettext } = useGettext();

const SCHEME_LABEL = $gettext("Scheme");
const CONCEPT_LABEL = $gettext("Concept");
const FOCUS = $gettext("Focus");
const UNFOCUS = $gettext("Unfocus");

const schemes: Ref<Scheme[]> = ref([]);
const focusedNode: Ref<TreeNode> = ref({ key: "dummy" });
const selectedKeys: Ref<TreeSelectionKeys> = ref({});
const expandedKeys: Ref<TreeExpandedKeys> = ref({});
const filterValue = ref("");
const treeDOMRef: Ref<ComponentPublicInstance | null> = ref(null);
// @ts-expect-error woes with inject
const selectedLanguage = inject(selectedLanguageKey) as Ref<Language>;
const nextFilterChangeNeedsExpandAll = ref(false);
const expandedKeysSnapshotBeforeSearch = ref<TreeExpandedKeys>({});
const rerenderTree = ref(0);
// @ts-expect-error woes with inject
const { setDisplayedRow } = inject(displayedRowKey) as unknown as {
    setDisplayedRow: RowSetter;
};

const rowLabel = (data: Labellable) => {
    if (!data) {
        return "";
    }
    const unstyledLabel = bestLabel(data, selectedLanguage.value.code).value;
    if (!filterValue.value) {
        return unstyledLabel;
    }
    const regex = new RegExp(`(${filterValue.value})`, "gi");
    return unstyledLabel.replace(regex, "<b>$1</b>");
};

const conceptAsNodeAndParentInstruction = (
    concept: Concept,
): NodeAndParentInstruction => {
    return conceptOrSchemeAsNodeAndParentInstruction(concept, concept.narrower);
};
const schemeAsNodeAndParentInstruction = (
    scheme: Scheme,
): NodeAndParentInstruction => {
    return conceptOrSchemeAsNodeAndParentInstruction(
        scheme,
        scheme.top_concepts,
    );
};
const conceptOrSchemeAsNodeAndParentInstruction = (
    labellable: Labellable,
    children: Concept[],
): NodeAndParentInstruction => {
    let childrenAsNodes: TreeNode[];
    const nodesAndInstructions = children.map((child) =>
        conceptAsNodeAndParentInstruction(child),
    );
    const parentOfFocusedNode = nodesAndInstructions.find(
        (obj) => obj.parentShouldHideSiblings,
    );
    if (parentOfFocusedNode) {
        childrenAsNodes = [parentOfFocusedNode.node];
    } else {
        childrenAsNodes = nodesAndInstructions.map((obj) => obj.node);
    }
    const iconLabel = (labellable as Scheme).top_concepts
        ? SCHEME_LABEL
        : CONCEPT_LABEL;
    const node: TreeNode = {
        key: labellable.id,
        label: bestLabel(labellable, selectedLanguage.value.code).value,
        children: childrenAsNodes,
        data: labellable,
        iconLabel,
    };
    let parentShouldHideSiblings = !!parentOfFocusedNode;
    if (!parentShouldHideSiblings) {
        const focalNodeIdx = node.children!.findIndex(
            (child: TreeNode) => child.data.id === focusedNode.value.data?.id,
        );
        if (focalNodeIdx > -1) {
            node.children = [node.children![focalNodeIdx]];
            parentShouldHideSiblings = true;
        }
    }
    return { node, parentShouldHideSiblings };
};

const tree = computed(() => {
    const focalNodeIdx = schemes.value.findIndex(
        (scheme) => scheme.id === focusedNode.value.data?.id,
    );
    if (focalNodeIdx > -1) {
        return [
            schemeAsNodeAndParentInstruction(schemes.value[focalNodeIdx]).node,
        ];
    }
    const nodesAndInstructions = schemes.value.map((scheme: Scheme) =>
        schemeAsNodeAndParentInstruction(scheme),
    );
    const parentOfFocusedNode = nodesAndInstructions.find(
        (obj) => obj.parentShouldHideSiblings,
    );
    if (parentOfFocusedNode) {
        return [parentOfFocusedNode.node];
    }
    return nodesAndInstructions.map((obj) => obj.node);
});

const expandAll = () => {
    for (const node of tree.value) {
        expandNode(node);
    }
    expandedKeys.value = { ...expandedKeys.value };
};

const collapseAll = () => {
    expandedKeys.value = {};
};

const expandNode = (node: TreeNode) => {
    if (node.children && node.children.length) {
        expandedKeys.value[node.key] = true;
        for (const child of node.children) {
            expandNode(child);
        }
    }
};

const iconForFocusToggle = (node: TreeNode) => {
    return focusedNode.value.data?.id === node.data.id
        ? "fa fa-search-minus"
        : "fa fa-bullseye";
};

const labelForFocusToggle = (node: TreeNode) => {
    return focusedNode.value.data?.id === node.data.id ? UNFOCUS : FOCUS;
};

const toggleFocus = (node: TreeNode) => {
    if (focusedNode.value.data?.id === node.data.id) {
        focusedNode.value = { key: "dummy" };
    } else {
        focusedNode.value = node;
    }
};

const expandPathsToFilterResults = (newFilterValue: string) => {
    // https://github.com/primefaces/primevue/issues/3996
    if (filterValue.value && !newFilterValue) {
        expandedKeys.value = { ...expandedKeysSnapshotBeforeSearch.value };
        expandedKeysSnapshotBeforeSearch.value = {};
        // Rerender to avoid error emitted in PrimeVue tree re: aria-selected.
        rerenderTree.value += 1;
    }
    // Expand all on the first interaction with the filter, or if the user
    // has collapsed a node and changes the filter.
    if (
        (!filterValue.value && newFilterValue) ||
        (nextFilterChangeNeedsExpandAll.value &&
            filterValue.value !== newFilterValue)
    ) {
        expandedKeysSnapshotBeforeSearch.value = { ...expandedKeys.value };
        expandAll();
    }
    nextFilterChangeNeedsExpandAll.value = false;
};

const getInputElement = () => {
    if (treeDOMRef.value !== null) {
        return treeDOMRef.value.$el.ownerDocument.querySelector(
            'input[data-pc-name="pcfilter"]',
        ) as HTMLInputElement;
    }
};

const restoreFocusToInput = () => {
    // The current implementation of collapsing all nodes when
    // backspacing out the search value relies on rerendering the
    // <Tree> component. Restore focus to the input element.
    if (rerenderTree.value > 0) {
        const inputEl = getInputElement();
        if (inputEl) {
            inputEl.focus();
        }
    }
};

const snoopOnFilterValue = () => {
    // If we wait to react to the emitted filter event, the templated rows
    // will have already rendered. (<TreeRow> bolds search terms.)
    const inputEl = getInputElement();
    if (inputEl) {
        expandPathsToFilterResults(inputEl.value);
        filterValue.value = inputEl.value;
    }
};

const filterCallbackWrapped = computed(() => {
    // Access some hidden functionality of the PrimeVue <Tree> to make
    // filter lookups lazy, that is, making use of the current state of the
    // label values and the selected language when doing the filtering.
    // "Hidden", because we need to violate the type of filter-by, which
    // should be a string. If we abuse it to be something that returns
    // a 1-element array containing a getter when split() is called on it,
    // that getter can return the best label to filter against.
    return {
        split: () => {
            return [
                (node: TreeNode) => {
                    return bestLabel(node.data, selectedLanguage.value.code)
                        .value;
                },
            ];
        },
    };
});

const updateSelectedAndExpanded = (node: TreeNode) => {
    setDisplayedRow(node.data);
    expandedKeys.value = {
        ...expandedKeys.value,
        [node.key]: true,
    };
};

const initializeTree = async () => {
    /*
    Currently, rather than inspecting the results of the batched
    delete requests, we just refetch everything. This requires being
    a little clever about resorting the ordered response from the API
    to preserve the existing sort (and avoid confusion).
    */
    const priorSortedListIds = tree.value.map((node) => node.key);

    await fetchConcepts()
        .then(({ schemes: fetchedSchemes }: { schemes: Scheme[] }) => {
            schemes.value = fetchedSchemes.sort(
                (a, b) =>
                    priorSortedListIds.indexOf(
                        schemeAsNodeAndParentInstruction(a).node.key,
                    ) -
                    priorSortedListIds.indexOf(
                        schemeAsNodeAndParentInstruction(b).node.key,
                    ),
            );
        })
        .catch((error: Error) => {
            toast.add({
                severity: ERROR,
                life: DEFAULT_ERROR_TOAST_LIFE,
                summary: $gettext("Unable to fetch concepts"),
                detail: error.message,
            });
        });
};

await initializeTree();
</script>

<template>
    <PresentationControls
        :expand-all
        :collapse-all
    />
    <Tree
        v-if="tree"
        ref="treeDOMRef"
        :key="rerenderTree"
        v-model:selection-keys="selectedKeys"
        v-model:expanded-keys="expandedKeys"
        :value="tree"
        :filter="true"
        :filter-by="filterCallbackWrapped as unknown as string"
        filter-mode="lenient"
        :filter-placeholder="$gettext('Find')"
        selection-mode="single"
        :pt="{
            pcFilter: {
                root: {
                    ariaLabel: $gettext('Find'),
                    style: {
                        width: '100%',
                        marginBottom: '1rem',
                        display: 'flex',
                    },
                },
            },
            nodeLabel: {
                style: { textWrap: 'nowrap' },
            },
            hooks: {
                onBeforeUpdate: snoopOnFilterValue,
                onMounted: restoreFocusToInput,
            },
        }"
        @node-collapse="nextFilterChangeNeedsExpandAll = true"
        @node-select="updateSelectedAndExpanded"
    >
        <template #nodeicon="slotProps">
            <LetterCircle :labelled="slotProps.node.data" />
        </template>
        <template #default="slotProps">
            <!-- eslint-disable vue/no-v-html -->
            <span v-html="rowLabel(slotProps.node.data)" />
            <!-- eslint-enable vue/no-v-html -->
            <i
                v-tooltip="labelForFocusToggle(slotProps.node)"
                role="button"
                :class="iconForFocusToggle(slotProps.node)"
                :aria-label="labelForFocusToggle(slotProps.node)"
                tabindex="0"
                :style="{ alignSelf: 'center', marginLeft: '1rem' }"
                @click="toggleFocus(slotProps.node)"
                @keyup.enter="toggleFocus(slotProps.node)"
            />
        </template>
    </Tree>
</template>
