<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { fetchSchemeResource } from "@/arches_lingo/api.ts";
import type { SchemeResource } from "@/arches_lingo/types.ts";
import SchemeSection from "@/arches_lingo/components/detail/SchemeSection.vue";

const route = useRoute();
const schemeResource = ref<SchemeResource | null>(null);

onMounted(async () => {
    const resource = (await fetchSchemeResource(
        route.params.id,
    )) as SchemeResource;
    schemeResource.value = resource;
});
</script>

<template>
    <div v-if="schemeResource">
        <div
            v-for="(section, resourceKey) in schemeResource.resource"
            :key="resourceKey"
        >
            <SchemeSection
                :section="section"
                :resource-key="resourceKey"
            />
        </div>
    </div>
</template>
