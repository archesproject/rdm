<script setup lang="ts">
import { inject } from "vue";
import { systemLanguageKey } from "@/arches_lingo/constants.ts";
import { routeNames } from "@/arches_lingo/routes.ts";

import type { Language } from "@/arches_vue_utils/types";
import type { SchemeResource, ResourceDescriptor } from "@/arches_lingo/types";

const systemLanguage = inject(systemLanguageKey) as Language;

const { scheme } = defineProps<{ scheme: SchemeResource }>();
const schemeURL = {
    name: routeNames.scheme,
    params: { id: scheme.resourceinstanceid },
};

const descriptors = scheme.descriptors;
let schemeDescriptor: ResourceDescriptor = {
    name: "",
    description: "",
};
if (descriptors) {
    const descriptor =
        descriptors[systemLanguage.code] ?? Object.values(descriptors)[0];
    schemeDescriptor.name = descriptor.name ?? "";
    schemeDescriptor.description = descriptor.description ?? "";
}
</script>

<template>
    <RouterLink
        :to="schemeURL"
        class="scheme-card"
    >
        <p>{{ schemeDescriptor.name }}</p>
        <p>{{ schemeDescriptor.description }}</p>
    </RouterLink>
</template>

<style scoped>
p {
    text-align: center;
}
.scheme-card {
    text-decoration: none;
    color: var(--p-text-color);
    width: 15rem;
    height: 15rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: 0.5rem;
    border: 1px solid var(--p-menubar-border-color);
    background-color: var(--p-primary-400);
}
.scheme-card:hover {
    background-color: var(--p-button-primary-hover-background);
    cursor: pointer;
}
</style>
