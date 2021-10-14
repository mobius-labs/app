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
                console.log("Retrieved token from local storage");
                commit("setToken", token);
                return true;
            }
            return false;
        },
        async login({ commit }, { token, router, oruga }) {
            commit("setToken", token);
            persistToken(token);
            console.log("redirecting...");
            await router.push("/app");
            oruga.notification.open({
                message: "Welcome!",
                variant: "success",
                rootClass: "toast-notification",
                duration: 5000,
            });
        },
        async logout(
            { commit },
            { router, oruga, logoutMessage, redirectURL }
        ) {
            commit("setToken", null);
            invalidateToken();
            console.log("logged out");
            await router.push(redirectURL || "/");
            oruga.notification.open({
                message: logoutMessage || "You are now logged out.",
                variant: "info",
                rootClass: "toast-notification",
                duration: 5000,
            });
        },
    },
    modules: {},
});

export default store;
