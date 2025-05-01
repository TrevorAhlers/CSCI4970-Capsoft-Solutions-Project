describe('Login Form', () => {
  
  beforeEach(() => {
    // Visit the login page
    cy.visit('/login');
  });

  it('should display username and password fields', () => {
    // Check that the username and password input fields exist
    cy.get('input[formControlName="username"]').should('exist');
    cy.get('input[formControlName="password"]').should('exist');
  });

  it('should show validation error for empty fields', () => {
    // Check that the submit button is disabled when fields are empty
    cy.get('button[type="submit"]').should('be.disabled');
    

    // Ensure no validation errors are shown as the fields are empty
    cy.get('mat-error').should('not.exist');
  });

  it('should enable the submit button when valid data is entered', () => {
    // Fill in valid username and password
    cy.get('input[formControlName="username"]').type('tporter');
    cy.get('input[formControlName="password"]').type('csci4970');
    
    // Ensure the submit button is enabled
    cy.get('button[type="submit"]').should('not.be.disabled');
  });

  it('should allow user to submit form with valid data and redirect to home', () => {
    // Fill in valid username and password
    cy.get('input[formControlName="username"]').type('tporter');
    cy.get('input[formControlName="password"]').type('csci4970');
  
    // Submit the form
    cy.get('button[type="submit"]').click();

    cy.url({ timeout: 5000 }).should('include', '/home');

  
    //  Assert token is stored
    cy.window().then((win) => {
      expect(win.localStorage.getItem('jwt')).to.not.be.null;
    });
  });
  

  it('should remain on the login page with invalid credentials', () => {
    // Fill in invalid username and password
    cy.get('input[formControlName="username"]').type('wronguser');
    cy.get('input[formControlName="password"]').type('wrongPassword123');
    
    // Submit the form
    cy.get('button[type="submit"]').click();

    // Ensure the URL remains on the login page
    cy.url().should('include', '/login');
    
    // Ensure no JWT token is stored in localStorage
    cy.window().then((window) => {
      expect(window.localStorage.getItem('jwt')).to.be.null;
    });
  });

  it('should redirect to registration page when clicking on the registration link', () => {
    // Click the registration link
    cy.get('.registration_link').click();

    // Check if the URL changes to the registration page
    cy.url().should('include', '/registration');
  });
});
