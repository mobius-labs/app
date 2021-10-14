import {
    createRouter,
    createWebHistory,
    RouteLocationNormalized,
} from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import SignUp from "../views/SignUp.vue";
import PageNotFound from "../views/PageNotFound.vue";
import AppLayout from "../views/AppLayout.vue";
import AppDashboard from "../views/AppDashboard.vue";
import Contacts from "../views/Contacts.vue";
import ForgotPassword from "../views/ForgotPassword.vue";
import AuthLayout from "../views/AuthLayout.vue";
import BusinessCardEdit from "../views/BusinessCardEdit.vue";
import { nextTick } from "vue";
import store from "@/store";
import BusinessCardView from "../views/BusinessCardView.vue";

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
        meta: { title: "Home", allowGuests: true },
    },
    {
        path: "/card/:email",
        name: "View Business Card",
        component: BusinessCardView,
    },
    {
        path: "/",
        component: AuthLayout,
        children: [
            {
                path: "/login",
                name: "Login",
                component: Login,
                meta: { title: "Login", allowGuests: true },
            },
            {
                path: "/signup",
                name: "SignUp",
                component: SignUp,
                meta: { title: "Sign up", allowGuests: true },
            },
            {
                path: "/forgot",
                name: "Forgot",
                component: ForgotPassword,
                meta: { title: "Forgot password", allowGuests: true },
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
                meta: { title: "Dashboard", height: 1 },
            },
            {
                path: "contacts/:id?",
                component: Contacts,
                meta: { title: "Contacts", height: 2 },
                props: (route: RouteLocationNormalized) => {
                    if (route.params.id === "new") {
                        return { selectedId: Contacts.NEW_CONTACT };
                    }
                    return {
                        selectedId: !route.params.id
                            ? null
                            : Number.parseInt(route.params.id as string),
                    };
                },
            },
            {
                path: "business-card",
                component: BusinessCardEdit,
                meta: { title: "eBusiness Card", height: 3, darkMode: true },
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

router.afterEach((to, from) => {
    if (to.meta.height && from.meta.height) {
        to.meta.transitionName =
            (to.meta.height as number) > (from.meta.height as number)
                ? "slide-up"
                : "slide-down";
    }
});

router.beforeEach((to, from, next) => {
    store.dispatch("determineAuthStatus").then((authenticated) => {
        if (!authenticated && to.meta.allowGuests !== true) {
            next({
                path: "/login",
            });
            return;
        }
        next();
    });
});

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
