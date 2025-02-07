<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useGettext } from "vue3-gettext";

import Button from "primevue/button";
import { useToast } from "primevue/usetoast";

import ResourceInstanceRelationships from "@/arches_lingo/components/generic/ResourceInstanceRelationships.vue";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
import {
    createScheme,
    fetchLingoResourcePartial,
    updateLingoResource,
} from "@/arches_lingo/api.ts";
import {
    VIEW,
    EDIT,
    OPEN_EDITOR,
    NEW,
    UPDATED,
    ERROR,
} from "@/arches_lingo/constants.ts";

import type {
    DataComponentMode,
    ResourceInstanceReference,
    SchemeInstance,
} from "@/arches_lingo/types";

const toast = useToast();
const schemeInstance = ref<SchemeInstance>({});
const route = useRoute();
const router = useRouter();
const { $gettext } = useGettext();

const { mode = VIEW } = defineProps<{
    mode?: DataComponentMode;
}>();

const emit = defineEmits([OPEN_EDITOR, UPDATED]);

defineExpose({ getSectionValue });

onMounted(async () => {
    getSectionValue();
});

async function save() {
    try {
        let updated;
        if (route.params.id === NEW) {
            updated = await createScheme(schemeInstance.value);
            await router.push({
                name: "scheme",
                params: { id: updated.resourceinstanceid },
            });
        } else {
            updated = await updateLingoResource(
                "scheme",
                route.params.id as string,
                schemeInstance.value,
            );
        }
        schemeInstance.value = updated;
        emit(UPDATED);
    } catch (error) {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error saving scheme"),
            detail: (error as Error).message,
        });
    }
}

async function setSchemeInstance() {
    try {
        const scheme = await fetchLingoResourcePartial(
            "scheme",
            route.params.id as string,
            "creation",
        );

        schemeInstance.value = scheme;
    } catch (error) {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error"),
            detail:
                error instanceof Error
                    ? error.message
                    : $gettext("Could not fetch the scheme standard"),
        });
    }
}

async function getSectionValue() {
    setSchemeInstance();
}

function onCreationUpdate(val: ResourceInstanceReference[]) {
    const schemeInstanceValue = schemeInstance.value!; // should never be null when updating

    if (!schemeInstanceValue?.creation) {
        schemeInstanceValue.creation = { creation_sources: val };
    } else {
        schemeInstanceValue.creation.creation_sources = val;
    }
}
</script>

<template>
    <div v-if="mode === VIEW">
        <SchemeReportSection
            :title-text="$gettext('Scheme Standards Followed')"
            :button-text="$gettext('Update Scheme Standards')"
            @open-editor="emit(OPEN_EDITOR)"
        >
            <ResourceInstanceRelationships
                :value="schemeInstance?.creation?.creation_sources"
            />
            <!-- Discussion of namespace_type indicated it should not be displayed or edited manually,
                 if this changes, the ControlledListItem widget can be used.-->
        </SchemeReportSection>
    </div>
    <div v-if="mode === EDIT">
        <ResourceInstanceRelationships
            :value="schemeInstance?.creation?.creation_sources"
            graph-slug="scheme"
            node-alias="creation_sources"
            :mode="EDIT"
            @update="onCreationUpdate"
        />
        <Button
            :label="$gettext('Update')"
            @click="save"
        />
    </div>
</template>
