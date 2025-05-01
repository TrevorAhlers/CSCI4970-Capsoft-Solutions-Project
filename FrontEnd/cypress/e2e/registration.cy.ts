describe('Registration Page', () => {
  beforeEach(() => {
    // Visit the login page URL first
    cy.visit('/login'); // Ensure this matches the actual login route
  });

  it('should navigate to the registration page when clicking on "Don\'t have an account?"', () => {
    // Click the "Don't have an account?" link to go to the registration page
    cy.contains('Don\'t have an account?').click();
    
    // Verify that the URL changes to the registration page
    cy.url().should('include', '/registration');
  });

  it('should display the registration form on the registration page', () => {
    // Go to registration page by clicking on the link after visiting login page
    cy.contains('Don\'t have an account?').click();

    // Check if form elements are visible
    cy.get('mat-card-title').contains('Create Account'); // Check if the title is visible
    cy.get('input[formControlName="username"]').should('be.visible');
    cy.get('input[formControlName="email"]').should('be.visible');
    cy.get('input[formControlName="password"]').should('be.visible');
    cy.get('input[formControlName="confirm_password"]').should('be.visible');
    cy.get('button[type="submit"]').should('be.visible').and('be.disabled'); // Submit button should be disabled initially
  });

  it('should enable submit button when form is valid', () => {
    // Navigate to the registration page first
    cy.contains('Don\'t have an account?').click();

    // Fill in the form with valid data
    cy.get('input[formControlName="username"]').type('testuser');
    cy.get('input[formControlName="email"]').type('testuser@example.com');
    cy.get('input[formControlName="password"]').type('Password123');
    cy.get('input[formControlName="confirm_password"]').type('Password123');
  
    // Check if submit button is enabled
    cy.get('button[type="submit"]').should('not.be.disabled');
  });

  it('should remain disabled if password and confirm password do not match', () => {
    // Navigate to the registration page first
    cy.contains('Don\'t have an account?').click();
    
    // Fill in the form with mismatched passwords
    cy.get('input[formControlName="username"]').type('testuser');
    cy.get('input[formControlName="email"]').type('testuser@example.com');
    cy.get('input[formControlName="password"]').type('Password123');
    cy.get('input[formControlName="confirm_password"]').type('DifferentPassword123');
  
    // Ensure the submit button remains disabled (because passwords do not match)
    cy.get('button[type="submit"]').should('be.disabled');
  });

  it('should call the backend API and register the user successfully', () => {
    // Navigate to the registration page first
    cy.contains('Don\'t have an account?').click();
  
    // Fill in the form with valid data
    cy.get('input[formControlName="username"]').type('testuser');
    cy.get('input[formControlName="email"]').type('testuser@example.com');
    cy.get('input[formControlName="password"]').type('Password123');
    cy.get('input[formControlName="confirm_password"]').type('Password123');
  
    // Mock the backend API response for successful registration
    cy.intercept('POST', '/api/register', {
      statusCode: 200,
      body: { message: 'Registration successful' }
    }).as('registerUser');
  
    // Submit the form
    cy.get('button[type="submit"]').click();
  
    // Wait for the registration API call
    cy.wait('@registerUser');
  
    // Verify that the user is redirected to the login page
    cy.url().should('include', '/login');
  });
});
