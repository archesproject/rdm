<script setup lang="ts">
import { useGettext } from "vue3-gettext";

import NonLocalizedStringWidget from "@/arches_component_lab/widgets/NonLocalizedStringWidget/NonLocalizedStringWidget.vue";
import ReferenceSelectWidget from "@/arches_controlled_lists/widgets/ReferenceSelectWidget/ReferenceSelectWidget.vue";
import ResourceInstanceMultiSelectWidget from "@/arches_component_lab/widgets/ResourceInstanceMultiSelectWidget/ResourceInstanceMultiSelectWidget.vue";
import DateWidget from "@/arches_component_lab/widgets/DateWidget/DateWidget.vue";

import { EDIT } from "@/arches_lingo/constants.ts";

import type { AppellativeStatus } from "@/arches_lingo/types.ts";

const { $gettext } = useGettext();

const props = defineProps<{
    schemeLabel: AppellativeStatus | undefined;
}>();
</script>

<template>
    <h4>{{ $gettext("Scheme Label") }}</h4>

    <NonLocalizedStringWidget
        graph-slug="scheme"
        node-alias="appellative_status_ascribed_name_content"
        :initial-value="
            props.schemeLabel?.appellative_status_ascribed_name_content
        "
        :mode="EDIT"
    />
    <DateWidget
        graph-slug="scheme"
        node-alias="appellative_status_timespan_begin_of_the_begin"
        :initial-value="
            props.schemeLabel?.appellative_status_timespan_begin_of_the_begin
        "
        :mode="EDIT"
    />
    <DateWidget
        graph-slug="scheme"
        node-alias="appellative_status_timespan_end_of_the_end"
        :initial-value="
            props.schemeLabel?.appellative_status_timespan_end_of_the_end
        "
        :mode="EDIT"
    />

    <ResourceInstanceMultiSelectWidget
        graph-slug="scheme"
        node-alias="appellative_status_data_assignment_actor"
        :initial-value="
            props.schemeLabel?.appellative_status_data_assignment_actor
        "
        :mode="EDIT"
    />
    <ResourceInstanceMultiSelectWidget
        graph-slug="scheme"
        node-alias="appellative_status_data_assignment_object_used"
        :initial-value="
            props.schemeLabel?.appellative_status_data_assignment_object_used
        "
        :mode="EDIT"
    />

    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="appellative_status_ascribed_name_language"
        :initial-value="
            props.schemeLabel?.appellative_status_ascribed_name_language
        "
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="appellative_status_ascribed_relation"
        :initial-value="props.schemeLabel?.appellative_status_ascribed_relation"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="appellative_status_status"
        :initial-value="props.schemeLabel?.appellative_status_status"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="appellative_status_status_metatype"
        :initial-value="props.schemeLabel?.appellative_status_status_metatype"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="appellative_status_data_assignment_type"
        :initial-value="
            props.schemeLabel?.appellative_status_data_assignment_type
        "
        :mode="EDIT"
    />
</template>
