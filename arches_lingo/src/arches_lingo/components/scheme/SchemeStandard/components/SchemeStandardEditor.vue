<script setup lang="ts">
import { inject, useTemplateRef, watch, type Component, type Ref } from "vue";
import { useRouter } from "vue-router";

import { Form } from "@primevue/forms";

import ResourceInstanceMultiSelectWidget from "@/arches_component_lab/widgets/ResourceInstanceMultiSelectWidget/ResourceInstanceMultiSelectWidget.vue";

import { createScheme, upsertLingoTile } from "@/arches_lingo/api.ts";
import { EDIT } from "@/arches_lingo/constants.ts";

import type { FormSubmitEvent } from "@primevue/forms";
import type { SchemeCreation } from "@/arches_lingo/types.ts";

const props = defineProps<{
    tileData: SchemeCreation | undefined;
    graphSlug: string;
    sectionTitle: string;
    resourceInstanceId: string | undefined;
    componentName: string;
    nodegroupAlias: string;
    tileId?: string;
}>();

const router = useRouter();

const schemeEditorFormRef = inject<Ref<Component | null>>(
    "schemeEditorFormRef",
);
const refreshReportSection = inject<(componentName: string) => void>(
    "refreshReportSection",
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
                [props.nodegroupAlias]: formData,
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

        refreshReportSection!(props.componentName);
    } catch (error) {
        console.error(error);
    }
}
</script>

<template>
    <h3>{{ props.sectionTitle }}</h3>

    <Form
        ref="form"
        @submit="save"
    >
        <ResourceInstanceMultiSelectWidget
            graph-slug="scheme"
            node-alias="creation_sources"
            :initial-value="props.tileData?.creation_sources"
            :mode="EDIT"
        />
    </Form>
</template>
