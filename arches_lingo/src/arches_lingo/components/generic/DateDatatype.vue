<script setup lang="ts">
import DateDatatypeViewer from "@/arches_lingo/components/generic/date-datatype/DateDatatypeViewer.vue";
import DateDatatypeEditor from "@/arches_lingo/components/generic/date-datatype/DateDatatypeEditor.vue";

import { EDIT, VIEW } from "@/arches_lingo/constants.ts";

import type { DataComponentMode } from "@/arches_lingo/types.ts";

const { mode = VIEW } = defineProps<{
    mode?: DataComponentMode;
    value?: string;
}>();

const emits = defineEmits(["update"]);

const onUpdate = (val: string) => {
    emits("update", val);
};
</script>

<template>
    <div>
        <div v-if="mode === VIEW">
            <DateDatatypeViewer :value="value" />
        </div>
        <div v-if="mode === EDIT">
            <DateDatatypeEditor
                :value="value"
                @update="onUpdate"
            />
        </div>
    </div>
</template>
