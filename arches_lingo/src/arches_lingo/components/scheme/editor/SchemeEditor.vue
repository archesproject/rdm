<script setup lang="ts">
import { inject, ref } from "vue";

import { useGettext } from "vue3-gettext";
import { useRouter } from "vue-router";

import Button from "primevue/button";
import { Form } from "@primevue/forms";

import { createScheme, upsertLingoTile } from "@/arches_lingo/api.ts";
import { EDIT, MAXIMIZE, MINIMIZE, CLOSE } from "@/arches_lingo/constants.ts";

import type { FormSubmitEvent } from "@primevue/forms";

const props = defineProps<{
    isEditorMaximized: boolean;
    component: any;
    graphSlug: string;
    nodeGroupAlias: string;
    resourceInstanceId: string | undefined;
    tileId?: string;
}>();

const { $gettext } = useGettext();
const router = useRouter();

const emit = defineEmits([MAXIMIZE, MINIMIZE, CLOSE]);

const forceSectionRefresh = inject<(componentName: string) => void>(
    "forceSectionRefresh",
);

const formKey = ref(0);

function toggleSize() {
    if (props.isEditorMaximized) {
        emit(MINIMIZE);
    } else {
        emit(MAXIMIZE);
    }
}

async function save(e: FormSubmitEvent) {
    try {
        const formData = Object.fromEntries(
            Object.entries(e.states).map(([key, state]) => [key, state.value]),
        );

        if (!props.resourceInstanceId) {
            const updated = await createScheme({
                [props.nodeGroupAlias]: [formData],
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
                props.nodeGroupAlias,
                {
                    resourceinstance: props.resourceInstanceId,
                    ...formData,
                    tileid: props.tileId,
                },
                props.tileId,
            );
        }

        forceSectionRefresh!(props.component.componentName);
    } catch (error) {
        console.error(error);
    }
}

function reset() {
    formKey.value += 1;
}
</script>

<template>
    <div class="container">
        <div class="header">
            <h3>{{ $gettext("Editor Tools") }}</h3>

            <div>
                <Button
                    :aria-label="$gettext('toggle editor size')"
                    @click="toggleSize"
                >
                    <i
                        :class="{
                            pi: true,
                            'pi-window-maximize': props.isEditorMaximized,
                            'pi-window-minimize': !props.isEditorMaximized,
                        }"
                        aria-hidden="true"
                    />
                </Button>
                <Button
                    :aria-label="$gettext('close editor')"
                    @click="$emit(CLOSE)"
                >
                    <i
                        class="pi pi-times"
                        aria-hidden="true"
                    />
                </Button>
            </div>
        </div>

        <Form
            :key="formKey"
            class="editor-form"
            @submit="save"
            @reset="reset"
        >
            <div class="editor-content">
                <component
                    :is="props.component"
                    v-bind="{ mode: EDIT, tileId: props.tileId }"
                />
            </div>
            <div>
                <Button
                    :label="$gettext('Save Changes')"
                    severity="success"
                    type="submit"
                />
                <Button
                    :label="$gettext('Cancel')"
                    severity="danger"
                    type="reset"
                />
            </div>
        </Form>
    </div>
</template>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.editor-form {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
}

.editor-content {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
}
</style>
