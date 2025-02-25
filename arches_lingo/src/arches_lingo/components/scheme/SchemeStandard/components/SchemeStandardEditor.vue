<script setup lang="ts">
import { useGettext } from "vue3-gettext";

import ResourceInstanceMultiSelectWidget from "@/arches_component_lab/widgets/ResourceInstanceMultiSelectWidget/ResourceInstanceMultiSelectWidget.vue";

import { EDIT } from "@/arches_lingo/constants.ts";

import type { SchemeCreation } from "@/arches_lingo/types.ts";

const { $gettext } = useGettext();

const props = defineProps<{
    schemeCreation: SchemeCreation | undefined;
}>();
</script>

<template>
    <h4>{{ $gettext("Scheme Standard") }}</h4>

    <ResourceInstanceMultiSelectWidget
        graph-slug="scheme"
        node-alias="creation_sources"
        :initial-value="props.schemeCreation?.creation_sources"
        :mode="EDIT"
    />
</template>
