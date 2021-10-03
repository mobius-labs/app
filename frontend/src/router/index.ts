import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import SignUp from "../views/SignUp.vue";
import PageNotFound from "../views/PageNotFound.vue";
import AppLayout from "../views/AppLayout.vue";
import AppDashboard from "../views/AppDashboard.vue";
import Contacts from "../views/Contacts.vue";
import ForgotPassword from "../views/ForgotPassword.vue";
import AuthLayout from "../views/AuthLayout.vue";
import { nextTick } from "vue";

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
        meta: { title: "Home" },
    },
    {
        path: "/",
        component: AuthLayout,
        children: [
            {
                path: "/login",
                name: "Login",
                component: Login,
                meta: { title: "Login" },
            },
            {
                path: "/signup",
                name: "SignUp",
                component: SignUp,
                meta: { title: "Sign up" },
            },
            {
                path: "/forgot",
                name: "Forgot",
                component: ForgotPassword,
                meta: { title: "Forgot password" },
            },
        ],
    },
    {
        path: "/app",
        name: "CRM",
        component: AppLayout,
        children: [
            {
                path: "",
                component: AppDashboard,
                meta: { title: "Dashboard" },
            },
            {
                path: "contacts",
                component: Contacts,
                meta: { title: "Contacts" },
            },
        ],
    },
    { path: "/:pathMatch(.*)*", name: "not-found", component: PageNotFound },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

const APP_TITLE = "Möbius CRM";
router.afterEach((to) => {
    // Use next tick to handle router history correctly
    // see: https://github.com/vuejs/vue-router/issues/914#issuecomment-384477609
    nextTick(() => {
        document.title = to.meta.title
            ? to.meta.title + " | " + APP_TITLE
            : APP_TITLE;
    });
});

export default router;
