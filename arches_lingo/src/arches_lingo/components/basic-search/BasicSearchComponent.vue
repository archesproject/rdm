<script setup lang="ts">
import { nextTick, ref, watch, onMounted } from "vue";
import { useGettext } from "vue3-gettext";

import AutoComplete from "primevue/autocomplete";
import Button from "primevue/button";

import { useToast } from "primevue/usetoast";

import SortAndFilterControls from "@/arches_lingo/components/basic-search/SortAndFilterControls.vue";
import SearchResult from "@/arches_lingo/components/basic-search/SearchResult.vue";

import { fetchSearchResults } from "@/arches_lingo/api.ts";
import { DEFAULT_ERROR_TOAST_LIFE, ERROR } from "@/arches_lingo/constants.ts";

import type { SearchResultItem } from "@/arches_lingo/types.ts";

const { $gettext } = useGettext();
const toast = useToast();

const props = defineProps({
    searchResultsPerPage: {
        type: Number,
        required: true,
    },
    searchResultItemSize: {
        type: Number,
        required: true,
    },
});

const autoCompleteInstance = ref<InstanceType<typeof AutoComplete> | null>(
    null,
);
const query = ref("");
const results = ref<SearchResultItem[]>([]);
const totalSearchResultsCount = ref(0);
const isLoading = ref(false);
const isLoadingAdditionalResults = ref(false);
const shouldShowClearInputButton = ref(false);
const searchResultsPage = ref(1);

const searchTerm = ref("");
watch(searchTerm, () => {
    if (autoCompleteInstance.value) {
        // @ts-expect-error: the `AutoComplete` type has `overlayVisible` mapped as a function. It's not.
        autoCompleteInstance.value.overlayVisible = false;
    }
});

/**
 * This isn't fantastic but it's the best way I can find to get around PrimeVue's lack of support for
 * updating the height of a `VirtualScroller` overlay, much less updating the height dynamically.
 */
const computedMinHeight = ref("");
watch(results, (results) => {
    if (results.length) {
        if (results.length <= 20) {
            const rootFontSize = parseFloat(
                getComputedStyle(document.documentElement).fontSize,
            );
            const itemHeightInRem = props.searchResultItemSize / rootFontSize; // convert to rem based on the root font size

            computedMinHeight.value = `${results.length * itemHeightInRem}rem`;
        } else {
            computedMinHeight.value = "60vh";
        }
    }
});

onMounted(() => {
    if (autoCompleteInstance.value) {
        // focus input on component load
        autoCompleteInstance.value.$el.querySelector("input").focus();
    }
});

const fetchData = async (
    searchTerm: string,
    items: number,
    page: number = 1,
) => {
    isLoading.value = true;
    shouldShowClearInputButton.value = false;

    try {
        const parsedResponse = await fetchSearchResults(
            searchTerm,
            items,
            page,
        );

        results.value = [...results.value, ...parsedResponse.data];
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
        isLoadingAdditionalResults.value = false;
    }
};

const clearResultsAndFetchData = () => {
    results.value = [];
    searchResultsPage.value = 1;

    fetchData(searchTerm.value, props.searchResultsPerPage);
};

const loadAdditionalSearchResults = (event: {
    first: number;
    last: number;
}) => {
    if (
        event.last >= searchResultsPage.value * props.searchResultsPerPage &&
        event.last <= totalSearchResultsCount.value
    ) {
        isLoadingAdditionalResults.value = true;
        searchResultsPage.value += 1;

        fetchData(
            searchTerm.value,
            props.searchResultsPerPage,
            searchResultsPage.value,
        );
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
</script>

<template>
    <div style="width: 100%">
        <div style="display: flex; align-items: center; position: relative">
            <i class="pi pi-search search-icon" />

            <AutoComplete
                ref="autoCompleteInstance"
                v-model="query"
                :loading="isLoading"
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
                        },
                    }),
                }"
                :suggestions="results"
                :virtual-scroller-options="{
                    itemSize: props.searchResultItemSize,
                    lazy: true,
                    loading: isLoading && !isLoadingAdditionalResults,
                    onLazyLoad: loadAdditionalSearchResults,
                    scrollHeight: computedMinHeight,
                    showLoader: true,
                    style: { minHeight: computedMinHeight },
                }"
                @complete="clearResultsAndFetchData"
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
                class="p-button-text"
                icon="pi pi-times"
                style="
                    background-color: transparent;
                    position: absolute;
                    inset-inline-end: 0.2rem;
                    color: var(--p-input-color);
                "
                @click="clearInput"
            />
        </div>

        <SortAndFilterControls />
    </div>
</template>

<style scoped>
.search-icon {
    position: absolute;
    inset-inline-start: 1rem;
    z-index: 1;
    font-weight: bold;
}

.clear-button {
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
