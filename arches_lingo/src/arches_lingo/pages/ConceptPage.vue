<script setup lang="ts">
import { inject } from "vue";

import { displayedRowKey } from "@/arches_lingo/constants.ts";

import type { DisplayedRowRefAndSetter } from "@/arches_lingo/types";

const { displayedRow } = inject(
    displayedRowKey,
) as unknown as DisplayedRowRefAndSetter;
</script>

<template>
    <pre style="text-wrap: auto">{{ displayedRow }}</pre>
</template>
