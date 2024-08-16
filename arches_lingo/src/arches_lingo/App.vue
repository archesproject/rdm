<script setup lang="ts">
import { computed, provide, ref } from "vue";
import { useRouter, useRoute } from "vue-router";

import ProgressSpinner from "primevue/progressspinner";
import Toast from "primevue/toast";

import { userKey } from "@/arches_lingo/constants.ts";
import { routeNames } from "@/arches_lingo/routes.ts";
import UserFetcher from "@/arches_lingo/components/UserFetcher.vue";

import type { User } from "@/arches_lingo/types";

import PageHeader from "@/arches_lingo/components/header/PageHeader.vue";

const user = ref<User | null>(null);
const setUser = (userToSet: User | null) => {
    user.value = userToSet;
};
provide(userKey, { user, setUser });

const router = useRouter();
const route = useRoute();

const isAuthenticated = computed(() => {
    return user.value && user.value.username !== "anonymous";
});

router.beforeEach(async (to) => {
    if (
        !isAuthenticated.value &&
        // Avoid an infinite redirect
        to.name !== routeNames.login
    ) {
        return { name: routeNames.login, params: { next: to.name as string } };
    }
});
</script>

<template>
    <main style="font-family: sans-serif; height: 100vh;">
        <PageHeader v-if="route.meta.shouldShowHeader" />
        <div style="margin: 1rem;">
            <RouterView />
        </div>
    </main>
    <Suspense>
        <UserFetcher />
        <template #fallback>
            <ProgressSpinner style="display: flex; margin-top: 8rem" />
        </template>
    </Suspense>
    <Toast />
</template>
