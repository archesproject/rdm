<script setup lang="ts">
import { ref } from "vue";
import { useGettext } from "vue3-gettext";

import Checkbox from "primevue/checkbox";
import RadioButton from "primevue/radiobutton";

const { $gettext } = useGettext();

const filters = [
    { value: "Concepts", label: $gettext("Concepts") },
    { value: "Places", label: $gettext("Places") },
    { value: "People", label: $gettext("People") },
    { value: "Groups", label: $gettext("Groups") },
    { value: "Periods", label: $gettext("Periods") },
];
const queryFilters = ref([]);

const sortOptions = [
    { value: "Unsorted", label: $gettext("Unsorted") },
    { value: "A to Z", label: $gettext("A to Z") },
    { value: "Z to A", label: $gettext("Z to A") },
];
const querySortPreference = ref();
</script>

<template>
    <div
        style="
            display: flex;
            justify-content: space-between;
            padding: 1.2rem;
            background-color: #ebeef0;
            border-top: 1px solid #ddd;
        "
    >
        <div style="display: flex; align-items: center">
            <div>Placeholder Sorting:</div>

            <div
                v-for="(sortOption, index) in sortOptions"
                :key="index"
                class="query-sort-preference"
            >
                <RadioButton
                    v-model="querySortPreference"
                    :input-id="`querySortPreference${index + 1}`"
                    :name="`querySortPreference${index + 1}`"
                    :value="sortOption.value"
                />
                <label :for="`querySortPreference${index + 1}`">{{
                    sortOption.label
                }}</label>
            </div>
        </div>

        <div style="display: flex; align-items: center">
            <div>Placeholder Include:</div>

            <div
                v-for="(filter, index) in filters"
                :key="index"
                class="query-filter"
            >
                <Checkbox
                    v-model="queryFilters"
                    :input-id="`queryFilter${index + 1}`"
                    :name="`queryFilter${index + 1}`"
                    :value="filter.value"
                />
                <label :for="`queryFilter${index + 1}`">{{
                    filter.label
                }}</label>
            </div>
        </div>
    </div>
</template>

<style scoped>
.query-sort-preference,
.query-filter {
    margin: 0 0.5rem;
    display: flex;
    align-items: center;

    label {
        margin: 0 0.25rem;
        cursor: pointer;
    }
}

:deep(.p-radiobutton-box),
:deep(.p-checkbox-box) {
    background-color: #ebeef0;
    border: 1px solid;
}
</style>
