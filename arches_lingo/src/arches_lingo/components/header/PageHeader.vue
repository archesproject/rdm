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
        class="page-header"
        :model="items"
    >
        <template #start>
            <RouterLink
                :to="{ name: routeNames.root }"
                style="text-decoration: none; color: inherit"
            >
                <h2>{{ $gettext("Arches Lingo") }}</h2>
            </RouterLink>
        </template>
        <template #item="{ item }">
            <RouterLink :to="{ name: item.name }">
                <Button>
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

<style scoped>
.page-header {
    border-radius: 0;
}

@media screen and (max-width: 960px) {
    :deep(.p-menubar-button) {
        display: none !important;
    }
}
</style>
