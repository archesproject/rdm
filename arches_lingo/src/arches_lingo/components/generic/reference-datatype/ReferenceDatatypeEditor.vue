<script setup lang="ts">
import { computed, inject, ref } from "vue";
import Select from "primevue/select";
import MultiSelect from "primevue/multiselect";

import { systemLanguageKey } from "@/arches_lingo/constants.ts";
import { PREF_LABEL } from "@/arches_vue_utils/constants.ts";

import type { ControlledListItem } from "@/arches_lingo/types";
import type { Language } from "@/arches_vue_utils/types.ts";

const systemLanguage = inject(systemLanguageKey) as Language;
const props = withDefaults(
    defineProps<{
        value?: ControlledListItem[];
        options?: ControlledListItem[];
        multiValue?: boolean;
    }>(),
    {
        value: () => [],
        options: () => [],
    },
);

const emit = defineEmits(["update"]);
const uriRef = ref(
    props?.value.length === 1 && !props.multiValue
        ? props?.value[0].uri
        : props?.value.map((item) => item.uri),
);
const val = computed({
    get() {
        return uriRef.value;
    },
    set(newVal) {
        uriRef.value = newVal;
        if (!props.multiValue) {
            const item = props.options?.find((item) => item.uri === newVal);
            emit("update", item ? [item] : []);
        } else {
            const items = props.options?.filter((item) =>
                newVal.includes(item.uri),
            );
            emit("update", items ?? []);
        }
    },
});

const optionLabels = (item: ControlledListItem): string => {
    const preferredLabel =
        item.labels.find(
            (label) =>
                label.language_id === systemLanguage?.code &&
                label.valuetype_id === PREF_LABEL,
        ) || item.labels.find((label) => label.valuetype_id === PREF_LABEL);
    return preferredLabel?.value ?? "";
};
</script>

<template>
    <Select
        v-model="val"
        v-if:="!props.multiValue"
        :show-toggle-all="!!options?.length"
        :options
        :option-label="optionLabels"
        option-value="uri"
        :pt="{
            emptyMessage: { style: { fontFamily: 'sans-serif' } },
            option: { style: { fontFamily: 'sans-serif' } },
        }"
        :placeholder="$gettext('Select References')"
    />
    <MultiSelect
        v-if="props.multiValue"
        v-model="val"
        :show-toggle-all="!!options?.length"
        :options
        :option-label="optionLabels"
        option-value="uri"
        :pt="{
            emptyMessage: { style: { fontFamily: 'sans-serif' } },
            option: { style: { fontFamily: 'sans-serif' } },
        }"
        :placeholder="$gettext('Select References')"
    />
</template>
