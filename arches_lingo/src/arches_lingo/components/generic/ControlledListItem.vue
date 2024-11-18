<script lang="ts">
const UPDATE = "update";
</script>
<script setup lang="ts">
import type { ControlledListItem } from "@/arches_lingo/types";
import ControlledListItemViewer from "@/arches_lingo/components/generic/ControlledListItemViewer.vue";

type DataComponentMode = "edit" | "view";
const props = defineProps<{
    mode?: DataComponentMode;
    value?: ControlledListItem;
}>();
defineEmits([UPDATE]);
</script>
<template>
    <div>
        <div v-if="!props.mode || props.mode === 'view'">
            <ControlledListItemViewer :value="props.value" />
        </div>
        <div v-if="props.mode === 'edit'"></div>
    </div>
</template>
