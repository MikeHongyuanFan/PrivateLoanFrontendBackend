/**
 * Utility functions to transform guarantor assets and liabilities from the frontend format to the backend format
 * 
 * UNIFIED DATA STRUCTURE:
 * - All assets (borrower, guarantor, company) are stored in the same Asset table
 * - All liabilities (borrower, guarantor, company) are stored in the same Liability table  
 * - The distinction is made through foreign key relationships (borrower_id vs guarantor_id)
 * - Context-aware validation is handled by the unified serializers
 * 
 * This transformer works with the unified backend structure and converts the frontend
 * form format to the proper unified Asset/Liability format for API submission.
 */

/**
 * Transforms guarantor assets from the frontend format to the backend format
 * @param {Object} guarantorAsset - The guarantor asset data from the frontend
 * @param {Array} guarantors - The guarantors array
 * @returns {Array} - Array of guarantors with properly formatted assets
 */
export function transformGuarantorAssets(guarantorAsset, guarantors) {
  console.log("transformGuarantorAssets called with:", { guarantorAsset, guarantors });
  
  if (!guarantorAsset || !guarantors || !Array.isArray(guarantors)) {
    console.log("Invalid input to transformGuarantorAssets");
    return guarantors;
  }

  // Create a deep copy of the guarantors array to avoid modifying the original
  const transformedGuarantors = JSON.parse(JSON.stringify(guarantors));
  
  // Process each guarantor to ensure borrower and application are properly formatted
  transformedGuarantors.forEach(guarantor => {
    // Clear existing assets and liabilities to ensure replacement, not addition
    guarantor.assets = [];
    guarantor.liabilities = [];
    
    // For new guarantors, set borrower and application to null
    // The backend will handle the assignment during creation
    guarantor.borrower = null;
    guarantor.application = null;
    
    // Remove any nested objects that might cause issues
    delete guarantor.borrower_details;
    delete guarantor.application_details;
  });

  // Map of asset types from frontend to backend schema
  const assetTypeMap = {
    'address': 'Property',
    'vehicle': 'Vehicle',
    'saving': 'Savings',
    'share': 'Investment Shares',
    'card': 'Credit Card',
    'creditor': 'Other Creditor',
    'other': 'Other'
  };

  // Process property assets (addresses)
  for (let i = 1; i <= 4; i++) {
    processAsset(
      guarantorAsset,
      transformedGuarantors,
      `address${i}`,
      `address${i}Value`,
      `address${i}Owing`,
      `address${i}G1`,
      `address${i}G2`,
      'Property',
      true // isProperty flag to include address field
    );
  }
  
  // Process other asset types
  Object.entries(assetTypeMap).forEach(([prefix, assetType]) => {
    if (prefix !== 'address') { // Skip addresses as they're handled separately
      processAsset(
        guarantorAsset,
        transformedGuarantors,
        prefix,
        `${prefix}Value`,
        `${prefix}Owing`,
        `${prefix}G1`,
        `${prefix}G2`,
        assetType
      );
    }
  });

  console.log("Transformed guarantors:", transformedGuarantors);
  return transformedGuarantors;
}

/**
 * Process an asset and add it to the appropriate guarantor(s)
 * @param {Object} guarantorAsset - The guarantor asset data
 * @param {Array} guarantors - The guarantors array
 * @param {String} descriptionKey - The key for the description value
 * @param {String} valueKey - The key for the value amount
 * @param {String} owingKey - The key for the amount owing
 * @param {String} g1Key - The key for the G1 flag
 * @param {String} g2Key - The key for the G2 flag
 * @param {String} assetType - The asset type for the backend
 * @param {Boolean} isProperty - Whether this is a property asset (includes address field)
 */
function processAsset(
  guarantorAsset,
  guarantors,
  descriptionKey,
  valueKey,
  owingKey,
  g1Key,
  g2Key,
  assetType,
  isProperty = false
) {
  console.log(`Processing asset: ${descriptionKey}, ${valueKey}, ${assetType}`);
  
  const description = guarantorAsset[descriptionKey] || '';
  const value = parseFloat(guarantorAsset[valueKey]) || 0;
  const amountOwing = parseFloat(guarantorAsset[owingKey]) || 0;
  const isG1 = guarantorAsset[g1Key];
  const isG2 = guarantorAsset[g2Key];
  
  console.log(`Asset values: description=${description}, value=${value}, owing=${amountOwing}, G1=${isG1}, G2=${isG2}`);
  
  // Skip if description is empty for properties, or if both G1 and G2 are false, or if value is 0
  if ((isProperty && !description) || (!isG1 && !isG2) || value === 0) {
    console.log(`Skipping asset: ${descriptionKey}`);
    return;
  }
  
  // Create asset object according to schema
  const asset = {
    asset_type: assetType,
    description: description || assetType,
    value: value.toString(),
    amount_owing: amountOwing.toString()
  };
  
  // Add address field for property assets
  if (isProperty && description) {
    asset.address = description;
  }
  
  console.log(`Created asset object:`, asset);
  
  // Add to appropriate guarantor(s)
  if (isG1 && guarantors.length >= 1) {
    guarantors[0].assets.push({
      ...asset,
      bg_type: 'BG1'
    });
    console.log(`Added asset to guarantor 1 with BG1`);
  }
  
  if (isG2 && guarantors.length >= 2) {
    guarantors[1].assets.push({
      ...asset,
      bg_type: 'BG2'
    });
    console.log(`Added asset to guarantor 2 with BG2`);
  } else if (isG2 && guarantors.length === 1) {
    // If G2 is selected but there's only one guarantor, add it to the first guarantor
    guarantors[0].assets.push({
      ...asset,
      bg_type: 'BG2'
    });
    console.log(`Added asset to guarantor 1 with BG2 (only one guarantor available)`);
  }
}

/**
 * Transforms guarantor assets from the backend format back to the frontend format for editing
 * @param {Array} guarantors - The guarantors array from backend with assets
 * @returns {Object} - Frontend format guarantor asset object
 */
export function reverseTransformGuarantorAssets(guarantors) {
  console.log("reverseTransformGuarantorAssets called with:", guarantors);
  
  if (!guarantors || !Array.isArray(guarantors) || guarantors.length === 0) {
    console.log("No guarantors to reverse transform");
    return createEmptyGuarantorAssetForm();
  }

  // Initialize empty frontend format
  const frontendAssets = createEmptyGuarantorAssetForm();
  
  // Process each guarantor's assets
  guarantors.forEach((guarantor, guarantorIndex) => {
    if (!guarantor.assets || !Array.isArray(guarantor.assets)) {
      return;
    }
    
    guarantor.assets.forEach(asset => {
      const bgType = asset.bg_type || 'BG1';
      const isG1 = bgType === 'BG1';
      const isG2 = bgType === 'BG2';
      
      // Map backend asset types to frontend format
      switch (asset.asset_type) {
        case 'Property':
          // Find next available address slot
          for (let i = 1; i <= 4; i++) {
            if (!frontendAssets[`address${i}`]) {
              frontendAssets[`address${i}`] = asset.description || asset.address || '';
              frontendAssets[`address${i}Value`] = asset.value || '';
              frontendAssets[`address${i}Owing`] = asset.amount_owing || '';
              frontendAssets[`address${i}G1`] = isG1;
              frontendAssets[`address${i}G2`] = isG2;
              break;
            }
          }
          break;
          
        case 'Vehicle':
          if (!frontendAssets.vehicleValue) {
            frontendAssets.vehicleValue = asset.value || '';
            frontendAssets.vehicleOwing = asset.amount_owing || '';
            frontendAssets.vehicleG1 = isG1;
            frontendAssets.vehicleG2 = isG2;
          }
          break;
          
        case 'Savings':
          if (!frontendAssets.savingValue) {
            frontendAssets.savingValue = asset.value || '';
            frontendAssets.savingOwing = asset.amount_owing || '';
            frontendAssets.savingG1 = isG1;
            frontendAssets.savingG2 = isG2;
          }
          break;
          
        case 'Investment Shares':
          if (!frontendAssets.shareValue) {
            frontendAssets.shareValue = asset.value || '';
            frontendAssets.shareOwing = asset.amount_owing || '';
            frontendAssets.shareG1 = isG1;
            frontendAssets.shareG2 = isG2;
          }
          break;
          
        case 'Credit Card':
          if (!frontendAssets.cardValue) {
            frontendAssets.cardValue = asset.value || '';
            frontendAssets.cardOwing = asset.amount_owing || '';
            frontendAssets.cardG1 = isG1;
            frontendAssets.cardG2 = isG2;
          }
          break;
          
        case 'Other Creditor':
          if (!frontendAssets.creditorValue) {
            frontendAssets.creditorValue = asset.value || '';
            frontendAssets.creditorOwing = asset.amount_owing || '';
            frontendAssets.creditorG1 = isG1;
            frontendAssets.creditorG2 = isG2;
          }
          break;
          
        case 'Other':
          if (!frontendAssets.otherValue) {
            frontendAssets.otherValue = asset.value || '';
            frontendAssets.otherOwing = asset.amount_owing || '';
            frontendAssets.otherG1 = isG1;
            frontendAssets.otherG2 = isG2;
          }
          break;
      }
    });
  });
  
  console.log("Reverse transformed guarantor assets:", frontendAssets);
  return frontendAssets;
}

/**
 * Creates an empty guarantor asset form object
 * @returns {Object} - Empty frontend format guarantor asset object
 */
function createEmptyGuarantorAssetForm() {
  return {
    address1: "", address1Value: "", address1Owing: "", address1G1: false, address1G2: false,
    address2: "", address2Value: "", address2Owing: "", address2G1: false, address2G2: false,
    address3: "", address3Value: "", address3Owing: "", address3G1: false, address3G2: false,
    address4: "", address4Value: "", address4Owing: "", address4G1: false, address4G2: false,
    vehicleValue: "", vehicleOwing: "", vehicleG1: false, vehicleG2: false,
    savingValue: "", savingOwing: "", savingG1: false, savingG2: false,
    shareValue: "", shareOwing: "", shareG1: false, shareG2: false,
    cardValue: "", cardOwing: "", cardG1: false, cardG2: false,
    creditorValue: "", creditorOwing: "", creditorG1: false, creditorG2: false,
    otherValue: "", otherOwing: "", otherG1: false, otherG2: false,
    totalValue: "", totalOwing: ""
  };
}
