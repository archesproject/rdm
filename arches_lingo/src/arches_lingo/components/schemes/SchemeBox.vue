<script setup lang="ts">
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
</script>

<template>
    <div>
        <p>{{ scheme.descriptors.en.name }}</p>
        <p>{{ scheme.descriptors.en.description }}</p>
    </div>
</template>
