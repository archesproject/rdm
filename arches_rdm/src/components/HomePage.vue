<script setup lang="ts">
import ProgressSpinner from "primevue/progressspinner";

import ConceptTree from "@/components/ConceptTree.vue";
</script>

<template>
    <Suspense>
        <ConceptTree />
        <template #fallback>
            <ProgressSpinner style="display: flex" />
        </template>
    </Suspense>
</template>
