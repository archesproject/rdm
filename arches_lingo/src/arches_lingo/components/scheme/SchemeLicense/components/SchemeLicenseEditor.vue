<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import type {
    SchemeRights,
    SchemeRightStatement,
} from "@/arches_lingo/types";
import { EDIT } from "@/arches_lingo/constants.ts";
import NonLocalizedStringWidget from "@/arches_component_lab/widgets/NonLocalizedStringWidget/NonLocalizedStringWidget.vue";
import ReferenceSelectWidget from "@/arches_controlled_lists/widgets/ReferenceSelectWidget/ReferenceSelectWidget.vue";
import ResourceInstanceMultiSelectWidget from "@/arches_component_lab/widgets/ResourceInstanceMultiSelectWidget/ResourceInstanceMultiSelectWidget.vue";

const props = defineProps<{
    schemeRights: SchemeRights | undefined;
    schemeRightStatement: SchemeRightStatement | undefined;
}>();

const { $gettext } = useGettext();

</script>
<template>
    <h4>{{ $gettext("Scheme Rights") }}</h4>
    <ResourceInstanceMultiSelectWidget
        graph-slug="scheme"
        node-alias="right_holder"
        :initial-value="props.schemeRights?.right_holder"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="right_type"
        :initial-value="props.schemeRights?.right_type"
        :multi-value="false"
        :mode="EDIT"
    />
    <NonLocalizedStringWidget
        graph-slug="scheme"
        node-alias="right_statement_content"
        :initial-value="props.schemeRightStatement?.right_statement_content"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="right_statement_language"
        :initial-value="props.schemeRightStatement?.right_statement_language"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="right_statement_type"
        :initial-value="props.schemeRightStatement?.right_statement_type"
        :mode="EDIT"
    />
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="right_statement_type_metatype"
        :initial-value="props.schemeRightStatement?.right_statement_type_metatype"
        :mode="EDIT"
    />
</template>