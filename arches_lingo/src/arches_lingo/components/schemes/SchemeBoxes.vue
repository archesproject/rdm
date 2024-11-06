<script setup lang="ts">
import { fetchSchemes } from "@/arches_lingo/api.ts";

const schemes = await fetchSchemes();
</script>

<template>
    <div style="display: block">
        <!-- Creating New Scheme -->
        <div>
            <input
                type="text"
                placeholder="Enter Scheme Name"
            />
            <button>Create Scheme</button>
        </div>

        <!-- Existing Schemes -->
        <div>
            <ul>
                <li
                    v-for="scheme in schemes"
                    :key="scheme.id"
                >
                    {{ scheme.name }}
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped></style>
