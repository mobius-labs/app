module.exports = {
    extends: [
        "eslint:recommended",
        "plugin:vue/vue3-recommended",
        // make ESLint not conflict with Prettier config
        "prettier",
        "prettier/vue",
    ],
    rules: {
        // this doesn't work well with Typescript higher-order functions
        "no-unused-vars": "off",
    },
    // gets rid of warnings about undefined `module` and `process` globals
    env: {
        browser: true,
        amd: true,
        node: true,
        jest: true,
    },
    // gets rid of errors parsing Typescript
    parserOptions: {
        parser: "@typescript-eslint/parser",
    },
};
