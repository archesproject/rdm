<script setup lang="ts">
import { ref } from "vue";

import HomePage from "@/components/HomePage.vue";
import LoginPage from "@/components/LoginPage.vue";

const isAuthenticated = ref(false);
</script>

<template>
    <link
        rel="stylesheet"
        href="https://unpkg.com/primevue/resources/themes/mdc-light-indigo/theme.css"
    >
    <component
        :is="isAuthenticated ? HomePage : LoginPage"
        v-model="isAuthenticated"
    />
</template>
