<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import DataTable from "primevue/datatable";
import Column from "primevue/column";

import { VIEW, EDIT, OPEN_EDITOR } from "@/arches_lingo/constants.ts";
import type {
    DataComponentMode,
    SchemeInstance,
} from "@/arches_lingo/types.ts";
import { fetchSchemeLabel } from "@/arches_lingo/api.ts";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";

const schemeInstance = ref<SchemeInstance>();
const { $gettext } = useGettext();
const route = useRoute();

defineProps<{
    mode?: DataComponentMode;
}>();

defineExpose({ save, getSectionValue });

const emits = defineEmits([OPEN_EDITOR]);

onMounted(async () => {
    getSectionValue();
});

async function getSectionValue() {
    const result = await fetchSchemeLabel(route.params.id as string);
    schemeInstance.value = {
        appellative_status: result.appellative_status,
    };

    //schemeAsLabelTable(scheme)
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
        <SchemeReportSection
            :title-text="$gettext('Scheme Labels')"
            @open-editor="emits(OPEN_EDITOR)"
        >
            <DataTable
                :value="schemeInstance?.appellative_status"
                table-style="min-width: 50rem"
            >
                <Column
                    field="appellative_status_ascribed_name_content"
                    header="Label"
                ></Column>
                <Column
                    field="type"
                    header="Label Type"
                ></Column>
                <Column
                    field="language"
                    header="Label Language"
                ></Column>
            </DataTable>
        </SchemeReportSection>
    </div>
    <div v-if="mode === EDIT"><!-- todo for Johnathan-->abc</div>
</template>
