// creates a toast with some sensible defaults
export function defaultToast(variant: string, message: string) {
    return {
        message,
        duration: 5000,
        variant,
        rootClass: "toast-notification",
    };
}
