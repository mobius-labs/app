import { createStore } from "vuex";
import {
    getToken,
    invalidateToken,
    persistToken,
} from "@/store/tokenPersistence";

// to understand Vuex, read up here: https://vuex.vuejs.org/

// declare your own store states
export interface State {
    authToken: string | null;
}

const store = createStore({
    state: {
        authToken: null,
    },
    mutations: {
        setToken(state, token) {
            state.authToken = token;
        },
    },
    actions: {
        determineAuthStatus({ state, commit }) {
            if (state.authToken !== null) {
                return true;
            }
            const token = getToken();
            if (token) {
                commit("setToken", token);
                return true;
            }
            return false;
        },
        async login({ commit }, { token, router, oruga, isSignUp }) {
            commit("setToken", token);
            console.log("redirecting...");
            persistToken(token);
            if (isSignUp) {
                // TODO: get rid of this, and add logic to beforeEach() hook to check onboard status
                await router.push("/onboard");
                oruga.notification.open({
                    message: "Yay!",
                    variant: "link",
                    rootClass: "toast-notification",
                    duration: 5000,
                });
            } else {
                await router.push("/app");
                oruga.notification.open({
                    message: "Welcome!",
                    variant: "link",
                    rootClass: "toast-notification",
                    duration: 5000,
                });
            }
        },
        async logout({ commit }, { router, oruga }) {
            commit("setToken", null);
            console.log("logged out");
            await router.push("/");
            invalidateToken();
            oruga.notification.open({
                message: "You are now logged out.",
                variant: "info",
                rootClass: "toast-notification",
                duration: 5000,
            });
        },
    },
    modules: {},
});

export default store;
