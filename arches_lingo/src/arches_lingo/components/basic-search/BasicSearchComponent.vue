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
const computedMinHeight = ref("");
const isLoading = ref(false);
const isLoadingAdditionalResults = ref(false);
const searchResults = ref<SearchResultItem[]>([]);
const searchResultsPage = ref(1);
const searchResultsTotalCount = ref(0);
const query = ref("");
const shouldShowClearInputButton = ref(false);

const focusInput = () => {
    if (autoCompleteInstance.value) {
        autoCompleteInstance.value.$el.querySelector("input").focus();
    }
};

const fetchData = async (searchTerm: string, items: number, page: number) => {
    isLoading.value = true;
    shouldShowClearInputButton.value = Boolean(page !== 1);

    try {
        const parsedResponse = await fetchSearchResults(
            searchTerm,
            items,
            page,
        );

        if (query.value) {
            // edge case for if user clears query before fetch completes
            if (page !== 1) {
                searchResults.value = [
                    ...searchResults.value,
                    ...parsedResponse.data,
                ];
            } else {
                searchResults.value = parsedResponse.data;
                searchResultsPage.value = 1;
            }

            searchResultsTotalCount.value = parsedResponse.total_results;
            shouldShowClearInputButton.value = true;
        }
    } catch (error) {
        toast.add({
            severity: ERROR,
            life: DEFAULT_ERROR_TOAST_LIFE,
            summary: $gettext("Failed to fetch data."),
            detail: error instanceof Error ? error.message : undefined,
        });

        searchResults.value = [];
        searchResultsPage.value = 1;
        searchResultsTotalCount.value = 0;
        shouldShowClearInputButton.value = true;
    } finally {
        isLoading.value = false;
        isLoadingAdditionalResults.value = false;
    }
};

const loadAdditionalSearchResults = (event: {
    first: number;
    last: number;
}) => {
    if (
        event.last >= searchResultsPage.value * props.searchResultsPerPage &&
        event.last <= searchResultsTotalCount.value
    ) {
        isLoadingAdditionalResults.value = true;
        searchResultsPage.value += 1;

        fetchData(
            query.value,
            props.searchResultsPerPage,
            searchResultsPage.value,
        );
    }
};

const clearInput = () => {
    query.value = "";
    shouldShowClearInputButton.value = false;
    focusInput();
};

const navigateToReport = () => {};

const keepOverlayVisible = () => {
    if (
        query.value &&
        searchResults.value.length &&
        isLoading.value === isLoadingAdditionalResults.value
    ) {
        nextTick(() => autoCompleteInstance.value?.show());
    }
};

onMounted(focusInput);

/**
 * This isn't fantastic but it's the best way I can find to get around PrimeVue's lack of support for
 * updating the height of a `VirtualScroller` overlay, much less updating the height dynamically.
 */
watch(searchResults, (searchResults) => {
    if (searchResults.length) {
        if (searchResults.length <= 20) {
            const rootFontSize = parseFloat(
                getComputedStyle(document.documentElement).fontSize,
            );
            const itemHeightInRem = props.searchResultItemSize / rootFontSize; // convert to rem based on the root font size

            computedMinHeight.value = `${searchResults.length * itemHeightInRem}rem`;
        } else {
            computedMinHeight.value = "60vh";
        }
    } else {
        computedMinHeight.value = "unset";
    }
});
</script>

<template>
    <div style="width: 100%; font-family: sans-serif">
        <div style="display: flex; align-items: center">
            <i class="pi pi-search search-icon" />

            <AutoComplete
                ref="autoCompleteInstance"
                v-model="query"
                option-label="id"
                :loading="isLoading && !isLoadingAdditionalResults"
                :placeholder="$gettext('Quick Search')"
                :pt="{
                    option: () => ({
                        style: {
                            padding: 0,
                            borderRadius: 0,
                        },
                    }),
                    overlay: () => ({
                        style: {
                            transform: 'translateY(3.8rem)',
                            borderRadius: 0,
                            fontFamily: 'sans-serif',
                            backgroundColor: '#ddd',
                        },
                    }),
                    list: () => ({
                        style: {
                            padding: 0,
                            gap: 0,
                        },
                    }),
                }"
                :suggestions="searchResults"
                :virtual-scroller-options="{
                    itemSize: props.searchResultItemSize,
                    lazy: true,
                    onLazyLoad: loadAdditionalSearchResults,
                    scrollHeight: computedMinHeight,
                    style: { minHeight: computedMinHeight },
                    numToleratedItems: 1,
                }"
                @complete="
                    () => {
                        autoCompleteInstance?.hide();
                        fetchData(query, props.searchResultsPerPage, 1);
                    }
                "
                @option-select="navigateToReport"
                @before-hide="keepOverlayVisible"
                @update:model-value="
                    (value) => {
                        if (!value) {
                            shouldShowClearInputButton = false;
                        }
                    }
                "
            >
                <template #option="slotProps">
                    <SearchResult :search-result="slotProps" />
                </template>
                <template
                    v-if="isLoadingAdditionalResults"
                    #footer
                >
                    <div class="footer">
                        <i
                            class="pi pi-spin pi-spinner p-virtualscroller-loader"
                        />
                    </div>
                </template>
            </AutoComplete>

            <Button
                v-if="shouldShowClearInputButton"
                :aria-label="$gettext('Clear Input')"
                class="p-button-text clear-button"
                icon="pi pi-times"
                @click="clearInput"
            />
        </div>

        <SortAndFilterControls />
    </div>
</template>

<style scoped>
.clear-button {
    background-color: transparent !important;
    position: absolute;
    inset-inline-end: 0.2rem;
    color: var(--p-input-color);
}

.search-icon {
    position: absolute;
    inset-inline-start: 1rem;
    z-index: 1;
    font-weight: bold;
}

.p-autocomplete {
    width: 100%;
}

.footer {
    text-align: center;
    position: absolute;
    bottom: 0;
    inset-inline-end: 0;

    i {
        font-size: 2rem;
        background-color: transparent;
        padding: 1rem;
        height: 4rem;
    }
}

:deep(.p-autocomplete .p-autocomplete-input) {
    width: 100%;
    padding: 1rem 2.5rem;
    border: none;
}
</style>
