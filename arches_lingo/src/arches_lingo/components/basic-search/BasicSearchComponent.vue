<script setup lang="ts">
import { nextTick, ref } from "vue";
import { useGettext } from "vue3-gettext";

import AutoComplete from "primevue/autocomplete";
import Button from "primevue/button";

import SortAndFilterControls from "@/arches_lingo/components/basic-search/SortAndFilterControls.vue";
import SearchResult from "@/arches_lingo/components/basic-search/SearchResult.vue";

import { fetchSearchResults } from "@/arches_lingo/api.ts";
import type { SearchResultItem } from "@/arches_lingo/types.ts";

const { $gettext } = useGettext();

const autoCompleteInstance = ref<InstanceType<typeof AutoComplete> | null>(
    null,
);
const query = ref("");
const queryString = ref("");
const results = ref<SearchResultItem[]>([]);
const isLoading = ref(false);
const shouldShowClearInputButton = ref(false);

const fetchData = async () => {
    isLoading.value = true;
    shouldShowClearInputButton.value = false;

    if (autoCompleteInstance.value) {
        // @ts-expect-error: the `AutoComplete` type has `overlayVisible` mapped as a function. It's not.
        autoCompleteInstance.value.overlayVisible = false;
    }

    try {
        const data = await fetchSearchResults(queryString.value);
        results.value = data as SearchResultItem[];
        shouldShowClearInputButton.value = true;
    } catch (error) {
        console.error("Error fetching data:", error);
    } finally {
        isLoading.value = false;
    }
};

const clearInput = () => {
    query.value = "";
    shouldShowClearInputButton.value = false;
};

const preventSelection = () => {
    query.value = queryString.value;
};

const keepOverlayVisible = () => {
    if (query.value && results.value.length) {
        nextTick(() => autoCompleteInstance.value?.show());
    }
};

const updateQueryString = (value: string | object) => {
    if (!value) {
        shouldShowClearInputButton.value = false;
    }

    if (typeof value === "string") {
        queryString.value = value;
    }
};
</script>

<template>
    <div style="display: flex; align-items: center; position: relative">
        <i class="pi pi-search search-icon" />

        <AutoComplete
            ref="autoCompleteInstance"
            v-model="query"
            :suggestions="results"
            :placeholder="$gettext('Quick Search')"
            :pt="{
                option: () => ({
                    style: {
                        padding: 0,
                    },
                }),
                overlay: () => ({
                    style: {
                        transform: 'translateY(2.3rem)',
                        maxHeight: '60vh',
                    },
                }),
            }"
            @complete="fetchData"
            @option-select="preventSelection"
            @before-hide="keepOverlayVisible"
            @update:model-value="updateQueryString"
        >
            <template #option="slotProps">
                <SearchResult :search-result="slotProps" />
            </template>
        </AutoComplete>

        <Button
            v-if="shouldShowClearInputButton"
            aria-label="Clear Input"
            class="p-button-text clear-button"
            style="background-color: transparent"
            icon="pi pi-times"
            @click="clearInput"
        />
    </div>

    <SortAndFilterControls />
</template>

<style scoped>
.search-icon {
    position: absolute;
    inset-inline-start: 1rem;
    z-index: 1;
    font-weight: bold;
}

.clear-button {
    position: absolute;
    inset-inline-end: 0.2rem;
    color: var(--p-input-color);
}

.p-autocomplete {
    width: 100%;
}

:deep(.p-autocomplete .p-autocomplete-input) {
    width: 100%;
    padding-right: 2.5rem;
    padding-left: 2.5rem;
}
</style>
