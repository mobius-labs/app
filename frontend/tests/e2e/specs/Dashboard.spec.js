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
    });

    it("Presents overdue catch-ups", () => {
        cy.get(".catchup").should("exist");
        cy.get(".mb-3 > .subtitle").should("contain.text", "Contact Four");
        cy.wait(1000);
        cy.get("button.button > :nth-child(1) > span").should(
            "contain.text",
            "We've caught up since!"
        );
    });

    it("Presents upcoming catch-ups", () => {
        cy.get(
            ":nth-child(2) > .o-clps__content > .card-content > :nth-child(1) > .catchup"
        ).should("exist");
        cy.get(
            ":nth-child(2) > .o-clps__content > .card-content > :nth-child(1) > .catchup > .level-left > div > .mb-3 > .subtitle"
        ).should("contain.text", "Contact Two");
    });

    it("Presents upcoming important dates", () => {
        cy.get(
            ":nth-child(3) > .o-clps__content > .card-content > :nth-child(1) > .notification"
        ).should("exist");
        cy.get(".level-left > div > .subtitle").should(
            "contain.text",
            "It's Contact One's birthday on 30 October 2021"
        );
    });
});
