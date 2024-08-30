<script setup lang="ts">
import type { SearchResultItem } from "@/arches_lingo/types.ts";

defineProps({
    searchResult: {
        type: Object,
        required: true,
    },
});

const getItemLabel = (item: SearchResultItem): string | undefined =>
    item.labels.find((label) => label.language === "en")?.value;

const getParentLabels = (item: SearchResultItem): string => {
    return item.parents
        .map((parent) => {
            const enLabel = parent.labels.find(
                (label) => label.language === "en-US",
            );
            return enLabel ? enLabel.value : "";
        })
        .join(" > ");
};
</script>

<template>
    <div
        class="search-result"
        :class="{ 'is-even': searchResult.index % 2 === 0 }"
    >
        <i class="pi pi-paperclip" />

        <div style="margin: 0 0.5rem">
            {{ getItemLabel(searchResult.option) }}
        </div>

        <div style="margin: 0 0.5rem">
            {{ getParentLabels(searchResult.option) }}
        </div>
    </div>
</template>

<style scoped>
.search-result {
    height: 100%;
    width: 100%;
    padding: 0.5rem;
    display: flex;
    align-items: center;
    background-color: white;
    border-bottom: 1px solid #ddd;
}

.p-focus > .search-result {
    background-color: #9cc3e4;
}

.is-even {
    background-color: #d3e5f4;
}
</style>
