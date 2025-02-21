<script setup lang="ts">
import { useGettext } from "vue3-gettext";

import MetaStringViewer from "@/arches_lingo/components/generic/MetaStringViewer.vue";
import ResourceInstanceRelationships from "@/arches_lingo/components/generic/ResourceInstanceRelationships.vue";
import ReferenceDatatype from "@/arches_lingo/components/generic/ReferenceDatatype.vue";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";

import { VIEW } from "@/arches_lingo/constants.ts";

import type {
    AppellativeStatus,
    MetaStringText,
} from "@/arches_lingo/types.ts";

const { $gettext } = useGettext();

const props = defineProps<{
    schemeLabels: AppellativeStatus[];
}>();

const metaStringLabel: MetaStringText = {
    deleteConfirm: $gettext("Are you sure you want to delete this label?"),
    language: $gettext("Label Language"),
    name: $gettext("Label Name"),
    type: $gettext("Label Type"),
    noRecords: $gettext("No scheme labels were found."),
};
</script>

<template>
    <SchemeReportSection
        :title-text="$gettext('Scheme Labels')"
        :button-text="$gettext('Add New Scheme Label')"
    >
        <MetaStringViewer
            :meta-strings="props.schemeLabels"
            :meta-string-text="metaStringLabel"
            graph-slug="scheme"
            node-alias="appellative_status"
        >
            <template #name="{ rowData }">
                <span>
                    {{
                        (rowData as AppellativeStatus)
                            .appellative_status_ascribed_name_content
                    }}
                </span>
            </template>
            <template #type="{ rowData }">
                <ReferenceDatatype
                    :value="
                        (rowData as AppellativeStatus)
                            .appellative_status_ascribed_relation
                    "
                    :mode="VIEW"
                >
                </ReferenceDatatype>
            </template>
            <template #language="{ rowData }">
                <ReferenceDatatype
                    :value="
                        (rowData as AppellativeStatus)
                            .appellative_status_ascribed_name_language
                    "
                    :mode="VIEW"
                >
                </ReferenceDatatype>
            </template>
            <template #drawer="{ rowData }">
                <div>
                    <span>{{ $gettext("Bibliographic Sources:") }}</span>
                    <ResourceInstanceRelationships
                        :value="
                            (rowData as AppellativeStatus)
                                .appellative_status_data_assignment_object_used
                        "
                    ></ResourceInstanceRelationships>
                </div>
                <div>
                    <span>{{ $gettext("Contributors:") }}</span>
                    <ResourceInstanceRelationships
                        :value="
                            (rowData as AppellativeStatus)
                                .appellative_status_data_assignment_actor
                        "
                    ></ResourceInstanceRelationships>
                </div>
            </template>
        </MetaStringViewer>
    </SchemeReportSection>
</template>
<style scoped>
:deep(.drawer) {
    padding: 1rem 2rem;
}
</style>
