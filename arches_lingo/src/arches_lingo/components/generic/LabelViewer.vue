<script setup lang="ts">
import { ref } from "vue";
import { useGettext } from "vue3-gettext";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import ConfirmDialog from "primevue/confirmdialog";
import { useConfirm } from "primevue/useconfirm";

import ControlledListItem from "@/arches_lingo/components/generic/ControlledListItem.vue";
import ResourceInstanceRelationships from "@/arches_lingo/components/generic/ResourceInstanceRelationships.vue";

import type { AppellativeStatus } from "@/arches_lingo/types";

const { $gettext } = useGettext();
const confirm = useConfirm();

const props = defineProps<{
    value?: AppellativeStatus[];
}>();

const emits = defineEmits(["editLabel", "deleteLabel"]);

const expandedRows = ref([]);

function confirmDelete(tileId: string) {
    confirm.require({
        header: $gettext("Confirmation"),
        message: $gettext("Are you sure you want to delete this label?"),
        accept: () => {
            emits("deleteLabel", tileId);
        },
        rejectProps: {
            label: "Cancel",
            severity: "secondary",
            outlined: true,
        },
        acceptProps: {
            label: "Delete",
            severity: "danger",
        },
    });
}
</script>

<template>
    <ConfirmDialog
        :pt="{ root: { style: { fontFamily: 'sans-serif' } } }"
    ></ConfirmDialog>
    <DataTable
        v-model:expanded-rows="expandedRows"
        :value="props.value"
        table-style="min-width: 50rem"
    >
        <Column
            expander
            style="width: 3rem"
        />
        <Column
            field="appellative_status_ascribed_name_content"
            :header="$gettext('Label')"
            sortable
        >
            <template #body="slotProps">
                {{
                    (slotProps.data as AppellativeStatus)
                        .appellative_status_ascribed_name_content
                }}
            </template>
        </Column>
        <Column
            field="appellative_status_ascribed_relation"
            :header="$gettext('Label Type')"
            sortable
        >
            <template #body="slotProps">
                <ControlledListItem
                    :value="
                        (slotProps.data as AppellativeStatus)
                            .appellative_status_ascribed_relation
                    "
                >
                </ControlledListItem>
            </template>
        </Column>
        <Column
            field="appellative_status_ascribed_name_language"
            :header="$gettext('Label Language')"
            sortable
        >
            <template #body="slotProps">
                <ControlledListItem
                    :value="
                        (slotProps.data as AppellativeStatus)
                            .appellative_status_ascribed_name_language
                    "
                >
                </ControlledListItem>
            </template>
        </Column>
        <Column>
            <template #body="slotProps">
                <div class="controls">
                    <Button
                        icon="pi pi-file-edit"
                        :aria-label="$gettext('edit')"
                        @click="
                            () =>
                                emits(
                                    'editLabel',
                                    (slotProps.data as AppellativeStatus)
                                        .tileid,
                                )
                        "
                    />
                    <Button
                        icon="pi pi-trash"
                        :aria-label="$gettext('delete')"
                        severity="danger"
                        outlined
                        @click="
                            () =>
                                confirmDelete(
                                    (slotProps.data as AppellativeStatus)
                                        .tileid,
                                )
                        "
                    />
                </div>
            </template>
        </Column>
        <template #expansion="slotProps">
            <div class="drawer">
                <div>
                    {{ $gettext("Bibliographic Sources") }}:
                    <ResourceInstanceRelationships
                        :value="
                            (slotProps.data as AppellativeStatus)
                                .appellative_status_data_assignment_object_used
                        "
                    ></ResourceInstanceRelationships>
                </div>
                <div>
                    {{ $gettext("Contributors") }}:
                    <ResourceInstanceRelationships
                        :value="
                            (slotProps.data as AppellativeStatus)
                                .appellative_status_data_assignment_actor
                        "
                    ></ResourceInstanceRelationships>
                </div>
            </div>
        </template>
    </DataTable>
</template>
<style scoped>
.controls {
    display: flex;
    flex-direction: row;
}
.controls button {
    margin: 0 0.5rem;
}
</style>
