<script setup lang="ts">
import { ref, watch } from "vue";
import InputText from "primevue/inputtext";

const props = defineProps<{ value: string }>();
const updateableValue = ref<string>(props.value as string);
const emit = defineEmits(["update"]);
watch(props, (newValue) => {
    updateableValue.value = newValue.value;
});
watch(updateableValue, (newValue) => {
    emit("update", newValue);
});
</script>
<template>
    <div>
        <InputText
            v-model="updateableValue"
            type="text"
        />
    </div>
</template>
