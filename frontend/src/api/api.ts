import axios, { AxiosError, AxiosInstance } from "axios";
import Oruga from "@oruga-ui/oruga-next";
import { Store } from "vuex";
import { State } from "@/store";

// TODO: figure out a better solution to these global vars
let instance: AxiosInstance | null = null;
let $oruga: typeof Oruga | null = null;
let vuexStore: Store<State> | null = null;

export const setOrugaInstance = (oruga: typeof Oruga) => {
    $oruga = oruga;
};

export const setStore = (store: Store<State>) => {
    vuexStore = store;
};

export const getAxiosInstance = () => {
    // Set config defaults when creating the instance
    if (instance === null) {
        // we default to the base API URL being the same host
        // as the frontend is running on
        let baseURL = "/api";
        if (parseInt(window.location.port) > 8000) {
            // for local development, Django should run on port 8000
            baseURL = "http://localhost:8000" + baseURL;
        }
        instance = axios.create({
            baseURL: baseURL,
        });

        // we pass the 'Authorization' header if needed
        instance.interceptors.request.use(
            (config) => {
                if (vuexStore !== null && vuexStore.state.authToken !== null) {
                    config.headers[
                        "Authorization"
                    ] = `Token ${vuexStore.state.authToken}`;
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
                    if ($oruga !== null) {
                        $oruga.notification.open({
                            message: "Network Error: failed to make API call",
                            variant: "danger",
                            indefinite: true,
                            closable: true,
                        });
                    }
                }
                return Promise.reject(error);
            }
        );
    }

    return instance;
};

// used for most API requests
export class ServerData {
    // form data which was sent to the server
    model: Record<string, any> = {};

    // validation errors returned by the API call, grouped by field name
    errors: Record<string, string[]> = {};

    nonFieldErrors: string[] = [];

    fromValidationError(e: AxiosError, model: Record<string, any>) {
        this.model = JSON.parse(JSON.stringify(model));
        let errors = null;
        if (e.response && e.response.data.errors) {
            errors = e.response.data.errors;
        } else if (e.response && e.response.status === 400) {
            // TODO: the "login" route doesn't nest all errors inside some "errors" object,
            //       so instead we need to look inside the global object
            errors = e.response.data;
        }

        if (errors === null) {
            return;
        }
        this.errors = {};
        this.nonFieldErrors = [];
        for (const [field, messages] of Object.entries(errors)) {
            if (field !== "non_field_errors") {
                this.errors[field] = messages as string[];
            } else {
                this.nonFieldErrors = messages as string[];
            }
        }
    }
}
