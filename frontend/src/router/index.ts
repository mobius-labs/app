import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import PageNotFound from "../views/PageNotFound.vue";
import AppLayout from "../views/AppLayout.vue";
import AppDashboard from "../views/AppDashboard.vue";
import Contacts from "../views/Contacts.vue";

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
    },
    {
        path: "/login",
        name: "Login",
        component: Login,
    },
    {
        path: "/app",
        name: "CRM",
        component: AppLayout,
        children: [
            {
                path: "",
                component: AppDashboard,
            },
            {
                path: "contacts",
                component: Contacts,
            },
        ],
    },
    {
        path: "/about",
        name: "About",
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import(/* webpackChunkName: "about" */ "../views/About.vue"),
    },
    { path: "/:pathMatch(.*)*", name: "not-found", component: PageNotFound },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
