<script setup lang="ts">
import { toRef, watch } from "vue";

import DatePicker from "primevue/datepicker";

const props = defineProps<{
    value: string | undefined;
}>();

const emit = defineEmits(["update"]);

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
        show-icon
        icon-display="input"
        date-format="yy-mm-dd"
        @update:model-value="() => emit('update', modelValue)"
    />
</template>
