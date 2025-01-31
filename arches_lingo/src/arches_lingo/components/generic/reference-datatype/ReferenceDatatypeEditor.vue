<script setup lang="ts">
import { computed, inject, ref, toRef, watch } from "vue";
import Select from "primevue/select";
import MultiSelect from "primevue/multiselect";

import { systemLanguageKey } from "@/arches_lingo/constants.ts";
import { PREF_LABEL } from "@/arches_vue_utils/constants.ts";

import type { ControlledListItem } from "@/arches_lingo/types";
import type { Language } from "@/arches_vue_utils/types.ts";

const systemLanguage = inject(systemLanguageKey) as Language;
const emit = defineEmits(["update"]);
const props = withDefaults(
    defineProps<{
        value?: ControlledListItem[];
        options?: ControlledListItem[];
        multiValue?: boolean;
        ptAriaLabeledBy?: string;
    }>(),
    {
        value: () => [],
        options: () => [],
    },
);

const modelValue = toRef(props, "value");
const val = computed({
    get() {
        return extractURI(modelValue.value);
    },
    set(newVal) {
        if (!props.multiValue) {
            const foundItem = props.options?.find(
                (item) => item.uri === newVal,
            );
            const item = foundItem ? [foundItem] : [];
            emit("update", item);
        } else {
            const foundItems = props.options?.filter((item) =>
                newVal.includes(item.uri),
            );
            const items = foundItems ?? [];
            emit("update", items);
        }
    },
});

const primeVuePickerVal = ref(val.value);
watch(primeVuePickerVal, (newVal) => {
    val.value = newVal;
});

function extractURI(item: ControlledListItem[]): string | string[] {
    if (item && !props.multiValue) {
        return item[0]?.uri;
    } else if (item && props.multiValue) {
        return item.map((item) => item.uri);
    } else {
        return [];
    }
}

function getOptionLabels(item: ControlledListItem): string {
    const prefLabels = item.labels.filter(
        (label) => label.valuetype_id === PREF_LABEL,
    );
    const optionLabel =
        prefLabels.find(
            (label) => label.language_id === systemLanguage?.code,
        ) || prefLabels[0];
    return optionLabel?.value ?? "";
}
</script>

<template>
    <Select
        v-model="primeVuePickerVal"
        v-if:="!props.multiValue"
        :show-toggle-all="!!options?.length"
        :options
        :option-label="getOptionLabels"
        option-value="uri"
        :pt="{
            emptyMessage: { style: { fontFamily: 'sans-serif' } },
            option: { style: { fontFamily: 'sans-serif' } },
        }"
        :placeholder="$gettext('Select References')"
        :aria-labelledby="props.ptAriaLabeledBy"
    />
    <MultiSelect
        v-if="props.multiValue"
        v-model="primeVuePickerVal"
        :show-toggle-all="!!options?.length"
        :options
        :option-label="getOptionLabels"
        option-value="uri"
        :pt="{
            emptyMessage: { style: { fontFamily: 'sans-serif' } },
            option: { style: { fontFamily: 'sans-serif' } },
        }"
        :placeholder="$gettext('Select References')"
        :aria-labelledby="props.ptAriaLabeledBy"
    />
</template>
