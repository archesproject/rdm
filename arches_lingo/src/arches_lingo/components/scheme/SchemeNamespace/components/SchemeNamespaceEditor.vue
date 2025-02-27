<script setup lang="ts">
import { inject, useTemplateRef, watch, type Component, type Ref } from "vue";
import { useRouter } from "vue-router";

import { Form } from "@primevue/forms";

import NonLocalizedStringWidget from "@/arches_component_lab/widgets/NonLocalizedStringWidget/NonLocalizedStringWidget.vue";

import { createScheme, upsertLingoTile } from "@/arches_lingo/api.ts";
import { EDIT } from "@/arches_lingo/constants.ts";

import type { FormSubmitEvent } from "@primevue/forms";
import type { SchemeNamespace } from "@/arches_lingo/types.ts";

const router = useRouter();

const props = defineProps<{
    tileData: SchemeNamespace | undefined;
    graphSlug: string;
    sectionTitle: string;
    resourceInstanceId: string | undefined;
    componentName: string;
    nodegroupAlias: string;
    tileId?: string;
}>();

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
            node-alias="namespace_name"
            :graph-slug="props.graphSlug"
            :initial-value="props.tileData?.namespace_name"
            :mode="EDIT"
        />
    </Form>
</template>
