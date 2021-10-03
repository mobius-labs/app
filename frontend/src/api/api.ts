import axios, { AxiosError, AxiosInstance } from "axios";
import Oruga from "@oruga-ui/oruga-next";

let instance: AxiosInstance | null = null;
let $oruga: typeof Oruga | null = null;

export const useOrugaInstance = (oruga: typeof Oruga) => {
    $oruga = oruga;
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

    fromValidationError(e: AxiosError, model: Record<string, any>) {
        this.model = JSON.parse(JSON.stringify(model));
        if (e.response && e.response.data.errors) {
            this.errors = e.response.data.errors;
        } else if (e.response && e.response.status === 400) {
            // TODO: the "login" route doesn't nest all errors inside some "errors" object,
            //       so instead we need to look inside the global object
            this.errors = {};
            for (const [field, errors] of Object.entries(e.response.data)) {
                if (field !== "non_field_errors") {
                    this.errors[field] = errors as string[];
                } else {
                    for (let error of errors as string[]) {
                        $oruga.notification.open({
                            duration: 5000,
                            message: error,
                            position: "top-right",
                            variant: "danger",
                            closable: true,
                        });
                    }
                }
            }
        }
    }
}
