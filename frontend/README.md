# Möbius Labs - Frontend

[view documentation on Confluence](https://mobius-labs.atlassian.net/wiki/spaces/MLH/pages/13697105/Frontend+Documentation)

## Code quality

We have a three-pronged approach to code-quality on the frontend.

- TypeScript - better editor support, catch runtime type errors at compile time.
- ESLint - to catch more bugs, avoid common Vue pitfalls
- Prettier - for consistent code formatting

Read here to set up your editor with ESLint integration:
https://eslint.vuejs.org/user-guide/#editor-integrations

## Project setup

Most of these commands should work in either this `frontend`
folder or the root directory.

In the repo root is a stub `package.json`, whose sole purpose is to forward certain commands to this subdirectory, since e.g.: the Heroku Node.js buildpack requires a package.json in the root directory.

```
$ npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).
