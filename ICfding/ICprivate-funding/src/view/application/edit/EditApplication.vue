<template>
    <div class="popup">        
        <div class="popup_title">
            <h1>Edit Application</h1>
            <div class="close">
                <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleClose"><Close /></el-icon>                    
            </div>
        </div>
        <div v-if="isLoading" class="loading-container">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>Loading application data...</span>
        </div>
        <el-scrollbar v-else>
            <div class="popup_content">
                <el-collapse v-model="activeNames" accordion style="--el-collapse-border-color: none;">
                    <el-collapse-item name="1">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isCompanyValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isCompanyValid ? '#2984DE' : '#272727'}">Company Borrower Details</p>
                            </div>
                        </template>
                        <Company 
                            :key="`company-${application.company_borrowers.length}`"
                            :company="application.company_borrowers" 
                            @add="addDirector" 
                            @remove="removeDirector"
                            @addCompany="addCompanyBorrower"
                            @removeCompany="removeCompanyBorrower">
                        </Company>
                    </el-collapse-item>
                    <el-collapse-item name="2">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isCompanyAssetValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isCompanyAssetValid ? '#2984DE' : '#272727'}">Company Assets & Liabilities</p>
                            </div>
                        </template>
                        <CompanyAssets 
                            :key="`company-assets-${application.company_borrowers.length}`"
                            :company="application.company_borrowers"
                            @addAsset="addAsset"
                            @removeAsset="removeAsset"
                            @addLiability="addLiability"
                            @removeLiability="removeLiability"
                            @addCompany="addCompanyBorrower"
                        ></CompanyAssets>
                    </el-collapse-item>
                    <el-collapse-item name="3">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isIndividualValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isIndividualValid ? '#2984DE' : '#272727'}">Individual Borrower Details</p>
                            </div>
                        </template>
                        <Inividual :borrowers="application.borrowers" @add="addBorrower" @remove="removeBorrower"></Inividual>
                    </el-collapse-item>
                    <el-collapse-item name="4">                        
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isEnquiryValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isEnquiryValid ? '#2984DE' : '#272727'}">General Solvency Enquires</p>
                            </div>
                        </template>
                        <Enquiries :enquiry="application"></Enquiries>
                    </el-collapse-item>
                    <el-collapse-item name="5">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isIndividualValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isIndividualValid ? '#2984DE' : '#272727'}">Guarantor Details</p>
                            </div>
                        </template>
                        <Guarantor :guarantors="application.guarantors" @add="addGuarantor" @remove="removeGuarantor"></Guarantor>
                    </el-collapse-item>
                    <el-collapse-item name="6">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isGuarantorAssetValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isGuarantorAssetValid ? '#2984DE' : '#272727'}">Guarantor Assets & Liability</p>
                            </div>
                        </template>
                        <GuarantorAsset :asset="guarantorAsset"></GuarantorAsset>
                    </el-collapse-item>
                    <el-collapse-item name="7">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isSecurityValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isSecurityValid ? '#2984DE' : '#272727'}">Proposed Security Details</p>
                            </div>
                        </template>
                        <Security :security="application.security_properties" @add="addSecurity" @remove="removeSecurity"></Security>
                    </el-collapse-item>
                    <el-collapse-item name="8">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isLoanDetailValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isLoanDetailValid ? '#2984DE' : '#272727'}">Loan Details & Purpose</p>
                            </div>
                        </template>
                        <LoanDetail :detail="application"></LoanDetail>
                    </el-collapse-item>
                    <el-collapse-item name="9">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isRequirementValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isRequirementValid ? '#2984DE' : '#272727'}">Loan Requirements</p>
                            </div>
                        </template>
                        <LoanRequirement 
                            :requirement="application.loan_requirements"
                            @add="addRequirement"
                            @remove="removeRequirement"
                        ></LoanRequirement>
                    </el-collapse-item>
                    <el-collapse-item name="10">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isExitValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isExitValid ? '#2984DE' : '#272727'}">Funding Calculation Input</p>
                            </div>
                        </template>
                        <Calculation :detail="application.funding_calculation_input"></Calculation>
                    </el-collapse-item>
                    <el-collapse-item name="11">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isExitValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isExitValid ? '#2984DE' : '#272727'}">Proposed Exit Strategy</p>
                            </div>
                        </template>
                        <Exit :exit="application"></Exit>
                    </el-collapse-item>
                </el-collapse>
            </div>
        </el-scrollbar>
        <div class="buttons">
            <Cancel @click="handleClose"></Cancel>
            <Save @click="handleSave" :loading="isSubmitting" text="Update"></Save>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { Close, SuccessFilled, Loading } from '@element-plus/icons-vue';
import { api } from '@/api';
import { transformGuarantorAssets } from '@/utils/guarantorAssetTransformer';

// Import components
import Company from '@/components/popup/addapplication/company.vue';
import CompanyAssets from '@/components/popup/addapplication/companyasset.vue';
import Enquiries from '@/components/popup/addapplication/enquiries.vue';
import Inividual from '@/components/popup/addapplication/inividual.vue';
import Guarantor from '@/components/popup/addapplication/guarantor.vue';
import GuarantorAsset from '@/components/popup/addapplication/guarantorasset.vue';
import Security from '@/components/popup/addapplication/security.vue';
import LoanDetail from '@/components/popup/addapplication/loandetail.vue';
import LoanRequirement from '@/components/popup/addapplication/loanrequirement.vue';
import Calculation from '@/components/popup/addapplication/calculation.vue';
import Exit from '@/components/popup/addapplication/exit.vue';
import Cancel from '@/components/buttons/cancel.vue';
import Save from '@/components/buttons/save.vue';

const props = defineProps({
    applicationId: {
        type: [Number, String],
        required: true
    }
});

const emit = defineEmits(['close', 'saved']);

// State
const activeNames = ref("1");
const isSubmitting = ref(false);
const isLoading = ref(true);
const application = ref({
    company_borrowers: [],
    borrowers: [],
    guarantors: [],
    security_properties: [],
    loan_requirements: [],
    funding_calculation_input: {}
});

const guarantorAsset = ref({
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
});

// Add a watcher to track changes to application data
watch(() => application.value.company_borrowers, (newVal, oldVal) => {
    console.log("Application company_borrowers changed:", {
        old: oldVal?.length || 0,
        new: newVal?.length || 0,
        data: newVal
    });
}, { deep: true });

// Helper function to create a new company borrower
const createCompanyBorrower = () => {
    return {
        company_name: "",
        company_abn: "",
        company_acn: "",
        industry_type: "",
        contact_number: "",
        annual_company_income: "",
        is_trustee: null,
        is_smsf_trustee: null,
        trustee_name: "",
        registered_address_unit: "",
        registered_address_street_no: "",
        registered_address_street_name: "",
        registered_address_suburb: "",
        registered_address_state: "",
        registered_address_postcode: "",
        directors: [{
            name: "",
            roles: "director",
            director_id: ""
        }],
        assets: [{
            asset_type: "Property",
            description: "",
            value: "",
            amount_owing: "",
            to_be_refinanced: "",
            address: ""
        }],
        liabilities: [{
            liability_type: "other",
            description: "",
            amount: "",
            lender: "",
            monthly_payment: "",
            to_be_refinanced: "",
            bg_type: "bg1"
        }]
    };
};

// Fetch application data on mount
onMounted(async () => {
    try {
        isLoading.value = true;
        console.log("Fetching application data for ID:", props.applicationId);
        
        // Add timestamp to force fresh data
        const [err, res] = await api.applicationWithCascade(props.applicationId, { 
            _t: Date.now() // Cache buster
        });
        if (err) {
            throw new Error(err.message || 'Failed to fetch application data');
        }
        
        console.log("=== FULL API RESPONSE ===");
        console.log(JSON.stringify(res, null, 2));
        console.log("=== AVAILABLE FIELDS ===");
        console.log("Fields in response:", Object.keys(res));
        console.log("=== COMPANY BORROWERS CHECK ===");
        console.log("company_borrowers field exists:", 'company_borrowers' in res);
        console.log("company_borrowers value:", res.company_borrowers);
        console.log("company_borrowers type:", typeof res.company_borrowers);
        console.log("company_borrowers length:", res.company_borrowers?.length);
        console.log("=== BORROWERS CHECK ===");
        console.log("borrowers field exists:", 'borrowers' in res);
        console.log("borrowers value:", res.borrowers);
        console.log("borrowers type:", typeof res.borrowers);
        console.log("borrowers length:", res.borrowers?.length);
        
        // Ensure company_borrowers is initialized as an array with proper structure
        if (!res.company_borrowers) {
            console.log("⚠️ No company_borrowers field found in API response!");
            res.company_borrowers = [];
        } else {
            console.log("✅ Found company_borrowers in API response:", res.company_borrowers);
            // Ensure each company borrower has the required fields
            res.company_borrowers.forEach((company, index) => {
                console.log(`Company borrower ${index}:`, company);
                if (!company.annual_company_income) company.annual_company_income = "";
                if (!company.assets) company.assets = [];
                if (!company.liabilities) company.liabilities = [];
                if (!company.directors) company.directors = [];
            });
        }
        
        // Ensure borrowers is initialized as an array
        if (!res.borrowers) {
            res.borrowers = [];
        } else {
            console.log("✅ Found borrowers in API response:", res.borrowers);
        }
        
        // Ensure guarantors is initialized as an array
        if (!res.guarantors) {
            res.guarantors = [];
        }
        
        // Ensure security_properties is initialized as an array
        if (!res.security_properties) {
            res.security_properties = [];
        }
        
        // Ensure loan_requirements is initialized as an array
        if (!res.loan_requirements) {
            res.loan_requirements = [];
        }
        
        // Ensure funding_calculation_input is initialized as an object
        if (!res.funding_calculation_input) {
            res.funding_calculation_input = {};
        }
        
        application.value = res;
        console.log("Application data loaded:", application.value);
        
        // Transform guarantor assets if they exist
        if (res.guarantors && res.guarantors.length > 0 && res.guarantors[0].assets) {
            try {
                const transformedAssets = transformGuarantorAssets(res.guarantors[0].assets);
                if (transformedAssets) {
                    guarantorAsset.value = transformedAssets;
                }
            } catch (error) {
                console.error("Error transforming guarantor assets:", error);
            }
        }
        
        ElMessage.success('Application data loaded successfully');
    } catch (error) {
        console.error("Error loading application:", error);
        ElMessage.error(error.message || 'Failed to load application data');
    } finally {
        isLoading.value = false;
    }
});

// Computed properties for validation - all fields are now optional
const isCompanyValid = computed(() => {
    // All fields are now optional - always return true
    return true;
});

const isCompanyAssetValid = computed(() => {
    // All fields are now optional - always return true
    return true;
});

const isEnquiryValid = computed(() => {
    // All fields are now optional - always return true
    return true;
});

const isIndividualValid = computed(() => {
    // All fields are now optional - always return true
    return true;
});

const isGuarantorAssetValid = computed(() => {
    // All fields are now optional - always return true
    return true;
});

const isSecurityValid = computed(() => {
    // All fields are now optional - always return true
    return true;
});

const isLoanDetailValid = computed(() => {
    // All fields are now optional - always return true
    return true;
});

const isRequirementValid = computed(() => {
    // All fields are now optional - always return true
    return true;
});

const isExitValid = computed(() => {
    // All fields are now optional - always return true
    return true;
});

// Event handlers
const handleClose = () => {
    emit('close');
};

const handleSave = async () => {
    try {
        isSubmitting.value = true;
        
        // Create a deep copy and transform data
        const applicationData = JSON.parse(JSON.stringify(application.value));
        
        // Add debug logging for company borrowers
        console.log("=== SAVE OPERATION DEBUG ===");
        console.log("Full applicationData:", applicationData);
        console.log("company_borrowers in save data:", applicationData.company_borrowers);
        console.log("company_borrowers length:", applicationData.company_borrowers?.length);
        if (applicationData.company_borrowers && applicationData.company_borrowers.length > 0) {
            applicationData.company_borrowers.forEach((company, index) => {
                console.log(`Company borrower ${index}:`, company);
                console.log(`Company borrower ${index} directors:`, company.directors);
                console.log(`Company borrower ${index} assets:`, company.assets);
                console.log(`Company borrower ${index} liabilities:`, company.liabilities);
            });
        }
        
        // Clean and validate company borrowers data before sending
        if (applicationData.company_borrowers && applicationData.company_borrowers.length > 0) {
            applicationData.company_borrowers.forEach((company, index) => {
                // Filter out empty directors (directors with no name)
                if (company.directors) {
                    company.directors = company.directors.filter(director => 
                        director.name && director.name.trim() !== ''
                    );
                }
                
                // Filter out empty assets (assets with no asset_type or description)
                if (company.assets) {
                    company.assets = company.assets.filter(asset => 
                        asset.asset_type && asset.asset_type.trim() !== '' &&
                        asset.description && asset.description.trim() !== ''
                    );
                }
                
                // Filter out empty liabilities (liabilities with no liability_type or description)
                if (company.liabilities) {
                    company.liabilities = company.liabilities.filter(liability => 
                        liability.liability_type && liability.liability_type.trim() !== '' &&
                        liability.description && liability.description.trim() !== ''
                    );
                }
                
                // Ensure numeric fields are properly formatted
                if (company.annual_company_income === '') {
                    company.annual_company_income = null;
                }
                
                console.log(`Cleaned company borrower ${index}:`, company);
            });
        }
        
        // Clean and validate security properties data before sending
        if (applicationData.security_properties && applicationData.security_properties.length > 0) {
            applicationData.security_properties = applicationData.security_properties.filter(property => 
                property.address_street_name || property.address_suburb
            ).map(property => {
                // Validate property_type against schema choices
                const validPropertyTypes = ["residential", "commercial", "industrial", "retail", "land", "rural", "other"];
                if (property.property_type && !validPropertyTypes.includes(property.property_type)) {
                    property.property_type = "residential"; // Default to residential
                }
                
                return {
                    ...property,
                    // Convert string numbers to integers for bedrooms, bathrooms, car_spaces
                    bedrooms: property.bedrooms === "" || property.bedrooms === null || property.bedrooms === undefined ? null : parseInt(property.bedrooms) || null,
                    bathrooms: property.bathrooms === "" || property.bathrooms === null || property.bathrooms === undefined ? null : parseInt(property.bathrooms) || null,
                    car_spaces: property.car_spaces === "" || property.car_spaces === null || property.car_spaces === undefined ? null : parseInt(property.car_spaces) || null,
                    
                    // Set boolean fields to null if empty string or undefined
                    is_single_story: property.is_single_story === "" || property.is_single_story === undefined ? null : property.is_single_story,
                    has_garage: property.has_garage === "" || property.has_garage === undefined ? null : property.has_garage,
                    has_carport: property.has_carport === "" || property.has_carport === undefined ? null : property.has_carport,
                    has_off_street_parking: property.has_off_street_parking === "" || property.has_off_street_parking === undefined ? null : property.has_off_street_parking,
                    
                    // Convert string numbers to floats for decimal fields
                    current_debt_position: property.current_debt_position === "" || property.current_debt_position === null ? null : parseFloat(property.current_debt_position) || null,
                    estimated_value: property.estimated_value === "" || property.estimated_value === null ? null : parseFloat(property.estimated_value) || null,
                    purchase_price: property.purchase_price === "" || property.purchase_price === null ? null : parseFloat(property.purchase_price) || null,
                    building_size: property.building_size === "" || property.building_size === null ? null : parseFloat(property.building_size) || null,
                    land_size: property.land_size === "" || property.land_size === null ? null : parseFloat(property.land_size) || null
                };
            });
        }
        
        // Only transform guarantor assets if they exist
        if (applicationData.guarantors && applicationData.guarantors.length > 0) {
            try {
                applicationData.guarantors = transformGuarantorAssets(guarantorAsset.value, applicationData.guarantors);
            } catch (error) {
                console.error("Error transforming guarantor assets for save:", error);
                // Continue with save even if transformation fails
            }
        }
        
        // Update application using partial update with cascade
        const [err, res] = await api.updateApplicationWithCascade(props.applicationId, applicationData);
        
        if (err) {
            console.error("API Error details:", err);
            
            // Check if it's a validation error and provide specific feedback
            if (err.status === 400 && err.data) {
                let errorMessage = 'Validation failed:\n';
                
                // Handle company borrower validation errors
                if (err.data.company_borrowers) {
                    errorMessage += 'Company Borrower errors:\n';
                    if (Array.isArray(err.data.company_borrowers)) {
                        err.data.company_borrowers.forEach((companyErrors, index) => {
                            if (companyErrors && typeof companyErrors === 'object') {
                                Object.keys(companyErrors).forEach(field => {
                                    errorMessage += `- Company ${index + 1} ${field}: ${companyErrors[field]}\n`;
                                });
                            }
                        });
                    }
                }
                
                // Handle other validation errors
                Object.keys(err.data).forEach(field => {
                    if (field !== 'company_borrowers' && err.data[field]) {
                        errorMessage += `- ${field}: ${err.data[field]}\n`;
                    }
                });
                
                throw new Error(errorMessage);
            }
            
            throw new Error(err.message || 'Failed to update application');
        }
        
        ElMessage.success('Application updated successfully');
        
        // Emit saved event with the updated data
        emit('saved', { id: props.applicationId, data: applicationData });
        
        handleClose();
    } catch (error) {
        console.error("Error saving application:", error);
        ElMessage.error(error.message || 'Failed to update application');
    } finally {
        isSubmitting.value = false;
    }
};

// Add/remove handlers for company borrowers
const addCompanyBorrower = () => {
    console.log("Adding company borrower...");
    const newCompany = createCompanyBorrower();
    application.value.company_borrowers.push(newCompany);
    
    // Force reactivity update
    application.value = { ...application.value };
    console.log("Company borrowers after add:", application.value.company_borrowers);
};

const removeCompanyBorrower = (idx) => {
    console.log("Removing company borrower at index:", idx);
    application.value.company_borrowers.splice(idx, 1);
    
    // Force reactivity update
    application.value = { ...application.value };
    console.log("Company borrowers after remove:", application.value.company_borrowers);
};

const addDirector = () => {
    console.log("Adding director...");
    // Ensure company_borrowers array exists and has at least one element
    if (!application.value.company_borrowers || application.value.company_borrowers.length === 0) {
        application.value.company_borrowers = [createCompanyBorrower()];
    }
    
    if (!application.value.company_borrowers[0].directors) {
        application.value.company_borrowers[0].directors = [];
    }
    application.value.company_borrowers[0].directors.push({
        name: "",
        roles: "director",
        director_id: ""
    });
    
    // Force reactivity update
    application.value = { ...application.value };
    console.log("Directors after add:", application.value.company_borrowers[0].directors);
};

const removeDirector = (idx) => {
    console.log("Removing director at index:", idx);
    if (application.value.company_borrowers && 
        application.value.company_borrowers[0] && 
        application.value.company_borrowers[0].directors) {
        application.value.company_borrowers[0].directors.splice(idx, 1);
        
        // Force reactivity update
        application.value = { ...application.value };
        console.log("Directors after remove:", application.value.company_borrowers[0].directors);
    }
};

const addAsset = () => {
    console.log("Adding asset...");
    // Ensure company_borrowers array exists and has at least one element
    if (!application.value.company_borrowers || application.value.company_borrowers.length === 0) {
        application.value.company_borrowers = [createCompanyBorrower()];
    }
    
    if (!application.value.company_borrowers[0].assets) {
        application.value.company_borrowers[0].assets = [];
    }
    application.value.company_borrowers[0].assets.push({
        asset_type: "Property",
        description: "",
        value: "",
        amount_owing: "",
        to_be_refinanced: "",
        address: ""
    });
    
    // Force reactivity update
    application.value = { ...application.value };
    console.log("Assets after add:", application.value.company_borrowers[0].assets);
};

const removeAsset = (idx) => {
    console.log("Removing asset at index:", idx);
    if (application.value.company_borrowers && 
        application.value.company_borrowers[0] && 
        application.value.company_borrowers[0].assets) {
        application.value.company_borrowers[0].assets.splice(idx, 1);
        
        // Force reactivity update
        application.value = { ...application.value };
        console.log("Assets after remove:", application.value.company_borrowers[0].assets);
    }
};

const addLiability = () => {
    console.log("Adding liability...");
    // Ensure company_borrowers array exists and has at least one element
    if (!application.value.company_borrowers || application.value.company_borrowers.length === 0) {
        application.value.company_borrowers = [createCompanyBorrower()];
    }
    
    if (!application.value.company_borrowers[0].liabilities) {
        application.value.company_borrowers[0].liabilities = [];
    }
    application.value.company_borrowers[0].liabilities.push({
        liability_type: "other",
        description: "",
        amount: "",
        lender: "",
        monthly_payment: "",
        to_be_refinanced: "",
        bg_type: "bg1"
    });
    
    // Force reactivity update
    application.value = { ...application.value };
    console.log("Liabilities after add:", application.value.company_borrowers[0].liabilities);
};

const removeLiability = (idx) => {
    console.log("Removing liability at index:", idx);
    if (application.value.company_borrowers && 
        application.value.company_borrowers[0] && 
        application.value.company_borrowers[0].liabilities) {
        application.value.company_borrowers[0].liabilities.splice(idx, 1);
        
        // Force reactivity update
        application.value = { ...application.value };
        console.log("Liabilities after remove:", application.value.company_borrowers[0].liabilities);
    }
};

const addBorrower = () => {
    application.value.borrowers.push({
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        date_of_birth: "",
        tax_id: "",
        marital_status: "",
        residency_status: "",
        referral_source: "",
        tags: ""
    });
};

const removeBorrower = (idx) => {
    application.value.borrowers.splice(idx, 1);
};

const addGuarantor = () => {
    application.value.guarantors.push({
        guarantor_type: "",
        title: "",
        first_name: "",
        last_name: "",
        date_of_birth: "",
        drivers_licence_no: "",
        home_phone: "",
        mobile: "",
        email: "",
        address_unit: "",
        address_street_no: "",
        address_street_name: "",
        address_suburb: "",
        address_state: "",
        address_postcode: "",
        occupation: "",
        employer_name: "",
        employment_type: "",
        annual_income: "",
        company_name: "",
        company_abn: "",
        company_acn: "",
        borrower: null,
        application: null,
        assets: [],
        liabilities: []
    });
};

const removeGuarantor = (idx) => {
    application.value.guarantors.splice(idx, 1);
};

const addSecurity = () => {
    application.value.security_properties.push({
        address_unit: "",
        address_street_no: "",
        address_street_name: "",
        address_suburb: "",
        address_state: "",
        address_postcode: "",
        property_type: "",
        bedrooms: null,  // Initialize as null instead of empty string
        bathrooms: null, // Initialize as null instead of empty string
        car_spaces: null, // Initialize as null instead of empty string
        building_size: null,
        land_size: null,
        has_garage: null,
        has_carport: null,
        is_single_story: null,
        has_off_street_parking: null,
        current_mortgagee: "",
        first_mortgage: "",
        second_mortgage: "",
        current_debt_position: null,
        occupancy: "",
        estimated_value: null,
        purchase_price: null
    });
};

const removeSecurity = (idx) => {
    application.value.security_properties.splice(idx, 1);
};

const addRequirement = () => {
    application.value.loan_requirements.push({
        description: "",
        amount: ""
    });
};

const removeRequirement = (idx) => {
    application.value.loan_requirements.splice(idx, 1);
};
</script>

<style scoped>
.popup {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    padding: 10px;
    display: flex;
    flex-direction: column;
    background: white;
    border: none;
    box-shadow: -8px -1px 9.3px 0px rgba(202, 202, 202, 0.16);
    width: 50%;
    height: 100vh;
    overflow: hidden;
    z-index: 1000;
}

.popup_title {
    width: 100%;
    padding: 10px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid var(--Line, #E1E1E1);
}

h1 {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 1.1rem;
    font-style: normal;
    font-weight: 500;
    line-height: 12px;
}

.close {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 20px;
}

.popup_content {
    width: 100%;
    padding: 10px;
}

.title {
    display: flex;
    align-items: center;
    gap: 10px;
}

.buttons {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
    padding: 10px;
    border-top: 1.5px solid #E1E1E1;
}

.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    gap: 10px;
}

.loading-container .el-icon {
    font-size: 24px;
    color: #2984DE;
}
</style>
