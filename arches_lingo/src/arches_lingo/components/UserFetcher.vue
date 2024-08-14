<script setup lang="ts">
import { inject, ref } from "vue";
import { useGettext } from "vue3-gettext";

import { useToast } from "primevue/usetoast";

import { fetchUser } from "@/arches_lingo/api.ts";
import {
    DEFAULT_ERROR_TOAST_LIFE,
    ERROR,
    userKey,
} from "@/arches_lingo/constants.ts";

const { $gettext } = useGettext();
const toast = useToast();

const { setUser } = inject(userKey, {
    user: ref(null),
    setUser: () => {},
});

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
    <div role="presentation"></div>
</template>
