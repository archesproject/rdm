import type { InjectionKey } from "vue";

import type { UserRefAndSetter } from "@/arches_lingo/types";
import HomePage from "@/arches_lingo/pages/home/HomePage.vue";
import LoginPage from "@/arches_lingo/pages/login/LoginPage.vue";
import BasicSearch from "@/arches_lingo/pages/search-basic/BasicSearch.vue";
import AdvancedSearch from "@/arches_lingo/pages/search-advanced/AdvancedSearch.vue";
import SchemeList from "@/arches_lingo/pages/scheme-list/SchemeList.vue";

export const ERROR = "error";
export const DEFAULT_ERROR_TOAST_LIFE = 8000;

export const userKey = Symbol() as InjectionKey<UserRefAndSetter>;

export const routes = [
    { path: "/", name: "root", component: HomePage },
    { path: "/login/:next?", name: "login", component: LoginPage },
    { path: "/search", name: "search", component: BasicSearch },
    {
        path: "/advanced-search",
        name: "advanced-search",
        component: AdvancedSearch,
    },
    { path: "/schemes", name: "schemes", component: SchemeList },
];

export const routeNames = {
    root: "root",
    login: "login",
    search: "search",
    advancedSearch: "advanced-search",
    schemes: "schemes",
};
