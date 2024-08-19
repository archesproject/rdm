export const routes = [
    {
        path: "/",
        name: "root",
        component: () => import("@/arches_lingo/pages/HomePage.vue"),
        meta: {
            shouldShowNavigation: true,
            requiresAuth: true,
        },
    },
    {
        path: "/login/:next?",
        name: "login",
        component: () => import("@/arches_lingo/pages/LoginPage.vue"),
        meta: {
            shouldShowNavigation: false,
            requiresAuth: false,
        },
    },
    {
        path: "/search",
        name: "search",
        component: () => import("@/arches_lingo/pages/BasicSearch.vue"),
        meta: {
            shouldShowNavigation: true,
            requiresAuth: true,
        },
    },
    {
        path: "/advanced-search",
        name: "advanced-search",
        component: () => import("@/arches_lingo/pages/AdvancedSearch.vue"),
        meta: {
            shouldShowNavigation: true,
            requiresAuth: true,
        },
    },
    {
        path: "/schemes",
        name: "schemes",
        component: () => import("@/arches_lingo/pages/SchemeList.vue"),
        meta: {
            shouldShowNavigation: true,
            requiresAuth: true,
        },
    },
];

export const routeNames = {
    root: "root",
    login: "login",
    search: "search",
    advancedSearch: "advanced-search",
    schemes: "schemes",
};
