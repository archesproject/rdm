<script setup lang="ts">
import SchemeBox from "@/arches_lingo/components/schemes/SchemeBox.vue";
import { fetchSchemes } from "@/arches_lingo/api.ts";

const schemes = await fetchSchemes();
</script>

<template>
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
                <SchemeBox :scheme="scheme" />
            </li>
        </ul>
    </div>
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
