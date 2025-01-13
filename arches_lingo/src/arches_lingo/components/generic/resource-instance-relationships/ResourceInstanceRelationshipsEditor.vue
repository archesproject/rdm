<script setup lang="ts">
import { computed, toRef } from "vue";
import MultiSelect from "primevue/multiselect";
import type { ResourceInstanceReference } from "@/arches_lingo/types";
import { useGettext } from "vue3-gettext";

const { $gettext } = useGettext();

const props = withDefaults(
    defineProps<{
        val?: string[];
        options?: ResourceInstanceReference[];
        ptAriaLabeledBy?: string;
    }>(),
    {
        options: () => [],
    },
);

const emit = defineEmits(["update"]);

const valRef = toRef(props, "val");

const value = computed({
    get() {
        return valRef.value;
    },
    set(value) {
        emit("update", value);
    },
});
</script>
<template>
    <MultiSelect
        v-model="value"
        :show-toggle-all="!!options?.length"
        :options
        option-label="display_value"
        option-value="resourceId"
        :pt="{
            emptyMessage: { style: { fontFamily: 'sans-serif' } },
            option: { style: { fontFamily: 'sans-serif' } },
        }"
        :placeholder="$gettext('Select Resources')"
        :aria-labelledby="props.ptAriaLabeledBy"
    />
</template>
