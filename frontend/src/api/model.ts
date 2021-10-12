import { AxiosError } from "axios";
import { deepCopy, valuesEqual } from "@/api/utils";

// here we have extracted out common functionality used for most API requests
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
