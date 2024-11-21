<script setup lang="ts">
import type {
    ControlledListItem,
    DataComponentMode,
} from "@/arches_lingo/types";
import ControlledListItemViewer from "@/arches_lingo/components/generic/ControlledListItemViewer.vue";
import { EDIT, VIEW } from "@/arches_lingo/constants.ts";

const { mode = EDIT } = defineProps<{
    mode?: DataComponentMode;
    value?: ControlledListItem;
}>();
defineEmits(["update"]);
</script>
<template>
    <div>
        <div v-if="mode === VIEW">
            <ControlledListItemViewer :value="value" />
        </div>
        <div v-if="mode === EDIT"></div>
    </div>
</template>
