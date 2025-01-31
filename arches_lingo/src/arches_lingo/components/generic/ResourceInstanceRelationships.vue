<script setup lang="ts">
import ResourceInstanceRelationshipsViewer from "@/arches_lingo/components/generic/resource-instance-relationships/ResourceInstanceRelationshipsViewer.vue";
import ResourceInstanceRelationshipsEditor from "@/arches_lingo/components/generic/resource-instance-relationships/ResourceInstanceRelationshipsEditor.vue";
import { EDIT, VIEW } from "@/arches_lingo/constants.ts";
import type {
    DataComponentMode,
    ResourceInstanceReference,
} from "@/arches_lingo/types";

const { mode = VIEW } = defineProps<{
    mode?: DataComponentMode;
    value?: ResourceInstanceReference[];
    options?: ResourceInstanceReference[];
    ptAriaLabeledBy?: string;
}>();

const emits = defineEmits(["update"]);

function onUpdate(val: string[]) {
    emits("update", val);
}
</script>
<template>
    <div v-if="mode === VIEW">
        <ResourceInstanceRelationshipsViewer :value="value" />
    </div>
    <div v-if="mode === EDIT">
        <ResourceInstanceRelationshipsEditor
            :options="options"
            :val="
                value?.map((referenceValue) => referenceValue.resourceId) ?? []
            "
            :pt-aria-labeled-by="ptAriaLabeledBy"
            @update="onUpdate"
        />
    </div>
</template>
