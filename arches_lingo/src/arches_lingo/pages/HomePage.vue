<script setup lang="ts">
import { computed, inject, ref } from "vue";
import { useRouter } from "vue-router";
import { useGettext } from "vue3-gettext";

import { useToast } from "primevue/usetoast";
import Button from "primevue/button";

import { logout } from "@/arches_lingo/api.ts";
import {
    DEFAULT_ERROR_TOAST_LIFE,
    ERROR,
    userKey,
} from "@/arches_lingo/constants.ts";
import { routeNames } from "@/arches_lingo/routes.ts";

import type { UserRefAndSetter } from "@/arches_lingo/types";

const { user, setUser } = inject(userKey, {
    user: ref(null),
    setUser: () => {},
}) as UserRefAndSetter;

const { $gettext } = useGettext();
const toast = useToast();
const router = useRouter();

const issueLogout = async () => {
    try {
        await logout();
        setUser(null);
        router.push({ name: routeNames.login });
    } catch (error) {
        toast.add({
            severity: ERROR,
            life: DEFAULT_ERROR_TOAST_LIFE,
            summary: $gettext("Sign out failed."),
            detail: error instanceof Error ? error.message : undefined,
        });
    }
};

const bestName = computed(() => {
    if (!user.value) {
        return "";
    }
    // TODO: determine appropriate i18n for this.
    if (user.value.first_name && user.value.last_name) {
        return user.value.first_name + " " + user.value.last_name;
    }
    return user.value.username;
});
</script>

<template>
    <div style="display: flex; justify-content: space-between">
        <h1>{{ $gettext("LINGO") }}</h1>
        <span>{{ $gettext("Hello %{bestName}", { bestName }) }}</span>
        <Button @click="issueLogout">
            {{ $gettext("Sign out") }}
        </Button>
    </div>
    <nav>
        <RouterLink :to="{ name: routeNames.root }">
            {{ $gettext("Go to Root") }}
        </RouterLink>
        <br />
        <RouterLink :to="{ name: routeNames.schemes }">
            {{ $gettext("Go to Schemes") }}
        </RouterLink>
        <br />
        <RouterLink :to="{ name: routeNames.search }">
            {{ $gettext("Go to Search") }}
        </RouterLink>
        <br />
        <RouterLink :to="{ name: routeNames.advancedSearch }">
            {{ $gettext("Go to Advanced Search") }}
        </RouterLink>
    </nav>
</template>
