import axios, { AxiosInstance } from "axios";
import Oruga from "@oruga-ui/oruga-next";
import { Store } from "vuex";
import { State } from "@/store";
import { Router } from "vue-router";

// TODO: figure out a better solution to these global vars
let instance: AxiosInstance | null = null;
let orugaInstance: typeof Oruga | null = null;
let vuexStore: Store<State> | null = null;
let routerInstance: Router | null = null;

const BASE_URL = "/api";

export const setOrugaInstance = (oruga: typeof Oruga) => {
    orugaInstance = oruga;
};

export const setRouterInstance = (router: Router) => {
    routerInstance = router;
};

export const setStore = (store: Store<State>) => {
    vuexStore = store;
};

// returns the base URL which should be used for all API calls
export function getBaseURL() {
    // we default to the base API URL being the same host
    // as the frontend is running on
    let baseURL = BASE_URL;
    if (parseInt(window.location.port) > 8000) {
        // for local development, Django should be running on port 8000,
        // whereas the frontend (`npm run serve`) is running on a higher port
        baseURL = "http://localhost:8000" + BASE_URL;
    }
    return baseURL;
}

export const getAxiosInstance = () => {
    // Set config defaults when creating the instance
    if (instance === null) {
        instance = axios.create({
            baseURL: getBaseURL(),
        });

        // we pass the 'Authorization' header if needed
        instance.interceptors.request.use(
            (config) => {
                if (vuexStore !== null && vuexStore.state.authToken !== null) {
                    if (config.headers) {
                        config.headers.Authorization = `Token ${vuexStore.state.authToken}`;
                    }
                }
                return config;
            },
            (error) => Promise.reject(error)
        );

        // here we set up some common error handling for all API calls...
        instance.interceptors.response.use(
            (r) => r,
            (error) => {
                if (!error.response) {
                    console.warn(
                        "No response from API, potential network error"
                    );
                    if (orugaInstance !== null) {
                        orugaInstance.notification.open({
                            message: "Network Error: failed to make API call",
                            variant: "danger",
                            duration: 5000,
                            closable: true,
                        });
                    }
                }
                if (
                    error.response &&
                    error.response.status === 401 &&
                    error.response.data &&
                    error.response.data.detail === "Invalid token."
                ) {
                    console.warn(
                        "Authentication failed, redirecting to login page"
                    );
                    if (
                        routerInstance !== null &&
                        orugaInstance !== null &&
                        vuexStore !== null
                    ) {
                        vuexStore.dispatch("logout", {
                            router: routerInstance,
                            oruga: orugaInstance,
                            logoutMessage: "You need to login again.",
                            redirectURL: "/login",
                        });
                    }
                }
                return Promise.reject(error);
            }
        );
    }

    return instance;
};

export interface ListResponse<T> {
    count: number;
    previous: string | null;
    next: string | null;
    results: T[];
}
