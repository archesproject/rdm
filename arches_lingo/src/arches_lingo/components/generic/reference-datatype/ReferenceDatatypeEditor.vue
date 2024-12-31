<script setup lang="ts">
import { computed, inject, toRef } from "vue";
import Select from "primevue/select";

import { systemLanguageKey } from "@/arches_lingo/constants.ts";
import { PREF_LABEL } from "@/arches_vue_utils/constants.ts";

import type { ControlledListItem } from "@/arches_lingo/types";
import type { Language } from "@/arches_vue_utils/types.ts";

const systemLanguage = inject(systemLanguageKey) as Language;
const props = withDefaults(
    defineProps<{
        value?: ControlledListItem[];
        options?: ControlledListItem[];
    }>(),
    {
        value: () => [],
        options: () => [],
    },
);

const emit = defineEmits(["update"]);
const valRef = toRef(props?.value?.[0]?.uri); // use uri as value
const val = computed({
    get() {
        return valRef.value; // unwrap array n=1
    },
    set(value) {
        // const item = props.options?.find((item) => item.uri === value);
        console.log(value);
        // emit("update", [item]); // rewrap array n=1
        emit("update", value);
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
