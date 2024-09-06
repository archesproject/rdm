<script setup lang="ts">
import { inject } from "vue";

import { selectedLanguageKey } from "@/arches_references/constants.ts";
import { bestLabel } from "@/arches_lingo/utils.ts";

import type { Language } from "@/arches/types";
import type { Ref } from "vue";
import type { TreeNode } from "primevue/treenode";
import type { Labellable } from "@/arches_lingo/types";

const { node, focusLabel, unfocusLabel } = defineProps<{
    node: TreeNode;
    focusLabel: string;
    unfocusLabel: string;
}>();
const selectedLanguage = inject(selectedLanguageKey) as Ref<Language>;

const filterValue = defineModel<string>("filterValue");
const focusedNode = defineModel<TreeNode | null>("focusedNode");

const rowLabel = (data: Labellable) => {
    if (!data) {
        return "";
    }
    const unstyledLabel = bestLabel(data, selectedLanguage?.value?.code).value;
    if (!filterValue.value) {
        return unstyledLabel;
    }
    const regex = new RegExp(`(${filterValue.value})`, "gi");
    return unstyledLabel.replace(regex, "<b>$1</b>");
};

const iconForFocusToggle = (node: TreeNode) => {
    return focusedNode.value?.data?.id === node.data.id
        ? "fa fa-search-minus"
        : "fa fa-bullseye";
};

const labelForFocusToggle = (node: TreeNode) => {
    return focusedNode.value?.data?.id === node.data.id
        ? unfocusLabel
        : focusLabel;
};

const toggleFocus = (node: TreeNode) => {
    if (focusedNode.value?.data?.id === node.data.id) {
        focusedNode.value = null;
    } else {
        focusedNode.value = node;
    }
};
</script>

<template>
    <!-- eslint-disable vue/no-v-html -->
    <span v-html="rowLabel(node.data)"></span>
    <!-- eslint-enable vue/no-v-html -->
    <i
        v-tooltip="labelForFocusToggle(node)"
        role="button"
        :class="iconForFocusToggle(node)"
        :aria-label="labelForFocusToggle(node)"
        tabindex="0"
        :style="{ alignSelf: 'center', marginLeft: '1rem' }"
        @click="toggleFocus(node)"
        @keyup.enter="toggleFocus(node)"
    ></i>
</template>
