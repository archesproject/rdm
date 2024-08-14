export const routes = [
    {
        path: "/",
        name: "root",
        component: () => import("@/arches_lingo/pages/HomePage.vue"),
    },
    {
        path: "/login/:next?",
        name: "login",
        component: () => import("@/arches_lingo/pages/LoginPage.vue"),
    },
    {
        path: "/search",
        name: "search",
        component: () => import("@/arches_lingo/pages/BasicSearch.vue"),
    },
    {
        path: "/advanced-search",
        name: "advanced-search",
        component: () => import("@/arches_lingo/pages/AdvancedSearch.vue"),
    },
    {
        path: "/schemes",
        name: "schemes",
        component: () => import("@/arches_lingo/pages/SchemeList.vue"),
    },
];

export const routeNames = {
    root: "root",
    login: "login",
    search: "search",
    advancedSearch: "advanced-search",
    schemes: "schemes",
};
