<script setup lang="ts">
import ProgressSpinner from "primevue/progressspinner";
import SchemeBoxes from "@/arches_lingo/components/schemes/SchemeBoxes.vue";
</script>

<template>
    <Suspense>
        <SchemeBoxes />
        <template #fallback>
            <ProgressSpinner />
        </template>
    </Suspense>
</template>
