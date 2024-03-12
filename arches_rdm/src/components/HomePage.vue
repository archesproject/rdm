<script setup lang="ts">
import { ref } from "vue";

import ProgressSpinner from "primevue/progressspinner";
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";

import ConceptTree from "@/components/ConceptTree.vue";
import DetailPane from "@/components/DetailPane.vue";

import type { TreeNode } from "primevue/tree/Tree";

const selectedNode: Ref<TreeNode> = ref({});
</script>

<template>
    <Splitter>
        <SplitterPanel
            :size="45"
            :min-size="20"
        >
            <Suspense>
                <ConceptTree v-model="selectedNode" />
                <template #fallback>
                    <ProgressSpinner style="display: flex" />
                </template>
            </Suspense>
        </SplitterPanel>
        <SplitterPanel
            :size="55"
            :min-size="20"
        >
            <DetailPane v-if="Object.keys(selectedNode).length" :node="selectedNode" />
        </SplitterPanel>
    </Splitter>
</template>

<style scoped>
.p-splitter {
    border: 0;
    height: 100vh;
}
</style>
