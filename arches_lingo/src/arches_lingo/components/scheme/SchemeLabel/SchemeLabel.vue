<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { useGettext } from "vue3-gettext";
import { useRoute } from "vue-router";
import { useToast } from "primevue/usetoast";

import ProgressSpinner from "primevue/progressspinner";

import SchemeLabelEditor from "@/arches_lingo/components/scheme/SchemeLabel/components/SchemeLabelEditor.vue";
import SchemeLabelViewer from "@/arches_lingo/components/scheme/SchemeLabel/components/SchemeLabelViewer.vue";

import { EDIT, ERROR, NEW, VIEW } from "@/arches_lingo/constants.ts";

import { fetchLingoResourcePartial } from "@/arches_lingo/api.ts";

import type {
    DataComponentMode,
    SchemeInstance,
} from "@/arches_lingo/types.ts";

const props = defineProps<{
    mode: DataComponentMode;
    tileId?: string | null;
}>();

const { $gettext } = useGettext();
const toast = useToast();
const route = useRoute();

const isLoading = ref(true);
const schemeInstance = ref<SchemeInstance>();
const appellativeStatusToEdit = computed(() => {
    return schemeInstance.value?.appellative_status?.find(
        (tile) => tile.tileid === props.tileId,
    );
});

onMounted(async () => {
    if (route.params.id !== NEW) {
        const sectionValue = await getSectionValue();

        schemeInstance.value = {
            appellative_status: sectionValue.appellative_status,
        };
    }

    isLoading.value = false;
});

async function getSectionValue() {
    try {
        return await fetchLingoResourcePartial(
            "scheme",
            route.params.id as string,
            "appellative_status",
        );
    } catch (error) {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error"),
            detail:
                error instanceof Error
                    ? error.message
                    : $gettext("Could not fetch the labels for the resource"),
        });
    }
}

async function update(tileId: string | undefined) {
    // await emit(UPDATED);
    // if (tileId) {
    //     await emit(OPEN_EDITOR, tileId);
    // }
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
            :scheme-instance="schemeInstance"
        />
        <SchemeLabelEditor
            v-else-if="mode === EDIT"
            :value="appellativeStatusToEdit"
            @update="update"
        />
    </template>
</template>
