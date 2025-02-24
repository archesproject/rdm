<script setup lang="ts">
import { onMounted, ref } from "vue";

import ProgressSpinner from "primevue/progressspinner";

import SchemeNoteEditor from "@/arches_lingo/components/scheme/SchemeNote/components/SchemeNoteEditor.vue";
import SchemeNoteViewer from "@/arches_lingo/components/scheme/SchemeNote/components/SchemeNoteViewer.vue";

import { EDIT, VIEW } from "@/arches_lingo/constants.ts";

import { fetchLingoResourcePartial } from "@/arches_lingo/api.ts";

import type {
    DataComponentMode,
    SchemeStatement,
} from "@/arches_lingo/types.ts";

const props = defineProps<{
    mode: DataComponentMode;
    tileId?: string | null;
    graphSlug: string;
    nodeGroupAlias: string;
    resourceInstanceId: string | undefined;
}>();

const isLoading = ref(false);
const SchemeNotes = ref([]);

const shouldCreateNewTile = Boolean(props.mode === EDIT && !props.tileId);

onMounted(async () => {
    if (!props.resourceInstanceId) return;

    if (props.mode === VIEW || !shouldCreateNewTile) {
        const sectionValue = await getSectionValue();

        if (props.tileId) {
            SchemeNotes.value = sectionValue[props.nodeGroupAlias].filter(
                (status: SchemeStatement) => status.tileid === props.tileId,
            );
        } else {
            SchemeNotes.value = sectionValue[props.nodeGroupAlias];
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
        <SchemeNoteViewer
            v-if="mode === VIEW"
            :scheme-notes="SchemeNotes"
        />
        <SchemeNoteEditor
            v-else-if="mode === EDIT"
            :scheme-note="shouldCreateNewTile ? undefined : SchemeNotes[0]"
        />
    </template>
</template>
