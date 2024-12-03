<script setup lang="ts">
import type { ControlledListItem } from "@/arches_lingo/types";
import ControlledListItemViewer from "@/arches_lingo/components/generic/ControlledListItemViewer.vue";
const VIEW = "view";
const EDIT = "edit";

type DataComponentMode = "edit" | "view";

const props = defineProps<{
    mode?: DataComponentMode;
    value?: ControlledListItem;
}>();
defineEmits(["update"]);
</script>
<template>
    <div>
        <div v-if="!props.mode || props.mode === VIEW">
            <ControlledListItemViewer :value="props.value" />
        </div>
        <div v-if="props.mode === EDIT"></div>
    </div>
</template>
