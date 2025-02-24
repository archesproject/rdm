<script setup lang="ts">
import { inject } from "vue";
import { useGettext } from "vue3-gettext";

import Button from "primevue/button";

import MetaStringViewer from "@/arches_lingo/components/generic/MetaStringViewer.vue";

import NonLocalizedStringWidget from "@/arches_component_lab/widgets/NonLocalizedStringWidget/NonLocalizedStringWidget.vue";
import ReferenceSelectWidget from "@/arches_controlled_lists/widgets/ReferenceSelectWidget/ReferenceSelectWidget.vue";
import ResourceInstanceMultiSelectWidget from "@/arches_component_lab/widgets/ResourceInstanceMultiSelectWidget/ResourceInstanceMultiSelectWidget.vue";

import { VIEW } from "@/arches_lingo/constants.ts";

import type {
    AppellativeStatus,
    MetaStringText,
} from "@/arches_lingo/types.ts";

const props = defineProps<{
    schemeLabels: AppellativeStatus[];
}>();

// need NodeGroup info here ( cardinality ) for proper button text

const { $gettext } = useGettext();

const openEditor = inject<(componentName: string) => void>("openEditor");

const metaStringLabel: MetaStringText = {
    deleteConfirm: $gettext("Are you sure you want to delete this label?"),
    language: $gettext("Label Language"),
    name: $gettext("Label Name"),
    type: $gettext("Label Type"),
    noRecords: $gettext("No scheme labels were found."),
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
        <h3>{{ $gettext("Scheme Label") }}</h3>

        <div>
            <Button
                :label="$gettext('Add New Scheme Label')"
                @click="openEditor!('SchemeLabel')"
            ></Button>
        </div>
    </div>

    <MetaStringViewer
        :meta-strings="props.schemeLabels"
        :meta-string-text="metaStringLabel"
        component-name="SchemeLabel"
        graph-slug="scheme"
        node-alias="appellative_status"
    >
        <template #name="{ rowData }">
            <NonLocalizedStringWidget
                graph-slug="scheme"
                node-alias="appellative_status_ascribed_name_content"
                :initial-value="
                    rowData.appellative_status_ascribed_name_content
                "
                :mode="VIEW"
                :hide-label="true"
            />
        </template>
        <template #type="{ rowData }">
            <ReferenceSelectWidget
                graph-slug="scheme"
                node-alias="appellative_status_ascribed_relation"
                :initial-value="rowData.appellative_status_ascribed_relation"
                :mode="VIEW"
                :hide-label="true"
            />
        </template>
        <template #language="{ rowData }">
            <ReferenceSelectWidget
                graph-slug="scheme"
                node-alias="appellative_status_ascribed_name_language"
                :initial-value="
                    rowData.appellative_status_ascribed_name_language
                "
                :mode="VIEW"
                :hide-label="true"
            />
        </template>
        <template #drawer="{ rowData }">
            <ResourceInstanceMultiSelectWidget
                graph-slug="scheme"
                node-alias="appellative_status_data_assignment_object_used"
                :initial-value="
                    rowData.appellative_status_data_assignment_object_used
                "
                :mode="VIEW"
            />
            <ResourceInstanceMultiSelectWidget
                graph-slug="scheme"
                node-alias="appellative_status_data_assignment_actor"
                :initial-value="
                    rowData.appellative_status_data_assignment_actor
                "
                :mode="VIEW"
            />
        </template>
    </MetaStringViewer>
</template>
