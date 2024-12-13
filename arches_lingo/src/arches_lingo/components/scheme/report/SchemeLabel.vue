<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { VIEW, EDIT, OPEN_EDITOR } from "@/arches_lingo/constants.ts";
import type {
    DataComponentMode,
    SchemeInstance,
} from "@/arches_lingo/types.ts";
import { fetchSchemeLabel } from "@/arches_lingo/api.ts";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
import LabelViewer from "@/arches_lingo/components/generic/LabelViewer.vue";

const schemeInstance = ref<SchemeInstance>();
const { $gettext } = useGettext();
const route = useRoute();

const props = withDefaults(
    defineProps<{
        mode?: DataComponentMode;
        args?: Array<object>;
    }>(),
    {
        mode: VIEW,
        args: () => [],
    },
);

defineExpose({ save, getSectionValue });

const emits = defineEmits([OPEN_EDITOR]);

onMounted(async () => {
    getSectionValue();
});

async function deleteLabel() {
    // deletes label
    console.log("deleted");
}

async function getSectionValue() {
    console.log(props);
    const result = await fetchSchemeLabel(route.params.id as string);
    schemeInstance.value = {
        appellative_status: result.appellative_status,
    };
}

async function save() {
    // todo for Johnathan.  This function will save the values of the form back to arches.
}

// async function update() {
//     // todo for Johnathan.  This function will handle the update emit when the user changes values in your form - you store those values in this section.
// }
</script>

<template>
    <div v-if="!mode || mode === VIEW">
        <SchemeReportSection
            :title-text="$gettext('Scheme Labels')"
            @open-editor="emits(OPEN_EDITOR)"
        >
            <LabelViewer
                :value="schemeInstance?.appellative_status"
                @edit-label="(...args) => emits(OPEN_EDITOR, ...args)"
                @delete-label="deleteLabel"
            ></LabelViewer>
        </SchemeReportSection>
    </div>
    <div v-if="mode === EDIT"><!-- todo for Johnathan-->abc</div>
</template>
<style scoped>
:deep(.drawer) {
    padding: 1rem 2rem;
}

:deep(.resource-instance-relationship-view) {
    padding: 0 0.25rem;
}
</style>
