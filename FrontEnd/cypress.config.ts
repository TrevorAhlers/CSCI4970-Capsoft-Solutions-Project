import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:4200',  // Your frontend URL
    supportFile: false,  // Disables the support file
    env: {
      apiBaseUrl: 'http://localhost:5000'
    }
  }
});


