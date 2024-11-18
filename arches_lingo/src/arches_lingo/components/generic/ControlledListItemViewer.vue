<script setup lang="ts">
import type { ControlledListItem } from "@/arches_lingo/types";

const props = defineProps<{ value?: ControlledListItem }>();
</script>
<template>
    <p>{{ props.value?.labels }}</p>
</template>
