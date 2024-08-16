<script setup lang="ts">
import { ref } from "vue";

import Button from "primevue/button";

import { routeNames } from "@/arches_lingo/routes.ts";

const items = ref([
    {
        icon: "fa fa-home",
        name: routeNames.root,
    },
    {
        icon: "fa fa-search",
        name: routeNames.search,
    },
]);
</script>

<template>
    <aside class="sidenav">
        <div
            v-for="item in items"
            :key="item.name"
        >
            <RouterLink :to="{ name: item.name }">
                <Button>
                    <i :class="item.icon"></i>
                </Button>
            </RouterLink>
        </div>
    </aside>
</template>

<style scoped>
.sidenav {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 3rem;
    border-right: 1px solid var(--p-menubar-border-color);
}

.p-button {
    min-height: 3rem;
    min-width: 3rem;
    border-radius: 0;
    font-size: 1.5rem;
}

@media screen and (max-width: 960px) {
    .sidenav {
        display: none;
    }
}
</style>
