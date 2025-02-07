<script setup lang="ts">
import { computed, onMounted, ref, toRef, watch } from "vue";
import MultiSelect from "primevue/multiselect";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import type {
    GraphInfo,
    ResourceInstanceReference,
    ResourceInstanceResult,
} from "@/arches_lingo/types";
import { useGettext } from "vue3-gettext";
import { fetchRelatableResources } from "@/arches_lingo/api.ts";
import {
    UPDATED,
    CREATE_NEW_RESOURCE,
    ERROR,
    DEFAULT_ERROR_TOAST_LIFE,
} from "@/arches_lingo/constants.ts";
import type { VirtualScrollerLazyEvent } from "primevue/virtualscroller";
import { useToast } from "primevue/usetoast";
import NewResourceBuilder from "../NewResourceBuilder.vue";

const showNewResource = ref(false);
const newResourceGraphId = ref<string | null>(null);
const { $gettext } = useGettext();
const toast = useToast();

const {
    val,
    graphSlug,
    nodeAlias,
    ptAriaLabeledBy,
    itemHeight = 38,
    resultsPerPage = 25,
} = defineProps<{
    val?: string[];
    graphSlug: string;
    nodeAlias: string;
    ptAriaLabeledBy?: string;
    itemHeight?: number;
    resultsPerPage?: number;
}>();
const options = ref<ResourceInstanceReference[]>([]);
const newElements = ref<GraphInfo[]>([]);
const isLoading = ref(false);
const isLoadingAdditionalResults = ref(false);
const computedResourceResultsHeight = ref("");
const resourceResultsPage = ref(1);
const resourceResultsTotalCount = ref(resultsPerPage);

watch(options, (resourceResults) => {
    if (resourceResults?.length) {
        const rootFontSize = parseFloat(
            getComputedStyle(document.documentElement).fontSize,
        );
        const itemHeightInRem = itemHeight / rootFontSize; // Convert to rem based on the root font size
        const computedHeightInRem = resourceResults.length * itemHeightInRem;

        const viewHeightInPixels = window.innerHeight * 0.6;
        const viewHeightInRem = viewHeightInPixels / rootFontSize; // Convert 60vh to rem

        if (computedHeightInRem > viewHeightInRem) {
            computedResourceResultsHeight.value = "60vh";
        } else {
            computedResourceResultsHeight.value = `${computedHeightInRem}rem`;
        }
    } else {
        computedResourceResultsHeight.value = "2.25rem";
    }
});

onMounted(() => {
    fetchData(1);
});

const emit = defineEmits([UPDATED, CREATE_NEW_RESOURCE]);

const valRef = toRef(() => val);

const value = computed({
    get() {
        return valRef.value;
    },
    set(value) {
        const selected = options.value.filter((option) =>
            value?.includes(option.resourceId),
        );
        emit(UPDATED, selected);
    },
});

const primeVuePickerVal = ref(value.value);
watch(primeVuePickerVal, (newVal) => {
    value.value = newVal;
});

async function fetchData(page: number) {
    try {
        const resourceData = await fetchRelatableResources(
            graphSlug,
            nodeAlias,
            page,
        );
        const references = resourceData.data.map(
            (
                resourceRecord: ResourceInstanceResult,
            ): ResourceInstanceReference => ({
                displayValue: resourceRecord.display_value,
                resourceId: resourceRecord.resourceinstanceid,
                ontologyProperty: "",
                inverseOntologyProperty: "",
            }),
        );

        if (page === 1) {
            options.value = references;
            newElements.value = resourceData.graphs;
        } else {
            options.value = [...options.value, ...references];
        }

        resourceResultsPage.value = resourceData.current_page;
        resourceResultsTotalCount.value = resourceData.total_results;
    } catch (error) {
        toast.add({
            severity: ERROR,
            life: DEFAULT_ERROR_TOAST_LIFE,
            summary: $gettext("Failed to fetch data."),
            detail: error instanceof Error ? error.message : undefined,
        });

        options.value = [];
        resourceResultsPage.value = 1;
        resourceResultsTotalCount.value = 0;
    } finally {
        isLoading.value = false;
        isLoadingAdditionalResults.value = false;
    }
}

async function onLazyLoadResources(event: VirtualScrollerLazyEvent) {
    if (
        event.last >= resourceResultsPage.value * resultsPerPage &&
        event.last <= resourceResultsTotalCount.value
    ) {
        isLoadingAdditionalResults.value = true;
        const page = resourceResultsPage.value + 1;
        fetchData(page);
    }
}

function createNewResource(slug: string) {
    showNewResource.value = true;
    newResourceGraphId.value = slug;
}

function toggleSelectAll() {
    // check all selected then remove all selected items
    if (this.$refs.selectAll.allSelected) {
        this.selectedItems = [];
        return;
    }

    // else add all items
    this.selectAll = true;
}
</script>
<template>
    <MultiSelect
        v-model="primeVuePickerVal"
        :show-toggle-all="options?.length > 1"
        :options
        option-label="displayValue"
        option-value="resourceId"
        class="resource-instance-relationships-selector"
        :virtual-scroller-options="{
            itemSize: itemHeight,
            lazy: true,
            onLazyLoad: onLazyLoadResources,
            scrollHeight: computedResourceResultsHeight,
            style: {
                minHeight: computedResourceResultsHeight,
                maxHeight: computedResourceResultsHeight,
            },
        }"
        :pt="{
            emptyMessage: { style: { fontFamily: 'sans-serif' } },
            option: { style: { fontFamily: 'sans-serif' } },
            overlay: { style: { fontFamily: 'sans-serif' } },
        }"
        :loading="isLoading && !isLoadingAdditionalResults"
        :placeholder="$gettext('Select Resources')"
        :aria-labelledby="ptAriaLabeledBy"
    >
        <template #header>
            <div
                v-if="options.length > 1"
                class="select-all"
                @click="toggleSelectAll"
            >
                {{ $gettext("Select All Items") }}
            </div>
        </template>
        <template #footer>
            <div
                v-for="element in newElements"
                :key="`new-${element.slug}`"
            >
                <Button
                    class="relationship-footer-btn"
                    :label="
                        $gettext('Create a new %{resourceName}', {
                            resourceName: element.name,
                        })
                    "
                    severity="secondary"
                    variant="text"
                    @click="() => createNewResource(element.slug)"
                />
            </div>
        </template>
    </MultiSelect>
    <Dialog
        v-model:visible="showNewResource"
        :header="$gettext('New Resource')"
        :dismissable-mask="true"
        :close-on-escape="true"
        :modal="true"
        :pt="{
            root: {
                style: {
                    borderRadius: '0',
                    fontFamily: 'sans-serif',
                },
            },
        }"
        ><NewResourceBuilder
            v-if="newResourceGraphId"
            :graph-slug="newResourceGraphId"
    /></Dialog>
</template>
<style lang="css" scoped>
.relationship-footer-btn {
    width: 100%;
    border-radius: unset;
    justify-content: flex-start;
}

.resource-instance-relationships-selector {
    max-width: 12rem;
}

.select-all {
    position: absolute;
    top: 0.6rem;
    left: 2.7rem;
}
</style>
