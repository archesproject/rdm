<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
import { ref } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import { VIEW, EDIT } from "@/arches_lingo/constants.ts";
import type { DataComponentMode } from "@/arches_lingo/types";

//todo: replace dummy data with actual data
const labels = ref([
    {
        code: "1",
        name: "label 1",
        category: "category 1",
        quantity: "1",
    },
    {
        code: "2",
        name: "label 2",
        category: "category 2",
        quantity: "2",
    },
    {
        code: "3",
        name: "label 3",
        category: "category 3",
        quantity: "3",
    },
]);
const { $gettext } = useGettext();

defineProps<{
    mode?: DataComponentMode;
}>();

defineExpose({ save, getSectionValue });

async function getSectionValue() {
    // todo: this function is for both of us, I'll implement it tomorrow (you should be able to work on the UI for the form and widgets with dummy data for now).
    // This is the current value of the label nodegroup that will be passed
    // via prop to both components.  Note - per ticket #146 I will probably be genericizing the label viewer component for use by other nodegroups.
    // you will likely need to do the same.    You will need to emit an update event from your component(s) and have a ref to that here, then actually
    // save that value with the save function below.
}

async function save() {
    // todo for Johnathan.  This function will save the values of the form back to arches.
}

// async function update() {
//     // todo for Johnathan.  This function will handle the update emit when the user changes values in your form - you store those values in this section.
// }
</script>

<template>
    <div v-if="!mode || mode === VIEW">
        <SchemeReportSection :title-text="$gettext('Scheme Labels')">
            <DataTable
                :value="labels"
                table-style="min-width: 50rem"
            >
                <Column
                    field="code"
                    header="Code"
                ></Column>
                <Column
                    field="name"
                    header="Name"
                ></Column>
                <Column
                    field="category"
                    header="Category"
                ></Column>
                <Column
                    field="quantity"
                    header="Quantity"
                ></Column>
            </DataTable>
        </SchemeReportSection>
    </div>
    <div v-if="mode === EDIT"><!-- todo for Johnathan-->abc</div>
</template>
