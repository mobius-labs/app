import {
    createRouter,
    createWebHistory,
    RouteLocationNormalized,
} from "vue-router";

import { getAxiosInstance } from "@/api/api";
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
import OnboardLayout from "../views/OnboardLayout.vue";

import { nextTick } from "vue";
import store from "@/store";
import BusinessCardView from "../views/BusinessCardView.vue";
import ScanCard from "@/views/ScanCard.vue";

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
        meta: {
            title: "View Business Card",
            allowGuests: true,
        },
        props: (route: RouteLocationNormalized) => {
            return { email: route.params.email };
        },
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
        path: "/onboard",
        name: "Onboard",
        component: OnboardLayout,
        meta: { title: "Onboard", allowNotOnboarded: true },
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
                path: "contacts/:id?",
                component: Contacts,
                meta: { title: "Contacts" },
                props: (route: RouteLocationNormalized) => {
                    if (route.query.initialData) {
                        return {
                            selectedId: Contacts.NEW_CONTACT,
                            initialData: JSON.parse(
                                route.query.initialData as string
                            ),
                        };
                    }
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
                meta: { title: "eBusiness Card", darkMode: true },
            },
            {
                path: "scan-card",
                component: ScanCard,
                meta: { title: "Scan Business Card" },
            },
        ],
    },
    { path: "/:pathMatch(.*)*", name: "not-found", component: PageNotFound },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

const APP_TITLE = "Möbius";

router.beforeEach((to, from, next) => {
    store.dispatch("determineAuthStatus").then(async (authenticated) => {
        if (!authenticated && to.meta.allowGuests !== true) {
            next({
                path: "/login",
            });
            return;
        }

        if (
            authenticated &&
            !to.meta.allowNotOnboarded &&
            !to.meta.allowGuests
        ) {
            // user is authenticated - check if they've onboarded
            try {
                await getAxiosInstance().get("contact_book/get_user_contacts");
            } catch (e) {
                if (e.response.status === 404) {
                    next({
                        path: "/onboard",
                    });
                    return;
                }
            }
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
