<script setup lang="ts">
import { routeNames } from "@/arches_lingo/routes.ts";

// TODO: Shift into types.ts
interface Scheme {
    resourceinstanceid: string;
    descriptors: {
        [key: string]: {
            name: string;
            description: string;
        };
    };
}

const { scheme } = defineProps<{ scheme: Scheme }>();
const schemeURL = {
    name: routeNames.scheme,
    params: { id: scheme.resourceinstanceid },
};
</script>

<template>
    <div>
        <RouterLink :to="schemeURL">
            <p>{{ scheme.descriptors.en.name }}</p>
        </RouterLink>
        <p>{{ scheme.descriptors.en.description }}</p>
    </div>
</template>
