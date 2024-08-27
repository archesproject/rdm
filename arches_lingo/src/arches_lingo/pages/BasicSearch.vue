<script setup lang="ts">
import BasicSearchComponent from "@/arches_lingo/components/basic-search/BasicSearchComponent.vue";
</script>

<template>
    <div style="height: 100%; padding: 8rem 4rem">
        <BasicSearchComponent :search-results-per-page="25" />
    </div>
</template>
