<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { fetchLingoResource } from "@/arches_lingo/api.ts";

import type {
    DataComponentMode,
    SchemeRights,
    SchemeRightStatement,
} from "@/arches_lingo/types";
import {
    NEW,
    VIEW,
    EDIT,
} from "@/arches_lingo/constants.ts";
import SchemeLicenseViewer from "@/arches_lingo/components/scheme/SchemeLicense/components/SchemeLicenseViewer.vue";
import SchemeLicenseEditor from "@/arches_lingo/components/scheme/SchemeLicense/components/SchemeLicenseEditor.vue";

const props = defineProps<{
    mode: DataComponentMode;
    tileId?: string | null;
    graphSlug: string;
    nodeGroupAlias: string;
    resourceInstanceId: string | undefined;
}>();

const isLoading = ref(false);
const schemeRights = ref<SchemeRights>({});
const schemeRightStatement = ref<SchemeRightStatement>({});
const shouldCreateNewTile = Boolean(props.mode === EDIT && !props.tileId);

onMounted(async () => {
    getSectionValue();
});

const route = useRoute();


async function getSectionValue() {
    if (route.params.id === NEW) {
        return;
    }
    const schemeInstance = await fetchLingoResource(
        "scheme",
        route.params.id as string,
    );
    schemeRights.value = schemeInstance?.rights ?? {};
    schemeRightStatement.value = schemeInstance?.rights?.right_statement ?? {};
}
</script>

<template>
    <ProgressSpinner
        v-if="isLoading"
        style="width: 100%"
    />
    <template v-else>
        <SchemeLicenseViewer
            v-if="mode === VIEW"
            :scheme-rights="schemeRights"
            :scheme-right-statement="schemeRightStatement"
        />
        <SchemeLicenseEditor
            v-else-if="mode === EDIT"
            :scheme-rights="shouldCreateNewTile ? undefined : schemeRights"
            :scheme-right-statement="shouldCreateNewTile ? undefined : schemeRightStatement"
        />
    </template>
</template>
