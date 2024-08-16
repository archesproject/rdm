<script setup lang="ts">
import { ref } from "vue";
import { useGettext } from "vue3-gettext";

import Button from "primevue/button";
import Menubar from "primevue/menubar";

import { routeNames } from "@/arches_lingo/routes.ts";
import UserInteraction from "@/arches_lingo/components/user/UserInteraction.vue";

const { $gettext } = useGettext();

const items = ref([
    {
        label: $gettext("Search"),
        icon: "fa fa-search",
        name: routeNames.search,
    },
    {
        label: $gettext("Advanced Search"),
        icon: "fa fa-file",
        name: routeNames.advancedSearch,
    },
]);
</script>

<template>
    <Menubar
        :model="items"
        style="height: 3rem"
    >
        <template #start>
            <RouterLink
                class="router-link"
                :to="{ name: routeNames.root }"
                style="text-decoration: none; color: inherit"
            >
                <h2>{{ $gettext("Arches Lingo") }}</h2>
            </RouterLink>
        </template>
        <template #item="{ item }">
            <RouterLink
                class="router-link"
                :to="{ name: item.name }"
            >
                <Button v-ripple>
                    <i :class="item.icon"></i>
                    <span>{{ item.label }}</span>
                </Button>
            </RouterLink>
        </template>
        <template #end>
            <UserInteraction />
        </template>
    </Menubar>
</template>

<style scoped></style>
