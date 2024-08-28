<script setup lang="ts">
import { nextTick, ref, watch, onMounted } from "vue";
import { useGettext } from "vue3-gettext";

import AutoComplete from "primevue/autocomplete";
import Button from "primevue/button";

import { useToast } from "primevue/usetoast";

import SortAndFilterControls from "@/arches_lingo/components/basic-search/SortAndFilterControls.vue";
import SearchResult from "@/arches_lingo/components/basic-search/SearchResult.vue";
import SearchResultsFooter from "@/arches_lingo/components/basic-search/SearchResultsFooter.vue";

import { fetchSearchResults } from "@/arches_lingo/api.ts";
import { DEFAULT_ERROR_TOAST_LIFE, ERROR } from "@/arches_lingo/constants.ts";

import type { SearchResultItem } from "@/arches_lingo/types.ts";

const { $gettext } = useGettext();
const toast = useToast();

defineProps({
    searchResultsPerPage: {
        type: Number,
        required: true,
    },
});

const autoCompleteInstance = ref<InstanceType<typeof AutoComplete> | null>(
    null,
);
const query = ref("");
const searchTerm = ref("");
const results = ref<SearchResultItem[]>([]);
const totalSearchResultsCount = ref(0);
const isLoading = ref(false);
const shouldShowClearInputButton = ref(false);

watch(searchTerm, () => {
    if (autoCompleteInstance.value) {
        // @ts-expect-error: the `AutoComplete` type has `overlayVisible` mapped as a function. It's not.
        autoCompleteInstance.value.overlayVisible = false;
    }
});

const fetchData = async (searchTerm: string, page: number = 1) => {
    isLoading.value = true;
    shouldShowClearInputButton.value = false;

    try {
        const parsedResponse = await fetchSearchResults(searchTerm, page);

        results.value = parsedResponse.data as SearchResultItem[];
        totalSearchResultsCount.value = parsedResponse.total_results;
        shouldShowClearInputButton.value = true;
    } catch (error) {
        toast.add({
            severity: ERROR,
            life: DEFAULT_ERROR_TOAST_LIFE,
            summary: $gettext("Failed to fetch data."),
            detail: error instanceof Error ? error.message : undefined,
        });
    } finally {
        isLoading.value = false;
    }
};

const clearInput = () => {
    query.value = "";
    shouldShowClearInputButton.value = false;
};

const preventSelection = () => {
    query.value = searchTerm.value;
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
        searchTerm.value = value;
    }
};

onMounted(() => {
    if (autoCompleteInstance.value) {
        // focus input on component load
        autoCompleteInstance.value.$el.querySelector("input").focus();
    }
});
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
                        transform: 'translateY(3.5rem)',
                        maxHeight: '60vh',
                        borderRadius: 0,
                    },
                }),
            }"
            @complete="() => fetchData(searchTerm)"
            @option-select="preventSelection"
            @before-hide="keepOverlayVisible"
            @update:model-value="updateQueryString"
        >
            <template #option="slotProps">
                <SearchResult :search-result="slotProps" />
            </template>
            <template #footer>
                <!-- currently not WCAG 2.0 compliant. See https://github.com/primefaces/primevue/issues/6304 -->
                <SearchResultsFooter
                    v-if="shouldShowClearInputButton"
                    tabindex="0"
                    :search-results-per-page="searchResultsPerPage"
                    :total-search-results-count="totalSearchResultsCount"
                    @page-change="
                        (event) => fetchData(searchTerm, event.page + 1)
                    "
                />
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
    padding: 1rem 2.5rem;
    border: none;
}
</style>
