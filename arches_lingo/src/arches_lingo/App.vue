<script setup lang="ts">
import Toast from "primevue/toast";

import ProgressSpinner from "primevue/progressspinner";

import PageSwitcher from "@/arches_lingo/pages/PageSwitcher.vue";
</script>

<template>
    <Suspense>
        <PageSwitcher />
        <template #fallback>
            <ProgressSpinner style="display: flex; margin-top: 8rem" />
        </template>
    </Suspense>
    <Toast />
</template>
