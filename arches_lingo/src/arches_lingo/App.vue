<script setup lang="ts">
import { provide, ref } from "vue";

import Toast from "primevue/toast";

import { userKey } from "@/arches_lingo/constants.ts";
import HomePage from "@/arches_lingo/pages/HomePage.vue";
import LoginPage from "@/arches_lingo/pages/login/LoginPage.vue";

import type { User } from "@/arches_lingo/types";

const user = ref<User | null>(null);
const setUser = (userToSet: User | null) => {
    user.value = userToSet;
};
provide(userKey, { user, setUser });
</script>

<template>
    <div style="font-family: sans-serif">
        <HomePage v-if="user" />
        <LoginPage v-else />
    </div>
    <Toast />
</template>
