<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
import { ref } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
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
</script>

<template>
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
</template>
