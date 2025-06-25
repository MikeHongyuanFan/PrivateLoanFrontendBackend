/**
 * API Test Utility
 * 
 * This file contains utility functions to test API endpoints
 * and help debug any issues with the borrower and guarantor APIs.
 */

import { api } from '@/api';

/**
 * Test borrower API endpoints
 */
export const testBorrowerAPI = async () => {
  console.log('Testing Borrower API endpoints...');
  
  try {
    // Test getting borrowers list
    console.log('Testing GET /api/borrowers/borrowers/');
    const [borrowersErr, borrowersRes] = await api.borrowers();
    if (borrowersErr) {
      console.error('Error getting borrowers:', borrowersErr);
    } else {
      console.log('Borrowers list retrieved successfully:', borrowersRes);
    }
    
    // Test creating a borrower
    console.log('Testing POST /api/borrowers/borrowers/');
    const testBorrowerData = {
      first_name: 'Test',
      last_name: 'Borrower',
      email: 'test.borrower@example.com',
      phone: '1234567890',
      date_of_birth: '1990-01-01',
      employment_type: 'full_time'
    };
    
    const [createErr, createRes] = await api.addBorrowers(testBorrowerData);
    if (createErr) {
      console.error('Error creating borrower:', createErr);
    } else {
      console.log('Borrower created successfully:', createRes);
      
      // Test getting the created borrower
      if (createRes.id) {
        console.log(`Testing GET /api/borrowers/borrowers/${createRes.id}`);
        const [getErr, getRes] = await api.borrower(createRes.id);
        if (getErr) {
          console.error('Error getting borrower:', getErr);
        } else {
          console.log('Borrower retrieved successfully:', getRes);
        }
      }
    }
    
  } catch (error) {
    console.error('Exception in testBorrowerAPI:', error);
  }
};

/**
 * Test guarantor API endpoints
 */
export const testGuarantorAPI = async () => {
  console.log('Testing Guarantor API endpoints...');
  
  try {
    // Test getting guarantors list
    console.log('Testing GET /api/borrowers/guarantors/');
    const [guarantorsErr, guarantorsRes] = await api.getGuarantors();
    if (guarantorsErr) {
      console.error('Error getting guarantors:', guarantorsErr);
    } else {
      console.log('Guarantors list retrieved successfully:', guarantorsRes);
    }
    
    // Test creating a guarantor
    console.log('Testing POST /api/borrowers/guarantors/');
    const testGuarantorData = {
      guarantor_type: 'individual',
      first_name: 'Test',
      last_name: 'Guarantor',
      email: 'test.guarantor@example.com',
      phone: '0987654321',
      date_of_birth: '1980-01-01',
      employment_type: 'full_time'
    };
    
    const [createErr, createRes] = await api.createGuarantor(testGuarantorData);
    if (createErr) {
      console.error('Error creating guarantor:', createErr);
    } else {
      console.log('Guarantor created successfully:', createRes);
      
      // Test getting the created guarantor
      if (createRes.id) {
        console.log(`Testing GET /api/borrowers/guarantors/${createRes.id}`);
        const [getErr, getRes] = await api.getGuarantor(createRes.id);
        if (getErr) {
          console.error('Error getting guarantor:', getErr);
        } else {
          console.log('Guarantor retrieved successfully:', getRes);
        }
      }
    }
    
  } catch (error) {
    console.error('Exception in testGuarantorAPI:', error);
  }
};

/**
 * Test guarantor relationships
 */
export const testGuarantorRelationships = async () => {
  console.log('Testing Guarantor Relationships...');
  
  try {
    // First, get some borrowers and applications to test with
    const [borrowersError, borrowersResponse] = await api.borrowers();
    const [applicationsError, applicationsResponse] = await api.applications();
    
    if (borrowersError || applicationsError) {
      console.error('Error loading test data:', { borrowersError, applicationsError });
      return;
    }
    
    const testBorrower = borrowersResponse.results?.[0];
    const testApplication = applicationsResponse.results?.[0];
    
    if (!testBorrower || !testApplication) {
      console.log('No test data available for relationship testing');
      return;
    }
    
    console.log('Test data:', {
      borrower: { id: testBorrower.id, name: `${testBorrower.first_name} ${testBorrower.last_name}` },
      application: { id: testApplication.id, name: `Application #${testApplication.id}` }
    });
    
    // Test creating a guarantor with relationships
    console.log('Testing POST /api/borrowers/guarantors/ with relationships');
    const testGuarantorData = {
      guarantor_type: 'individual',
      first_name: 'Test',
      last_name: 'Guarantor',
      email: 'test.guarantor@example.com',
      phone: '0987654321',
      date_of_birth: '1980-01-01',
      employment_type: 'full_time',
      borrower: testBorrower.id,
      application: testApplication.id
    };
    
    const [createError, createResponse] = await api.createGuarantor(testGuarantorData);
    if (createError) {
      console.error('Error creating guarantor with relationships:', createError);
    } else {
      console.log('Guarantor with relationships created successfully:', createResponse);
      
      // Test getting the created guarantor to verify relationships
      if (createResponse.id) {
        console.log(`Testing GET /api/borrowers/guarantors/${createResponse.id}`);
        const [getError, getResponse] = await api.getGuarantor(createResponse.id);
        if (getError) {
          console.error('Error getting guarantor:', getError);
        } else {
          console.log('Guarantor retrieved successfully:', getResponse);
          console.log('Relationship fields:', {
            borrower: getResponse.borrower,
            application: getResponse.application
          });
        }
        
        // Test getting related borrowers
        console.log(`Testing GET /api/borrowers/guarantors/${createResponse.id}/borrowers/`);
        const [borrowerRelError, borrowerRelResponse] = await api.getGuarantorBorrowers(createResponse.id);
        if (borrowerRelError) {
          console.error('Error getting guarantor borrowers:', borrowerRelError);
        } else {
          console.log('Guarantor borrowers retrieved successfully:', borrowerRelResponse);
        }
        
        // Test getting related applications
        console.log(`Testing GET /api/borrowers/guarantors/${createResponse.id}/applications/`);
        const [appRelError, appRelResponse] = await api.getGuarantorApplications(createResponse.id);
        if (appRelError) {
          console.error('Error getting guarantor applications:', appRelError);
        } else {
          console.log('Guarantor applications retrieved successfully:', appRelResponse);
        }
      }
    }
    
  } catch (error) {
    console.error('Exception in testGuarantorRelationships:', error);
  }
};

/**
 * Run all API tests
 */
export const runAPITests = async () => {
  console.log('Starting API tests...');
  
  await testBorrowerAPI();
  await testGuarantorAPI();
  await testGuarantorRelationships();
  
  console.log('API tests completed.');
}; 