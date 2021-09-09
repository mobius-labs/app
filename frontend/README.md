# Möbius Labs - Frontend

[view more documentation on Confluence](https://mobius-labs.atlassian.net/wiki/spaces/MLH/pages/13697105/Frontend+Documentation)

## Project setup

Most of these commands should work in either this `frontend`
folder or the root directory.

In the repo root is a stub `package.json`, whose sole purpose is to forward certain commands to this subdirectory, since e.g.: the Heroku Node.js buildpack requires a package.json in the root directory.

```
$ npm install
```

### Compiles and hot-reloads for development

```
$ npm run serve
```

### Compiles and minifies for production

```
$ npm run build
```

### Lints and fixes files

```
$ npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## Code quality

We have a three-pronged approach to code-quality on the frontend.

- TypeScript - better editor support, catch runtime type errors at compile time.
- ESLint - to catch more bugs, avoid common Vue pitfalls
- Prettier - for consistent code formatting

According to the frontend [GitHub Actions workflow](../.github/workflows/frontend.yml),
all PRs making changes to the frontend must pass the ESLint check,
and must match the formatting of Prettier, in order to be accepted.
Though this is quite a harsh rule, it should make it easier to
maintain code quality in the long run.

## Editors & tooling

Recommended editors (same as for the backend):

- PyCharm Professional Edition and the Vue.js extension,
- VS Code with the [Vetur](https://vuejs.github.io/vetur/) extension.

There is a Chrome/Firefox extension which lets you debug a Vue.js application more easily:
https://devtools.vuejs.org/guide/installation.html#settings

You can also setup PyCharm / VS Code / other editor with ESLint integration, so that errors and warnings appear while editing:
https://eslint.vuejs.org/user-guide/#editor-integrations
