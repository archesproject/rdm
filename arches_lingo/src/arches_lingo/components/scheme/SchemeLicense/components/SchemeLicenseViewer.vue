<script setup lang="ts">
import { inject } from "vue";
import { useGettext } from "vue3-gettext";
import Button from "primevue/button";
import type {
    SchemeRights,
    SchemeRightStatement,
} from "@/arches_lingo/types";
import { VIEW } from "@/arches_lingo/constants.ts";
import NonLocalizedStringWidget from "@/arches_component_lab/widgets/NonLocalizedStringWidget/NonLocalizedStringWidget.vue";
import ReferenceSelectWidget from "@/arches_controlled_lists/widgets/ReferenceSelectWidget/ReferenceSelectWidget.vue";
import ResourceInstanceMultiSelectWidget from "@/arches_component_lab/widgets/ResourceInstanceMultiSelectWidget/ResourceInstanceMultiSelectWidget.vue";

const props = defineProps<{
    schemeRights: SchemeRights | undefined;
    schemeRightStatement: SchemeRightStatement | undefined;
}>();
const { $gettext } = useGettext();

const openEditor = inject<(componentName: string) => void>("openEditor");

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
        <h3>{{ $gettext("Scheme Rights") }}</h3>
        <div>
            <Button
                :label="$gettext('Add New Scheme Right')"
                @click="openEditor!('SchemeLicense')"
            ></Button>
        </div>
    </div>
    <h4>{{ $gettext("Rights Holders") }}</h4>
    <ResourceInstanceMultiSelectWidget
        graph-slug="scheme"
        node-alias="right_holder"
        :initial-value="props.schemeRights?.right_holder"
        :hide-label="true"
        :mode="VIEW"
    />
    <h4>{{ $gettext("Rights Type") }}</h4>
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="right_type"
        :initial-value="props.schemeRights?.right_type"
        :multi-value="false"
        :hide-label="true"
        :mode="VIEW"
    />
    <h4>{{ $gettext("Statement") }}</h4>
    <NonLocalizedStringWidget
        graph-slug="scheme"
        node-alias="right_statement_content"
        :initial-value="props.schemeRightStatement?.right_statement_content"
        :mode="VIEW"
    />
    <h4>{{ $gettext("Statement Language") }}</h4>
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="right_statement_language"
        :initial-value="props.schemeRightStatement?.right_statement_language"
        :hide-label="true"
        :mode="VIEW"
    />
    <h4>{{ $gettext("Statement Type") }}</h4>
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="right_statement_type"
        :initial-value="props.schemeRightStatement?.right_statement_type"
        :hide-label="true"
        :mode="VIEW"
    />
    <h4>{{ $gettext("Statement Type Metatype") }}</h4>
    <ReferenceSelectWidget
        graph-slug="scheme"
        node-alias="right_statement_type_metatype"
        :initial-value="props.schemeRightStatement?.right_statement_type_metatype"
        :hide-label="true"
        :mode="VIEW"
    />
</template>