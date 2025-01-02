<script setup lang="ts">
import type {
    ControlledListItem,
    DataComponentMode,
} from "@/arches_lingo/types";
import ReferenceDatatypeViewer from "@/arches_lingo/components/generic/reference-datatype/ReferenceDatatypeViewer.vue";
import ReferenceDatatypeEditor from "@/arches_lingo/components/generic/reference-datatype/ReferenceDatatypeEditor.vue";
import { EDIT, VIEW } from "@/arches_lingo/constants.ts";

defineProps<{
    mode?: DataComponentMode;
    value?: ControlledListItem[];
    multiValue?: boolean;
    options?: ControlledListItem[];
}>();
const emits = defineEmits(["update"]);
const onUpdate = (val: ControlledListItem[]) => {
    emits("update", val);
};
</script>
<template>
    <div>
        <div v-if="mode === VIEW">
            <ReferenceDatatypeViewer :value="value" />
        </div>
        <div v-if="mode === EDIT">
            <ReferenceDatatypeEditor
                :value="value"
                :options="options"
                :multi-value="multiValue"
                @update="onUpdate"
            />
        </div>
    </div>
</template>
