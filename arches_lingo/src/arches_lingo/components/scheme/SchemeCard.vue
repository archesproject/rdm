<script setup lang="ts">
import { inject } from "vue";
import { getDescriptors } from "@/arches_vue_utils/utils.ts";
import { systemLanguageKey } from "@/arches_lingo/constants.ts";
import { routeNames } from "@/arches_lingo/routes.ts";

import type { Language } from "@/arches_vue_utils/types";
import type { SchemeDescriptor } from "@/arches_lingo/types";

const systemLanguage = inject(systemLanguageKey) as Language;

const { scheme } = defineProps<{ scheme: SchemeDescriptor }>();
const schemeURL = {
    name: routeNames.scheme,
    params: { id: scheme.resourceinstanceid },
};
const [schemeName, schemeDescription] = getDescriptors(
    scheme.descriptors,
    systemLanguage.code,
);
</script>

<template>
    <RouterLink
        :to="schemeURL"
        class="existing-scheme-card {"
    >
        <p>{{ schemeName }}</p>
        <p>{{ schemeDescription }}</p>
    </RouterLink>
</template>

<style scoped>
.existing-scheme-card {
    text-decoration: none;
    color: var(--p-text-color);
    width: inherit;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
</style>
