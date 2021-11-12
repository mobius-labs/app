# Code Quality

[[back to README]](../README.md)

## Frontend

We have a five-pronged approach to code-quality on the frontend.

- _TypeScript_ - better editor support, catch runtime type errors at compile time.
- _ESLint_ - to catch more bugs, avoid common Vue pitfalls
- _Prettier_ - for consistent code formatting
- _Unit tests_ - to test individual Vue components and classes
- _E2E tests (Cypress)_ - to confirm the overall application flow

According to the frontend [GitHub Actions workflow](../.github/workflows/frontend.yml),
all PRs making changes to the frontend must pass the ESLint check,
and match the formatting of Prettier, and pass unit tests in order to be accepted.
Though this is quite a harsh rule, it should make it easier to
maintain code quality in the long run.
