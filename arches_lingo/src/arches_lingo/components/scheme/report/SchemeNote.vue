<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useGettext } from "vue3-gettext";
import { useRoute } from "vue-router";
import { useToast } from "primevue/usetoast";
import MetaStringViewer from "@/arches_lingo/components/generic/MetaStringViewer.vue";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
import { deleteSchemeNoteTile, fetchSchemeNotes } from "@/arches_lingo/api.ts";
import { ERROR, OPEN_EDITOR, VIEW, EDIT } from "@/arches_lingo/constants.ts";
import type {
    DataComponentMode,
    MetaStringText,
    SchemeInstance,
    SchemeStatement,
} from "@/arches_lingo/types.ts";
import ResourceInstanceRelationships from "@/arches_lingo/components/generic/ResourceInstanceRelationships.vue";
import ControlledListItem from "@/arches_lingo/components/generic/ControlledListItem.vue";

const { $gettext } = useGettext();
const schemeInstance = ref<SchemeInstance>();
const route = useRoute();
const toast = useToast();
const metaStringLabel: MetaStringText = {
    deleteConfirm: $gettext("Are you sure you want to delete this note?"),
    language: $gettext("Note Language"),
    name: $gettext("Note Name"),
    type: $gettext("Note Type"),
};

withDefaults(
    defineProps<{
        mode?: DataComponentMode;
        tileId?: string | null;
    }>(),
    {
        mode: VIEW,
        tileId: null, // editor arg specifying what tile to operate on.
    },
);

const emits = defineEmits([OPEN_EDITOR]);

defineExpose({ getSectionValue });

onMounted(() => {
    getSectionValue();
});

async function getSectionValue() {
    try {
        const result = await fetchSchemeNotes(route.params.id as string);
        schemeInstance.value = {
            statement: result.statement,
        };
    } catch (error) {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error"),
            detail:
                error instanceof Error
                    ? error.message
                    : $gettext("Could not fetch the notes for the resource"),
        });
    }
}

async function deleteSectionValue(tileId: string) {
    let result = false;
    try {
        result = await deleteSchemeNoteTile(route.params.id as string, tileId);
    } catch (error) {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error"),
            detail:
                error instanceof Error
                    ? error.message
                    : $gettext("Could not delete selected note"),
        });
    }

    if (result) {
        getSectionValue();
    }
}

function editSectionValue(tileId: string) {
    const SchemeStatement = schemeInstance.value?.statement?.find(
        (tile) => tile.tileid === tileId,
    );
    if (SchemeStatement && SchemeStatement.tileid === tileId) {
        emits(OPEN_EDITOR, SchemeStatement.tileid);
    } else {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error"),
            detail: $gettext("Could not find the selected label to edit"),
        });
    }
}
</script>

<template>
    <div v-if="mode === VIEW">
        <SchemeReportSection
            :title-text="$gettext('Scheme Notes')"
            @open-editor="emits(OPEN_EDITOR)"
        >
            <MetaStringViewer
                :meta-strings="schemeInstance?.statement"
                :meta-string-text="metaStringLabel"
                @edit-string="editSectionValue"
                @delete-string="deleteSectionValue"
            >
                <template #name="{ rowData }">
                    {{ (rowData as SchemeStatement).statement_content_n1 }}
                </template>
                <template #type="{ rowData }">
                    <ControlledListItem
                        :value="(rowData as SchemeStatement).statement_type_n1"
                    >
                    </ControlledListItem>
                </template>
                <template #language="{ rowData }">
                    <ControlledListItem
                        :value="
                            (rowData as SchemeStatement).statement_language_n1
                        "
                    >
                    </ControlledListItem>
                </template>
                <template #drawer="{ rowData }">
                    <div>
                        {{ $gettext("Bibliographic Sources") }}:
                        <ResourceInstanceRelationships
                            :value="
                                (rowData as SchemeStatement)
                                    .statement_data_assignment_object_used
                            "
                        ></ResourceInstanceRelationships>
                    </div>
                    <div>
                        {{ $gettext("Contributors") }}:
                        <ResourceInstanceRelationships
                            :value="
                                (rowData as SchemeStatement)
                                    .statement_data_assignment_actor
                            "
                        ></ResourceInstanceRelationships>
                    </div>
                </template>
            </MetaStringViewer>
        </SchemeReportSection>
    </div>
    <div v-if="mode === EDIT"></div>
</template>
