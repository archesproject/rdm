<script setup lang="ts">
import { toRef, watch } from "vue";

import DatePicker from "primevue/datepicker";

const props = defineProps<{
    value: string | undefined;
    dateFormat: string;
}>();

const emit = defineEmits(["update"]);

const modelValue = toRef(props.value);

watch(
    () => props.value,
    (newValue) => {
        modelValue.value = newValue;
    },
);

// Datepicker returns date object, which needs to be parsed to post back
// https://github.com/primefaces/primevue/issues/6278
function parseDate(date: unknown): string | null {
    if (date) {
        return new Date(date as string).toISOString().split("T")[0];
    }
    return null;
}
</script>

<template>
    <DatePicker
        v-model="modelValue"
        icon-display="input"
        :date-format="dateFormat"
        show-icon
        @update:model-value="() => emit('update', parseDate(modelValue))"
    />
</template>
