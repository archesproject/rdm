<script setup lang="ts">
import { inject } from "vue";
import { useGettext } from "vue3-gettext";

import Button from "primevue/button";

import MetaStringViewer from "@/arches_lingo/components/generic/MetaStringViewer.vue";

import NonLocalizedStringWidget from "@/arches_component_lab/widgets/NonLocalizedStringWidget/NonLocalizedStringWidget.vue";
import ReferenceSelectWidget from "@/arches_controlled_lists/widgets/ReferenceSelectWidget/ReferenceSelectWidget.vue";
import ResourceInstanceMultiSelectWidget from "@/arches_component_lab/widgets/ResourceInstanceMultiSelectWidget/ResourceInstanceMultiSelectWidget.vue";

import { VIEW } from "@/arches_lingo/constants.ts";

import type { MetaStringText, SchemeStatement } from "@/arches_lingo/types.ts";

const props = defineProps<{
    schemeNotes: SchemeStatement[];
}>();

// need NodeGroup info here ( cardinality ) for proper button text

const { $gettext } = useGettext();

const openEditor = inject<(componentName: string) => void>("openEditor");

const metaStringLabel: MetaStringText = {
    deleteConfirm: $gettext("Are you sure you want to delete this note?"),
    language: $gettext("Note Language"),
    name: $gettext("Note Name"),
    type: $gettext("Note Type"),
    noRecords: $gettext("No scheme notes were found."),
};
</script>

<template>
    <div
        style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 0.125rem solid var(--p-menubar-border-color);
        "
    >
        <h3>{{ $gettext("Scheme Note") }}</h3>

        <div>
            <Button
                :label="$gettext('Add New Scheme Note')"
                @click="openEditor!('SchemeNote')"
            ></Button>
        </div>
    </div>

    <MetaStringViewer
        :meta-strings="props.schemeNotes"
        :meta-string-text="metaStringLabel"
        component-name="SchemeNote"
        graph-slug="scheme"
        node-alias="appellative_status"
    >
        <template #name="{ rowData }">
            <NonLocalizedStringWidget
                graph-slug="scheme"
                node-alias="statement_content_n1"
                :initial-value="rowData.statement_content_n1"
                :mode="VIEW"
                :hide-label="true"
            />
        </template>
        <template #type="{ rowData }">
            <ReferenceSelectWidget
                graph-slug="scheme"
                node-alias="statement_type_n1"
                :initial-value="rowData.statement_type_n1"
                :mode="VIEW"
                :hide-label="true"
            />
        </template>
        <template #language="{ rowData }">
            <ReferenceSelectWidget
                graph-slug="scheme"
                node-alias="statement_language_n1"
                :initial-value="rowData.statement_language_n1"
                :mode="VIEW"
                :hide-label="true"
            />
        </template>
        <template #drawer="{ rowData }">
            <ResourceInstanceMultiSelectWidget
                graph-slug="scheme"
                node-alias="statement_data_assignment_object_used"
                :initial-value="rowData.statement_data_assignment_object_used"
                :mode="VIEW"
            />
            <ResourceInstanceMultiSelectWidget
                graph-slug="scheme"
                node-alias="statement_data_assignment_actor"
                :initial-value="rowData.statement_data_assignment_actor"
                :mode="VIEW"
            />
        </template>
    </MetaStringViewer>
</template>
