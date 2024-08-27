<script setup lang="ts">
import { ref } from "vue";

import Checkbox from 'primevue/checkbox';
import RadioButton from 'primevue/radiobutton';

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
        "
    >
        <div style="display: flex;">
            <div>
                Placeholder Sorting:
            </div>

            <div style="display: flex;">
                <div>
                    <RadioButton v-model="querySortPreference" inputId="querySortPreference1" name="querySortPreference" value="Unsorted" />
                    <label for="querySortPreference1">Unsorted</label>
                </div>
                <div>
                    <RadioButton v-model="querySortPreference" inputId="querySortPreference2" name="querySortPreference" value="A to Z" />
                    <label for="querySortPreference2">A to Z</label>
                </div>
                <div>
                    <RadioButton v-model="querySortPreference" inputId="querySortPreference3" name="querySortPreference" value="Z to A" />
                    <label for="querySortPreference3">Z to A</label>
                </div>
            </div>
        </div>
        <div style="display: flex;">
            <div>
                Placeholder filters:
            </div>
    
            <div style="display: flex;">
                <div>
                    <Checkbox v-model="queryFilters" inputId="queryFilter1" name="queryFilters" value="Concepts" />
                    <label for="queryFilter1"> Concepts </label>
                </div>
                <div>
                    <Checkbox v-model="queryFilters" inputId="queryFilter2" name="queryFilters" value="Places" />
                    <label for="queryFilter2"> Places </label>
                </div>
                <div>
                    <Checkbox v-model="queryFilters" inputId="queryFilter3" name="queryFilters" value="People" />
                    <label for="queryFilter3"> People </label>
                </div>
                <div>
                    <Checkbox v-model="queryFilters" inputId="queryFilter4" name="queryFilters" value="Groups" />
                    <label for="queryFilter4"> Groups </label>
                </div>
                <div>
                    <Checkbox v-model="queryFilters" inputId="queryFilter4" name="queryFilters" value="Periods" />
                    <label for="queryFilter4"> Periods </label>
                </div>
            </div>
        </div>
    </div>
</template>
