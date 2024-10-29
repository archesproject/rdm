<script setup lang="ts">
import type { Scheme } from "@/arches_lingo/types";

const { scheme } = defineProps<{ scheme: Scheme }>();
</script>

<template>
    <pre style="text-wrap: auto">{{ scheme }}</pre>
</template>
