<script setup lang="ts">
import { onMounted, ref } from "vue";

import ProgressSpinner from "primevue/progressspinner";

import SchemeLabelEditor from "@/arches_lingo/components/scheme/SchemeLabel/components/SchemeLabelEditor.vue";
import SchemeLabelViewer from "@/arches_lingo/components/scheme/SchemeLabel/components/SchemeLabelViewer.vue";

import { EDIT, VIEW } from "@/arches_lingo/constants.ts";

import { fetchLingoResourcePartial } from "@/arches_lingo/api.ts";

import type {
    AppellativeStatus,
    DataComponentMode,
} from "@/arches_lingo/types.ts";

const props = defineProps<{
    mode: DataComponentMode;
    tileId?: string | null;
    graphSlug: string;
    nodeGroupAlias: string;
    resourceInstanceId: string | undefined;
}>();

const isLoading = ref(false);
const schemeLabels = ref<AppellativeStatus[]>([]);

const shouldCreateNewTile = Boolean(props.mode === EDIT && !props.tileId);

onMounted(async () => {
    if (!props.resourceInstanceId) return;

    if (props.mode === VIEW || !shouldCreateNewTile) {
        const sectionValue = await getSectionValue();

        if (props.tileId) {
            schemeLabels.value = sectionValue.appellative_status.filter(
                (status: AppellativeStatus) => status.tileid === props.tileId,
            );
        } else {
            schemeLabels.value = sectionValue.appellative_status;
        }
    }
});

async function getSectionValue() {
    isLoading.value = true;

    try {
        return await fetchLingoResourcePartial(
            props.graphSlug,
            props.resourceInstanceId as string,
            props.nodeGroupAlias,
        );
    } catch (error) {
        console.error(error);
    } finally {
        isLoading.value = false;
    }
}
</script>

<template>
    <ProgressSpinner
        v-if="isLoading"
        style="width: 100%"
    />

    <template v-else>
        <SchemeLabelViewer
            v-if="mode === VIEW"
            :scheme-labels="schemeLabels"
        />
        <SchemeLabelEditor
            v-else-if="mode === EDIT"
            :scheme-label="shouldCreateNewTile ? undefined : schemeLabels[0]"
        />
    </template>
</template>
