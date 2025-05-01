describe('Home Page Flow', () => {
  it('logs in and views the home page', () => {
    cy.visit('/login');

    cy.intercept('POST', '/api/login').as('loginRequest');

    cy.get('input[formControlName="username"]').type('tporter');
    cy.get('input[formControlName="password"]').type('csci4970');
    cy.get('button[type="submit"]').click();

    cy.wait('@loginRequest'); // Wait for the API to finish
    cy.url().should('include', '/home');


    cy.get('app-profile h1.header').should('contain.text', 'tporter');


    //  Upload file
    // Replace the selector with the actual <input type="file"> selector
    cy.get('input[type="file"]').selectFile('cypress/fixtures/uploads/Spring2023 conflict.csv');

    //  Confirm upload success by checking for list view (after upload switches view)
    cy.get('app-section-view', { timeout: 5000 }).should('exist');

    //  Verify rows are populated after the upload
    cy.get('app-section-view app-section-row').should('have.length.greaterThan', 0);

    //  Interact with the first row in the list view (using the 'row-hover' class)
    cy.get('app-section-view .row-hover').first().click({ force: true });

    //  Check that the app-details pane is populated
    cy.get('app-details').should('exist');
    

  });
});
