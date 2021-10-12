import { AxiosError } from "axios";
import { deepCopy, valuesEqual } from "@/api/utils";

// common functionality used for CRUD operations on a single struct of data (of type T)
export class Model<T = Record<string, any>> {
    // the state of the model the user is currently editing
    model: T;

    // the server's current copy of this model
    lastSavedModel: T;

    // the last version we submitted to the server
    // (it may have been rejected if it didn't pass validation)
    lastSubmittedModel: T;

    // validation errors returned by API calls, grouped by field name
    errors: Record<string, string[]> = {};

    // validation errors returned by API calls, which don't pertain to any specific field
    nonFieldErrors: string[] = [];

    // true if a request is currently in-flight
    isSubmitting: boolean = false;

    constructor(model: T) {
        this.model = deepCopy(model);
        this.lastSavedModel = model;
        this.lastSubmittedModel = model;
    }

    // true if there are validation errors
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

    // true if there are validation errors for a particular field
    hasErrorsForField<Key extends keyof T>(fieldName: Key): boolean {
        if (this.isSubmittedValueStale(fieldName)) {
            return false;
        }
        return !!this.errors[fieldName as string];
    }

    // true if the user has changed this field since last submitting
    isSubmittedValueStale<Key extends keyof T>(fieldName: Key) {
        return this.lastSubmittedModel[fieldName] !== this.model[fieldName];
    }

    // returns the first validation message for a particular field
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

    // true if there are no unsaved changes
    matchesServer(): boolean {
        console.log(
            JSON.stringify(this.lastSavedModel),
            JSON.stringify(this.model)
        );
        return valuesEqual(this.lastSavedModel, this.model);
    }

    // marks that `model` was submitted to the server, and optionally an error `e` was thrown
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

    // a convenience function to try and make an API call, handling errors appropriately.
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
