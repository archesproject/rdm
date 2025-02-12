<script setup lang="ts">
import type { ControlledListItem } from "@/arches_lingo/types";

withDefaults(
    defineProps<{
        value?: ControlledListItem[] | ControlledListItem;
    }>(),
    {
        value: () => [],
    },
);
</script>
<template>
    <span v-if="value instanceof Array">
        <span
            v-for="val in value"
            :key="val.list_item_id"
        >
            <span>{{ val.display_value }}</span>
        </span>
    </span>
    <span v-else-if="value">
        <span>{{ value.display_value }}</span>
    </span>
    <span v-else>
        <span>{{ $gettext("None") }}</span>
    </span>
</template>
