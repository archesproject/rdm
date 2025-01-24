<script setup lang="ts">
import ResourceInstanceRelationshipsViewer from "@/arches_lingo/components/generic/resource-instance-relationships/ResourceInstanceRelationshipsViewer.vue";
import ResourceInstanceRelationshipsEditor from "@/arches_lingo/components/generic/resource-instance-relationships/ResourceInstanceRelationshipsEditor.vue";
import { EDIT, UPDATED, VIEW } from "@/arches_lingo/constants.ts";
import type {
    DataComponentMode,
    ResourceInstanceReference,
} from "@/arches_lingo/types";

const { mode = VIEW } = defineProps<{
    mode?: DataComponentMode;
    value?: ResourceInstanceReference[];
    graphSlug?: string;
    nodeAlias?: string;
    ptAriaLabeledBy?: string;
}>();

const emit = defineEmits([UPDATED]);

function onUpdate(val: ResourceInstanceReference[]) {
    emit(UPDATED, val);
}
</script>
<template>
    <div v-if="mode === VIEW">
        <ResourceInstanceRelationshipsViewer :value="value" />
    </div>
    <div v-if="mode === EDIT && graphSlug && nodeAlias">
        <ResourceInstanceRelationshipsEditor
            :val="
                value?.map((referenceValue) => referenceValue.resourceId) ?? []
            "
            :pt-aria-labeled-by="ptAriaLabeledBy"
            :graph-slug="graphSlug"
            :node-alias="nodeAlias"
            @updated="onUpdate"
        />
    </div>
</template>
