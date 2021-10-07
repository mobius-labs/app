// we need some way of persisting our token after the user closes their tab, otherwise they would
// need to login every single time they open a tab.

// for now, we use localStorage to do this, though note that
// this can be vulnerable to XSS attacks.
// see: https://auth0.com/docs/security/data-security/token-storage#browser-local-storage-scenarios

const LOCAL_STORAGE_KEY = "mobius-api";

export const persistToken = (token: string) => {
    localStorage.setItem(LOCAL_STORAGE_KEY, token);
};

export const invalidateToken = () => {
    localStorage.setItem(LOCAL_STORAGE_KEY, "");
};

export const getToken = (): string | null => {
    return localStorage.getItem(LOCAL_STORAGE_KEY);
};
