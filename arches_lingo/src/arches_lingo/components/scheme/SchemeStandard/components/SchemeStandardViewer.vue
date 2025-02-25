<script setup lang="ts">
import { inject } from "vue";
import { useGettext } from "vue3-gettext";

import Button from "primevue/button";

import ResourceInstanceMultiSelectWidget from "@/arches_component_lab/widgets/ResourceInstanceMultiSelectWidget/ResourceInstanceMultiSelectWidget.vue";
import { VIEW } from "@/arches_lingo/constants.ts";

import type { SchemeCreation } from "@/arches_lingo/types.ts";

const props = defineProps<{
    schemeCreation: SchemeCreation | undefined;
}>();

const { $gettext } = useGettext();

const openEditor = inject<(componentName: string) => void>("openEditor");
</script>

<template>
    <div
        style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 0.125rem solid var(--p-menubar-border-color);
        "
    >
        <h3>{{ $gettext("Scheme Standard") }}</h3>

        <div>
            <Button
                :label="$gettext('Add New Scheme Standard')"
                @click="openEditor!('SchemeStandard')"
            ></Button>
        </div>
    </div>
    <ResourceInstanceMultiSelectWidget
        graph-slug="scheme"
        node-alias="creation_sources"
        :initial-value="props.schemeCreation?.creation_sources"
        :mode="VIEW"
    />
</template>
