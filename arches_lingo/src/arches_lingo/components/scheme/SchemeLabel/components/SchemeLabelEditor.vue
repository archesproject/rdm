<script setup lang="ts">
import { inject, useTemplateRef, watch } from "vue";

import { useRouter } from "vue-router";
import { Form } from "@primevue/forms";

import DateWidget from "@/arches_component_lab/widgets/DateWidget/DateWidget.vue";
import NonLocalizedStringWidget from "@/arches_component_lab/widgets/NonLocalizedStringWidget/NonLocalizedStringWidget.vue";
import ReferenceSelectWidget from "@/arches_controlled_lists/widgets/ReferenceSelectWidget/ReferenceSelectWidget.vue";
import ResourceInstanceMultiSelectWidget from "@/arches_component_lab/widgets/ResourceInstanceMultiSelectWidget/ResourceInstanceMultiSelectWidget.vue";

import { createScheme, upsertLingoTile } from "@/arches_lingo/api.ts";
import { EDIT } from "@/arches_lingo/constants.ts";

import type { Component, Ref } from "vue";
import type { FormSubmitEvent } from "@primevue/forms";
import type { AppellativeStatus } from "@/arches_lingo/types.ts";

const props = defineProps<{
    tileData: AppellativeStatus | undefined;
    componentName: string;
    sectionTitle: string;
    graphSlug: string;
    nodegroupAlias: string;
    resourceInstanceId: string | undefined;
    tileId?: string;
}>();

const router = useRouter();

const schemeEditorFormRef = inject<Ref<Component | null>>(
    "schemeEditorFormRef",
);
const forceSectionRefresh = inject<(componentName: string) => void>(
    "forceSectionRefresh",
);

const formRef = useTemplateRef("form");
watch(
    () => formRef.value,
    (formComponent) => (schemeEditorFormRef!.value = formComponent),
);

async function save(e: FormSubmitEvent) {
    try {
        const formData = Object.fromEntries(
            Object.entries(e.states).map(([key, state]) => [key, state.value]),
        );

        if (!props.resourceInstanceId) {
            const updated = await createScheme({
                [props.nodegroupAlias]: [formData],
            });

            await router.push({
                name: props.graphSlug,
                params: { id: updated.resourceinstanceid },
            });

            // console.log(updated);  // UPDATED DOES NOT RETURN A TILEID!
            // openEditor!("SchemeLabel", updated.appellative_status[0].tileid);
        } else {
            await upsertLingoTile(
                props.graphSlug,
                props.nodegroupAlias,
                {
                    resourceinstance: props.resourceInstanceId,
                    ...formData,
                    tileid: props.tileId,
                },
                props.tileId,
            );
        }

        forceSectionRefresh!(props.componentName);
    } catch (error) {
        console.error(error);
    }
}
</script>

<template>
    <h4>{{ props.sectionTitle }}</h4>

    <Form
        ref="form"
        @submit="save"
    >
        <NonLocalizedStringWidget
            :graph-slug="props.graphSlug"
            node-alias="appellative_status_ascribed_name_content"
            :initial-value="
                props.tileData?.appellative_status_ascribed_name_content
            "
            :mode="EDIT"
        />
        <DateWidget
            :graph-slug="props.graphSlug"
            node-alias="appellative_status_timespan_begin_of_the_begin"
            :initial-value="
                props.tileData?.appellative_status_timespan_begin_of_the_begin
            "
            :mode="EDIT"
        />
        <DateWidget
            :graph-slug="props.graphSlug"
            node-alias="appellative_status_timespan_end_of_the_end"
            :initial-value="
                props.tileData?.appellative_status_timespan_end_of_the_end
            "
            :mode="EDIT"
        />

        <ResourceInstanceMultiSelectWidget
            :graph-slug="props.graphSlug"
            node-alias="appellative_status_data_assignment_actor"
            :initial-value="
                props.tileData?.appellative_status_data_assignment_actor
            "
            :mode="EDIT"
        />
        <ResourceInstanceMultiSelectWidget
            :graph-slug="props.graphSlug"
            node-alias="appellative_status_data_assignment_object_used"
            :initial-value="
                props.tileData?.appellative_status_data_assignment_object_used
            "
            :mode="EDIT"
        />

        <ReferenceSelectWidget
            :graph-slug="props.graphSlug"
            node-alias="appellative_status_ascribed_name_language"
            :initial-value="
                props.tileData?.appellative_status_ascribed_name_language
            "
            :mode="EDIT"
        />
        <ReferenceSelectWidget
            :graph-slug="props.graphSlug"
            node-alias="appellative_status_ascribed_relation"
            :initial-value="
                props.tileData?.appellative_status_ascribed_relation
            "
            :mode="EDIT"
        />
        <ReferenceSelectWidget
            :graph-slug="props.graphSlug"
            node-alias="appellative_status_status"
            :initial-value="props.tileData?.appellative_status_status"
            :mode="EDIT"
        />
        <ReferenceSelectWidget
            :graph-slug="props.graphSlug"
            node-alias="appellative_status_status_metatype"
            :initial-value="props.tileData?.appellative_status_status_metatype"
            :mode="EDIT"
        />
        <ReferenceSelectWidget
            :graph-slug="props.graphSlug"
            node-alias="appellative_status_data_assignment_type"
            :initial-value="
                props.tileData?.appellative_status_data_assignment_type
            "
            :mode="EDIT"
        />
    </Form>
</template>
