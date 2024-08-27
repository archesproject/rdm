<script setup lang="ts">
import { ref } from "vue";
import { useGettext } from "vue3-gettext";

import Checkbox from "primevue/checkbox";
import RadioButton from "primevue/radiobutton";

const { $gettext } = useGettext();

const queryFilters = ref();
const querySortPreference = ref();
</script>

<template>
    <div
        class="p-autocomplete p-inputtext p-component"
        style="
            height: 2rem;
            margin-top: 0.2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        "
    >
        <div style="display: flex">
            <div>Placeholder Sorting:</div>

            <div style="display: flex">
                <div class="query-sort-preference">
                    <RadioButton
                        v-model="querySortPreference"
                        input-id="querySortPreference1"
                        name="querySortPreference"
                        value="Unsorted"
                    />
                    <label for="querySortPreference1">{{
                        $gettext("Unsorted")
                    }}</label>
                </div>
                <div class="query-sort-preference">
                    <RadioButton
                        v-model="querySortPreference"
                        input-id="querySortPreference2"
                        name="querySortPreference"
                        value="A to Z"
                    />
                    <label for="querySortPreference2">{{
                        $gettext("A to Z")
                    }}</label>
                </div>
                <div class="query-sort-preference">
                    <RadioButton
                        v-model="querySortPreference"
                        input-id="querySortPreference3"
                        name="querySortPreference"
                        value="Z to A"
                    />
                    <label for="querySortPreference3">{{
                        $gettext("Z to A")
                    }}</label>
                </div>
            </div>
        </div>
        <div style="display: flex">
            <div>Placeholder filters:</div>

            <div style="display: flex">
                <div class="query-filter">
                    <Checkbox
                        v-model="queryFilters"
                        input-id="queryFilter1"
                        name="queryFilters"
                        value="Concepts"
                    />
                    <label for="queryFilter1">{{ $gettext("Concepts") }}</label>
                </div>
                <div class="query-filter">
                    <Checkbox
                        v-model="queryFilters"
                        input-id="queryFilter2"
                        name="queryFilters"
                        value="Places"
                    />
                    <label for="queryFilter2">{{ $gettext("Places") }}</label>
                </div>
                <div class="query-filter">
                    <Checkbox
                        v-model="queryFilters"
                        input-id="queryFilter3"
                        name="queryFilters"
                        value="People"
                    />
                    <label for="queryFilter3">{{ $gettext("People") }}</label>
                </div>
                <div class="query-filter">
                    <Checkbox
                        v-model="queryFilters"
                        input-id="queryFilter4"
                        name="queryFilters"
                        value="Groups"
                    />
                    <label for="queryFilter4">{{ $gettext("Groups") }}</label>
                </div>
                <div class="query-filter">
                    <Checkbox
                        v-model="queryFilters"
                        input-id="queryFilter4"
                        name="queryFilters"
                        value="Periods"
                    />
                    <label for="queryFilter4">{{ $gettext("Periods") }}</label>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.query-sort-preference,
.query-filter {
    margin: 0 0.5rem;
}

.query-sort-preference > :nth-child(2),
.query-filter > :nth-child(2) {
    margin: 0 0.25rem;
    cursor: pointer;
}
</style>
