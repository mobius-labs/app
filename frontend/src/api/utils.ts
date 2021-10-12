// sometimes due to Vue's reactivity rules, we need a completely fresh copy of an object.
export function deepCopy<T>(x: T): T {
    return JSON.parse(JSON.stringify(x));
}

// ensures `func` is only called max once every `timeout` milliseconds
export function debounce(this: any, func: any, timeout = 200) {
    let timer: number;
    return (...args: any[]) => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            func.apply(this, args);
        }, timeout);
    };
}

// `setTimeout`, except as a promise
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

// from MDN docs:
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions#escaping
export function escapeRegExp(s: string) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); // $& means the whole matched string
}

export function convertToTitleCase(str: string) {
    return str.replace(/\w\S*/g, function (txt: string) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}
