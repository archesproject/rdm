<script setup lang="ts">
import { onMounted, ref } from "vue";

import ProgressSpinner from "primevue/progressspinner";

import SchemeStandardViewer from "@/arches_lingo/components/scheme/SchemeStandard/components/SchemeStandardViewer.vue";
import SchemeStandardEditor from "@/arches_lingo/components/scheme/SchemeStandard/components/SchemeStandardEditor.vue";

import { EDIT, VIEW } from "@/arches_lingo/constants.ts";

import { fetchLingoResourcePartial } from "@/arches_lingo/api.ts";

import type {
    DataComponentMode,
    SchemeCreation,
} from "@/arches_lingo/types.ts";

const props = defineProps<{
    mode: DataComponentMode;
    tileId?: string | null;
    graphSlug: string;
    nodeGroupAlias: string;
    resourceInstanceId: string | undefined;
}>();

const isLoading = ref(false);
const schemeCreation = ref<SchemeCreation>();

const shouldCreateNewTile = Boolean(props.mode === EDIT && !props.tileId);

onMounted(async () => {
    if (!props.resourceInstanceId) return;

    if (props.mode === VIEW || !shouldCreateNewTile) {
        const sectionValue = await getSectionValue();

        schemeCreation.value = sectionValue.creation;
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
        <SchemeStandardViewer
            v-if="mode === VIEW"
            :scheme-creation="schemeCreation"
        />
        <SchemeStandardEditor
            v-else-if="mode === EDIT"
            :scheme-creation="schemeCreation"
        />
    </template>
</template>
