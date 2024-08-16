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

const { user, setUser } = inject(userKey, {
    user: ref(null),
    setUser: () => {},
});

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
    <div style="display: flex; align-items: center;">
        <span>{{ $gettext("Hello %{bestName}", { bestName }) }}</span>
        <Button style="margin-left: 1rem;" @click="issueLogout">
            {{ $gettext("Sign out") }}
        </Button>
    </div>
</template>
