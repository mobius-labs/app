export function deepCopy<T>(x: T): T {
    return JSON.parse(JSON.stringify(x));
}
