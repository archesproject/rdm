<script setup lang="ts">
import { toRef, watch } from "vue";

import DatePicker from "primevue/datepicker";

const props = defineProps<{
    value: string | undefined;
}>();

const modelValue = toRef(props.value);

watch(
    () => props.value,
    (newValue) => {
        modelValue.value = newValue;
    },
);
</script>

<template>
    <DatePicker
        v-model="modelValue"
        disabled
        date-format="yy-mm-dd"
    />
</template>
