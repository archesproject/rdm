<script setup lang="ts">
import { useGettext } from "vue3-gettext";

import NonLocalizedStringWidget from "@/arches_component_lab/widgets/NonLocalizedStringWidget/NonLocalizedStringWidget.vue";
import ReferenceSelectWidget from "@/arches_controlled_lists/widgets/ReferenceSelectWidget/ReferenceSelectWidget.vue";
import ResourceInstanceMultiSelectWidget from "@/arches_component_lab/widgets/ResourceInstanceMultiSelectWidget/ResourceInstanceMultiSelectWidget.vue";
import DateWidget from "@/arches_component_lab/widgets/DateWidget/DateWidget.vue";

import { EDIT } from "@/arches_lingo/constants.ts";

import type { SchemeStatement } from "@/arches_lingo/types.ts";

const { $gettext } = useGettext();

const props = defineProps<{
    schemeNote: SchemeStatement | undefined;
}>();
</script>

<template>
    <h4>{{ $gettext("Scheme Note") }}</h4>

    <NonLocalizedStringWidget
        graph-slug="scheme"
        node-alias="statement_content_n1"
        :initial-value="props.schemeNote?.statement_content_n1"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="statement_language_n1"
        :initial-value="props.schemeNote?.statement_language_n1"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="statement_type_n1"
        :initial-value="props.schemeNote?.statement_type_n1"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="statement_type_metatype_n1"
        :initial-value="props.schemeNote?.statement_type_metatype_n1"
        :mode="EDIT"
    />
    <DateWidget
        graph-slug="scheme"
        node-alias="statement_data_assignment_timespan_begin_of_the_begin"
        :initial-value="
            props.schemeNote
                ?.statement_data_assignment_timespan_begin_of_the_begin
        "
        :mode="EDIT"
    />
    <DateWidget
        graph-slug="scheme"
        node-alias="statement_data_assignment_timespan_end_of_the_end"
        :initial-value="
            props.schemeNote?.statement_data_assignment_timespan_end_of_the_end
        "
        :mode="EDIT"
    />
    <ResourceInstanceMultiSelectWidget
        graph-slug="scheme"
        node-alias="statement_data_assignment_actor"
        :initial-value="props.schemeNote?.statement_data_assignment_actor"
        :mode="EDIT"
    />
    <ResourceInstanceMultiSelectWidget
        graph-slug="scheme"
        node-alias="statement_data_assignment_object_used"
        :initial-value="props.schemeNote?.statement_data_assignment_object_used"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="statement_data_assignment_type"
        :initial-value="props.schemeNote?.statement_data_assignment_type"
        :mode="EDIT"
    />
</template>
