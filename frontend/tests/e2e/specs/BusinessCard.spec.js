describe("Dashboard integration tests", () => {
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

        cy.get(":nth-child(4) > li > a").click();

        cy.url().should("include", "/business-card");
    });

    it("Shows personal business card", () => {
        cy.get(".bc").should("exist");

        cy.get(".bc-name-title > .subtitle").should("contain.text", "Test");
    });

    it.only("Can edit business card", () => {
        cy.get(".edit-button > :nth-child(1)").click();

        cy.get('[placeholder="Surname"][expanded=""] > .control > .input')
            .clear()
            .type("User")
            .should("have.value", "User");

        cy.get(
            ":nth-child(6) > [data-test=title] > [data-test=add-button]"
        ).click();

        cy.get(
            ':nth-child(2) > [placeholder="Type"] > .control > [data-test=select_email]'
        ).select("Business");

        cy.get(
            ':nth-child(2) > [placeholder="e.g.: johndoe@gmail.com"][data-v-96dc8b3e=""] > .control > [data-test=input_email]'
        )
            .clear()
            .type("test7343@gmail.com")
            .should("have.value", "test7343@gmail.com");

        cy.get(".is-size-7").should("contain.text", "Updated");

        cy.get(".has-text-primary > :nth-child(1)").should(
            "contain.text",
            "Saved contact"
        );

        cy.wait(1000);

        cy.get("[data-test=close-button]").click();

        cy.get(".bc-name-title > .subtitle").should(
            "contain.text",
            "Test User"
        );

        cy.get(".bc-item > a").should("contain.text", "test7343@gmail.com");
    });
});
