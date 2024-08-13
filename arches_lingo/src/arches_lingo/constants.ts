import type { InjectionKey } from "vue";

import type { UserRefAndSetter } from "@/arches_lingo/types";

export const ERROR = "error";
export const DEFAULT_ERROR_TOAST_LIFE = 8000;

export const userKey = Symbol() as InjectionKey<UserRefAndSetter>;

export const routes = [
    {
        path: "/",
        name: "root",
        component: () => import("@/arches_lingo/pages/home/HomePage.vue"),
    },
    {
        path: "/login/:next?",
        name: "login",
        component: () => import("@/arches_lingo/pages/login/LoginPage.vue"),
    },
    {
        path: "/search",
        name: "search",
        component: () =>
            import("@/arches_lingo/pages/search-basic/BasicSearch.vue"),
    },
    {
        path: "/advanced-search",
        name: "advanced-search",
        component: () =>
            import("@/arches_lingo/pages/search-advanced/AdvancedSearch.vue"),
    },
    {
        path: "/schemes",
        name: "schemes",
        component: () =>
            import("@/arches_lingo/pages/scheme-list/SchemeList.vue"),
    },
];

export const routeNames = {
    root: "root",
    login: "login",
    search: "search",
    advancedSearch: "advanced-search",
    schemes: "schemes",
};
