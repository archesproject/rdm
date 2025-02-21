<script setup lang="ts">
import { onMounted, ref } from "vue";

import { useGettext } from "vue3-gettext";
import { useRoute } from "vue-router";
import { useToast } from "primevue/usetoast";

import ProgressSpinner from "primevue/progressspinner";

import SchemeLabelEditor from "@/arches_lingo/components/scheme/SchemeLabel/components/SchemeLabelEditor.vue";
import SchemeLabelViewer from "@/arches_lingo/components/scheme/SchemeLabel/components/SchemeLabelViewer.vue";

import { EDIT, ERROR, VIEW } from "@/arches_lingo/constants.ts";

import { fetchLingoResourcePartial } from "@/arches_lingo/api.ts";

import type {
    AppellativeStatus,
    DataComponentMode,
} from "@/arches_lingo/types.ts";

defineOptions({
    componentName: "SchemeLabel",
});

const props = defineProps<{
    mode: DataComponentMode;
    tileId?: string | null;
}>();

const { $gettext } = useGettext();
const toast = useToast();
const route = useRoute();

const isLoading = ref(true);
const schemeLabels = ref<AppellativeStatus[]>([]);

const shouldCreateNewTile = Boolean(props.mode === EDIT && !props.tileId);

onMounted(async () => {
    if (props.mode === VIEW || !shouldCreateNewTile) {
        const sectionValue = await getSectionValue();

        if (props.tileId) {
            schemeLabels.value = sectionValue.appellative_status.filter(
                (appellativeStatus: AppellativeStatus) =>
                    appellativeStatus.tileid === props.tileId,
            );
        } else {
            schemeLabels.value = sectionValue.appellative_status;
        }
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
