<script setup lang="ts">
import { computed, onMounted, ref, toRef, watch } from "vue";
import MultiSelect from "primevue/multiselect";
import Button from "primevue/button";
import type {
    GraphInfo,
    NewResourceInstance,
    ResourceInstanceReference,
    ResourceInstanceResult,
} from "@/arches_lingo/types";
import { useGettext } from "vue3-gettext";
import { fetchRelatableResources } from "@/arches_lingo/api.ts";
import { UPDATED, CREATE_NEW_RESOURCE } from "@/arches_lingo/constants.ts";

const { $gettext } = useGettext();

const props = defineProps<{
    val?: string[];
    graphSlug: string;
    nodeAlias: string;
    ptAriaLabeledBy?: string;
}>();
const options = ref<ResourceInstanceReference[]>([]);
const newElements = ref<NewResourceInstance[]>([]);

onMounted(async () => {
    console.log(props);
    const resourceData = await fetchRelatableResources(
        props.graphSlug,
        props.nodeAlias,
    );
    options.value = resourceData.data.map(
        (
            resourceRecord: ResourceInstanceResult,
        ): ResourceInstanceReference => ({
            displayValue: resourceRecord.display_value,
            resourceId: resourceRecord.resourceinstanceid,
            ontologyProperty: "",
            inverseOntologyProperty: "",
        }),
    );
    newElements.value = resourceData.graphs.map(
        (graphInfo: GraphInfo): NewResourceInstance => ({
            displayValue: $gettext("Add a new %{graphName}", {
                graphName: graphInfo.name,
            }),
            graphId: graphInfo.graphid,
        }),
    );
});

const emit = defineEmits([UPDATED, CREATE_NEW_RESOURCE]);

const valRef = toRef(props, "val");

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
</script>
<template>
    <MultiSelect
        v-model="primeVuePickerVal"
        :show-toggle-all="!!options?.length"
        :options
        option-label="displayValue"
        option-value="resourceId"
        :pt="{
            emptyMessage: { style: { fontFamily: 'sans-serif' } },
            option: { style: { fontFamily: 'sans-serif' } },
            overlay: { style: { fontFamily: 'sans-serif' } },
        }"
        :placeholder="$gettext('Select Resources')"
        :aria-labelledby="props.ptAriaLabeledBy"
    >
        <template #footer>
            <div
                v-for="element in newElements"
                :key="`new-${element.graphId}`"
            >
                <Button
                    class="relationship-footer-btn"
                    :label="element.displayValue"
                    severity="secondary"
                    variant="text"
                    @click="$emit(CREATE_NEW_RESOURCE, element.graphId)"
                />
            </div>
        </template>
    </MultiSelect>
</template>
<style lang="css" scoped>
.relationship-footer-btn {
    width: 100%;
    border-radius: unset;
}
</style>
