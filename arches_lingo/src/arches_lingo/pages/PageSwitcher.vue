<script setup lang="ts">
import { provide, ref } from "vue";
import { useGettext } from "vue3-gettext";

import { useToast } from "primevue/usetoast";

import { fetchUser } from "@/arches_lingo/api.ts";
import {
    DEFAULT_ERROR_TOAST_LIFE,
    ERROR,
    userKey,
} from "@/arches_lingo/constants.ts";
import HomePage from "@/arches_lingo/pages/HomePage.vue";
import LoginPage from "@/arches_lingo/pages/login/LoginPage.vue";

import type { User } from "@/arches_lingo/types";

const { $gettext } = useGettext();
const toast = useToast();

const user = ref<User | null>(null);
const setUser = (userToSet: User | null) => {
    user.value = userToSet;
};
provide(userKey, { user, setUser });

try {
    setUser(await fetchUser());
} catch (error) {
    toast.add({
        severity: ERROR,
        life: DEFAULT_ERROR_TOAST_LIFE,
        summary: $gettext("Login required"), // most likely case is inactive user
        detail: error instanceof Error ? error.message : undefined,
    });
}
</script>

<template>
    <div style="font-family: sans-serif">
        <HomePage v-if="user && user.username !== 'anonymous'" />
        <LoginPage v-else />
    </div>
</template>
