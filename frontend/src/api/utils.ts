export function deepCopy<T>(x: T): T {
    return JSON.parse(JSON.stringify(x));
}

export function debounce(this: any, func: any, timeout = 200) {
    let timer: number;
    return (...args: any[]) => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            func.apply(this, args);
        }, timeout);
    };
}

export async function delay(ms: number) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(undefined);
        }, ms);
    });
}

// from: https://stackoverflow.com/questions/30476150/javascript-deep-comparison-recursively-objects-and-properties
// simplified since we only really care about simple values like strings, numbers
export function valuesEqual(a: any, b: any): boolean {
    // If a and b reference the same value, return true
    if (a === b) return true;

    // Otherwise they're Objects, Functions or Arrays or some kind of host object
    if (typeof a == "object" || typeof a == "function") {
        let aKeys = Object.keys(a);
        let bKeys = Object.keys(b);

        // If they don't have the same number of keys, return false
        if (aKeys.length != bKeys.length) {
            return false;
        }

        // Check they have the same keys
        if (
            !aKeys.every(function (key) {
                return Object.prototype.hasOwnProperty.call(b, key);
            })
        ) {
            return false;
        }

        // Check key values - uses ES5 Object.keys
        return aKeys.every(function (key) {
            return valuesEqual(a[key], b[key]);
        });
    }

    return false;
}
