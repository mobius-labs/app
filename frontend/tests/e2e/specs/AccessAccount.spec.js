// https://docs.cypress.io/api/introduction/api.html

describe("Access Account integration tests", () => {
    it("Visits the app root url", () => {
        cy.visit("/");
        cy.contains("p", "möbius crm.");
    });

    it("Lets non-user sign up to Mobius", () => {
        cy.visit("/");

        cy.get(".has-text-centered > .button")
            .contains("Get Connected")
            .click();
        cy.url().should("include", "/signup");

        cy.get(":nth-child(3) > .control > .input")
            .type("test7342@gmail.com")
            .should("have.value", "test7342@gmail.com");

        cy.get(":nth-child(4) > .control > .input")
            .type("test123")
            .should("have.value", "test123");

        cy.get(":nth-child(5) > .control > .input")
            .type("test123")
            .should("have.value", "test123");

        cy.get(".icon-container").click();

        cy.url().should("include", "/onboard");

        cy.get(".nav-buttons > :nth-child(2)").click();

        cy.get(
            '[placeholder="Your first name"][data-v-57b12f5a=""] > .control > .input'
        ).type("Test");
        cy.get(
            '[placeholder="Your surname"][data-v-57b12f5a=""] > .control > .input'
        ).type("User");
        cy.get(".nav-buttons > :nth-child(2)").click();

        cy.get(".nav-buttons > :nth-child(2)").click();

        cy.get(".icon-container").click();

        cy.url().should("include", "/app");
    });

    it.only("Lets user log in with credentials", () => {
        cy.visit("/");

        cy.get(".is-warning").click();
        cy.url().should("include", "/login");

        cy.get('[icon="envelope"] > .control > .input')
            .type("test7343@gmail.com")
            .should("have.value", "test7343@gmail.com");

        cy.get(":nth-child(4) > .control > .input")
            .type("test123")
            .should("have.value", "test123");

        cy.get(".icon-container").click();

        cy.url().should("include", "/app");
    });
});
