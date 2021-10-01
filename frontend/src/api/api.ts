import axios, { AxiosInstance, AxiosResponse } from "axios";

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

export function displayErrors(response: AxiosResponse, $oruga: any) {
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
