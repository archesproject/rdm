<script setup lang="ts">
import { onMounted, ref } from "vue";
import SchemeCard from "@/arches_lingo/components/scheme/SchemeCard.vue";
import { fetchSchemes } from "@/arches_lingo/api.ts";

import type { SchemeDescriptor } from "@/arches_lingo/types";

const schemes = ref<SchemeDescriptor[]>([]);

onMounted(async () => {
    schemes.value = await fetchSchemes();
});
</script>

<template>
    <Suspense>
        <div>
            <ul
                style="
                    display: flex;
                    flex-wrap: wrap;
                    list-style-type: none;
                    padding: 0;
                "
            >
                <!-- Create New Scheme -->
                <li
                    class="scheme-card"
                    style="text-align: center"
                >
                    Placeholder for creating new scheme
                </li>
                <!-- Existing Schemes -->
                <li
                    v-for="scheme in schemes"
                    :key="scheme.resourceinstanceid"
                    class="scheme-card"
                >
                    <SchemeCard :scheme="scheme" />
                </li>
            </ul>
        </div>
    </Suspense>
</template>

<style scoped>
.scheme-card {
    margin: 0.5rem;
    padding: 1rem;
    border: 0.0625rem solid var(--p-menubar-border-color);
    min-width: 300px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: var(--p-primary-400);
}
</style>
