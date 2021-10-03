import axios, { AxiosInstance, AxiosResponse } from "axios";
import Oruga from "@oruga-ui/oruga-next";

let instance: AxiosInstance | null = null;

export const getInstance = () => {
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
    }

    return instance;
};

// used for most API requests
export class ServerData {
    // form data which was sent to the server
    model: Record<string, any> = {};

    // validation errors returned by the API call, grouped by field name
    errors: Record<string, string[]> = {};
}

export function displayErrors(response: AxiosResponse, $oruga: typeof Oruga) {
    console.log(response.data.errors);
    for (const [field, errors] of Object.entries(response.data.errors)) {
        for (let error of errors as string[]) {
            $oruga.notification.open({
                duration: 5000,
                message: field + ": " + error,
                position: "top-right",
                variant: "danger",
                closable: true,
            });
        }
    }
}
