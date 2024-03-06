<script setup lang="ts">
import { ref } from "vue";

import HomePage from "@/components/HomePage.vue";
import LoginPage from "@/components/LoginPage.vue";

const isAuthenticated = ref(false);
</script>

<template>
    <component
        :is="isAuthenticated ? HomePage : LoginPage"
        :v-model:is-authenticated="isAuthenticated"
    />
</template>
