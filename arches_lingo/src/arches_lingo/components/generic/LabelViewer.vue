<script setup lang="ts">
import { ref } from "vue";
import { useGettext } from "vue3-gettext";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import ConfirmDialog from "primevue/confirmdialog";
import { useConfirm } from "primevue/useconfirm";

import type { AppellativeStatus } from "@/arches_lingo/types";

const { $gettext } = useGettext();
const expandedRows = ref([]);
const confirm = useConfirm();

const props = defineProps<{
    labels?: object[];
}>();

const emits = defineEmits(["editLabel", "deleteLabel"]);

function confirmDelete(tileId: string) {
    confirm.require({
        header: $gettext("Confirmation"),
        message: $gettext("Are you sure you want to delete this label?"),
        accept: () => {
            emits("deleteLabel", tileId);
        },
        rejectProps: {
            label: $gettext("Cancel"),
            severity: "secondary",
            outlined: true,
        },
        acceptProps: {
            label: $gettext("Delete"),
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
        :value="props.labels"
        table-style="min-width: 50rem"
    >
        <Column
            expander
            style="width: 3rem"
        />
        <Column
            :header="$gettext('Label')"
            sortable
        >
            <template #body="slotProps">
                <slot
                    name="name"
                    :row-data="slotProps.data"
                ></slot>
            </template>
        </Column>
        <Column
            :header="$gettext('Label Type')"
            sortable
        >
            <template #body="slotProps">
                <slot
                    name="type"
                    :row-data="slotProps.data"
                ></slot>
            </template>
        </Column>
        <Column
            :header="$gettext('Label Language')"
            sortable
        >
            <template #body="slotProps">
                <slot
                    name="language"
                    :row-data="slotProps.data"
                ></slot>
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
                <slot
                    name="drawer"
                    :row-data="slotProps.data"
                ></slot>
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
