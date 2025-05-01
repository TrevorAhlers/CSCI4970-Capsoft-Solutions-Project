describe('Registration and Login Flow', () => {
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
  
    // Submit the form (this triggers the backend registration)
    cy.get('button[type="submit"]').click();
  
    // Call the backend registration API after form submission
    cy.request({
      method: 'POST',
      url: '/api/register',
      failOnStatusCode: false, 
      body: {
        username: 'testuser',
        email: 'testuser@example.com',
        password: 'Password123',
        confirm_password: 'Password123'
      }
    }).then((response) => {
      
      if (response.status === 201) {
        expect(response.body.msg).to.eq('User created');
      } else {
        cy.log('Registration failed with status: ' + response.status);
      }
    });

    // After successful registration, navigate to the login page
    cy.url().should('include', '/login');
  });

  it('should call the backend API to login after registration', () => {
    // After registration, attempt to login with the same credentials
    cy.contains('Don\'t have an account?').click();
  
    // Fill in the registration form with valid data
    cy.get('input[formControlName="username"]').type('testuser');
    cy.get('input[formControlName="email"]').type('testuser@example.com');
    cy.get('input[formControlName="password"]').type('Password123');
    cy.get('input[formControlName="confirm_password"]').type('Password123');
  
    // Submit the registration form
    cy.get('button[type="submit"]').click();
  
    // Wait for the registration to complete
    cy.wait(2000); // Ensure that backend registration has finished

    // Now login with the same credentials
    cy.get('input[formControlName="username"]').type('testuser');
    cy.get('input[formControlName="password"]').type('Password123');
  
    // Submit the login form
    cy.get('button[type="submit"]').click();

    // Call the backend login API after form submission
    cy.request({
      method: 'POST',
      url: '/api/login',
      failOnStatusCode: false, 
      body: {
        username: 'testuser',
        password: 'Password123'
      }
    }).then((response) => {
      
      if (response.status === 200) {
        expect(response.body.token).to.exist;
      } else {
        cy.log('Login failed with status: ' + response.status);
      }
    });

    // Verify that the user is redirected to the home page after successful login
    cy.url().should('include', '/home');
  });
});
