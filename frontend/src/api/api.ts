import axios, { AxiosError, AxiosInstance } from "axios";
import Oruga from "@oruga-ui/oruga-next";
import { Store } from "vuex";
import { State } from "@/store";
import { deepCopy, valuesEqual } from "@/api/utils";

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
                            duration: 5000,
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
export class Model<T = Record<string, any>> {
    model: T;

    // the server's current copy of this model
    lastSavedModel: T;

    // the last version we submitted to the server
    // (it may have been rejected if it didn't pass validation)
    lastSubmittedModel: T;

    // validation errors returned by the API call, grouped by field name
    errors: Record<string, string[]> = {};

    nonFieldErrors: string[] = [];

    isSubmitting: boolean = false;

    constructor(model: T) {
        this.model = deepCopy(model);
        this.lastSavedModel = model;
        this.lastSubmittedModel = model;
    }

    hasErrors(): boolean {
        if (this.nonFieldErrors.length > 0) {
            return true;
        }
        for (const [, errors] of Object.entries(this.errors)) {
            if (errors) {
                return true;
            }
        }
        return false;
    }

    hasErrorsForField<Key extends keyof T>(fieldName: Key): boolean {
        if (this.isSubmittedValueStale(fieldName)) {
            return false;
        }
        return !!this.errors[fieldName as string];
    }

    isSubmittedValueStale<Key extends keyof T>(fieldName: Key) {
        return this.lastSubmittedModel[fieldName] !== this.model[fieldName];
    }

    displayFirstError<Key extends keyof T>(fieldName: Key) {
        if (this.isSubmittedValueStale(fieldName)) {
            return null;
        }
        let errors = this.errors[fieldName as string];
        if (errors && errors.length > 0) {
            return errors[0];
        }
        return null;
    }

    matchesServer() {
        console.log(
            JSON.stringify(this.lastSavedModel),
            JSON.stringify(this.model)
        );
        return valuesEqual(this.lastSavedModel, this.model);
    }

    captureServerResponse(model: T | null, e?: AxiosError) {
        this.lastSubmittedModel = model ?? deepCopy(this.model);

        this.errors = {};
        this.nonFieldErrors = [];

        if (!e) {
            this.lastSavedModel = model ?? deepCopy(this.model);
            if (model !== null) {
                for (const [key, value] of Object.entries(model)) {
                    this.model[key as keyof T] = value;
                }
            }
            return;
        }
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
        for (const [field, messages] of Object.entries(errors)) {
            if (field !== "non_field_errors") {
                this.errors[field] = messages as string[];
            } else {
                this.nonFieldErrors = messages as string[];
            }
        }
    }

    async tryUpdate(request: () => Promise<void>) {
        this.isSubmitting = true;

        try {
            await request();
        } catch (e) {
            this.captureServerResponse(null, e);
        }

        this.isSubmitting = false;
    }
}
