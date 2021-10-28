describe("Access Account integration tests", () => {
    beforeEach(() => {
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

        cy.get(":nth-child(2) > a").click();

        cy.url().should("include", "/contacts");
    });

    it("Can add contact", () => {
        cy.wait(500);
        cy.get(".is-primary > :nth-child(1) > :nth-child(2)").click();

        cy.get('[placeholder="First Name"][expanded=""] > .control > .input')
            .type("Contact")
            .should("have.value", "Contact");

        cy.get('[placeholder="Surname"][expanded=""] > .control > .input')
            .type("One")
            .should("have.value", "One");

        cy.get(
            ":nth-child(4) > [data-test=title] > [data-test=add-button]"
        ).click();
        cy.get('[placeholder="Type"] > .control > select').select("Friend");
        cy.get(
            '[placeholder="e.g.: johndoe@gmail.com"][data-v-698bee05=""] > .control > .input'
        )
            .type("contact1@gmail.com")
            .should("have.value", "contact1@gmail.com");

        cy.get(".icon-container").click();

        cy.get(".o-notices--top > .is-info").should("exist");

        cy.get("[data-test=close-button]").click();
    });

    it("Can delete contact", () => {
        cy.wait(500);

        cy.get(
            ':nth-child(1) > [data-label="Actions"] > .buttons > .is-info'
        ).click();
        cy.get(".o-notices--top > .is-info").should("exist");
    });

    it("Can edit contact", () => {
        cy.wait(500);

        cy.get(
            ':nth-child(1) > [data-label="Actions"] > .buttons > .is-warning'
        ).click();

        cy.wait(1000);

        cy.get(
            ":nth-child(4) > [data-test=title] > [data-test=add-button]"
        ).click();
        cy.get(
            ':nth-child(3) > [placeholder="Type"] > .control > [data-test=select_email]'
        ).select("Friend");
        cy.get(
            ':nth-child(3) > [placeholder="e.g.: johndoe@gmail.com"][data-v-96dc8b3e=""] > .control > [data-test=input_email]'
        )
            .clear()
            .type("homie@gmail.com")
            .should("have.value", "homie@gmail.com");

        cy.get(".is-size-7").should("exist");

        cy.wait(1000);

        cy.get(".has-text-primary > :nth-child(1)").should("exist");

        cy.wait(1000);

        cy.get("[data-test=close-button]").click();

        cy.wait(1000);

        cy.get('[data-label="Phone Nos. & Emails"] > :nth-child(2)').should(
            "exist"
        );
    });

    it("Can search for contacts", () => {
        cy.wait(500);

        cy.get(".input")
            .type("Contact Four")
            .should("have.value", "Contact Four");

        cy.wait(1000);

        cy.get(".buttons > .is-warning").click();

        cy.get(
            '[placeholder="First Name"][expanded=""] > .control > .input'
        ).should("have.value", "Contact");

        cy.get(
            '[placeholder="Surname"][expanded=""] > .control > .input'
        ).should("have.value", "Four");

        cy.get("[data-test=close-button]").click();
    });

    it.only("Can add date of last catchup", () => {
        cy.wait(500);

        cy.get(
            ':nth-child(1) > [data-label="Actions"] > .buttons > .is-warning'
        ).click();

        cy.wait(1000);

        cy.get(".dropdown-trigger > .control > .input").click();

        cy.get(".datepicker-body > :nth-child(2) > :nth-child(5)").click();

        cy.wait(1000);

        cy.get(":nth-child(14) > .control > select").select("Weekly");

        cy.wait(1000);

        cy.get("[data-test=close-button]").click();
    });
});
