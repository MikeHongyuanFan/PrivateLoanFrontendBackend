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
                <!-- Add stage display -->
                <div class="stage-section">
                    <h2>Current Stage</h2>
                    <el-tag :type="getStageTagType(application.stage)" size="large">
                        {{ getStageDisplay(application.stage) }}
                    </el-tag>
                </div>
                
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
                        <GuarantorAsset 
                            :guarantors="application.guarantors" 
                            @update:guarantors="updateGuarantors">
                        </GuarantorAsset>
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

// Add a watcher to track changes to application data
watch(() => application.value.company_borrowers, (newVal, oldVal) => {
    console.log("Application company_borrowers changed:", {
        old: oldVal?.length || 0,
        new: newVal?.length || 0,
        data: newVal
    });
}, { deep: true });

// Add a watcher to track changes to guarantors data
watch(() => application.value.guarantors, (newVal, oldVal) => {
    console.log("Application guarantors changed:", {
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
        console.log("=== GUARANTORS CHECK ===");
        console.log("guarantors field exists:", 'guarantors' in res);
        console.log("guarantors value:", res.guarantors);
        console.log("guarantors type:", typeof res.guarantors);
        console.log("guarantors length:", res.guarantors?.length);
        
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
                
                // Convert numeric fields from strings to numbers for el-input-number components
                if (company.annual_company_income && typeof company.annual_company_income === 'string') {
                    company.annual_company_income = parseFloat(company.annual_company_income) || 0;
                }
            });
        }
        
        // Ensure borrowers is initialized as an array
        if (!res.borrowers) {
            res.borrowers = [];
        } else {
            console.log("✅ Found borrowers in API response:", res.borrowers);
        }
        
        // Ensure guarantors is initialized as an array with proper structure
        if (!res.guarantors) {
            res.guarantors = [];
        } else {
            console.log("✅ Found guarantors in API response:", res.guarantors);
            // Ensure each guarantor has the required fields
            res.guarantors.forEach((guarantor, index) => {
                console.log(`Guarantor ${index}:`, guarantor);
                if (!guarantor.assets) guarantor.assets = [];
                if (!guarantor.liabilities) guarantor.liabilities = [];
                
                // Convert numeric fields from strings to numbers for el-input-number components
                if (guarantor.annual_income && typeof guarantor.annual_income === 'string') {
                    guarantor.annual_income = parseFloat(guarantor.annual_income) || 0;
                }
            });
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
        
        // Transform address data from backend format to frontend format
        if (res.borrowers && res.borrowers.length > 0) {
            res.borrowers.forEach((borrower, index) => {
                console.log(`=== LOADING BORROWER ${index} ADDRESS DATA ===`);
                console.log('Backend borrower data:', {
                    address: borrower.address,
                    residential_address: borrower.residential_address,
                    mailing_address: borrower.mailing_address
                });
                
                // Convert numeric fields from strings to numbers for el-input-number components
                if (borrower.annual_income && typeof borrower.annual_income === 'string') {
                    borrower.annual_income = parseFloat(borrower.annual_income) || 0;
                }
                if (borrower.employment_duration && typeof borrower.employment_duration === 'string') {
                    borrower.employment_duration = parseFloat(borrower.employment_duration) || 0;
                }
                if (borrower.other_income && typeof borrower.other_income === 'string') {
                    borrower.other_income = parseFloat(borrower.other_income) || 0;
                }
                if (borrower.monthly_expenses && typeof borrower.monthly_expenses === 'string') {
                    borrower.monthly_expenses = parseFloat(borrower.monthly_expenses) || 0;
                }
                
                // Parse structured address data from address object if available
                if (borrower.address) {
                    borrower.address_street = borrower.address.street || '';
                    borrower.address_city = borrower.address.city || '';
                    borrower.address_state = borrower.address.state || '';
                    borrower.address_postal_code = borrower.address.postal_code || '';
                    borrower.address_country = borrower.address.country || '';
                    console.log('Parsed address fields from nested object:', {
                        address_street: borrower.address_street,
                        address_city: borrower.address_city,
                        address_state: borrower.address_state,
                        address_postal_code: borrower.address_postal_code,
                        address_country: borrower.address_country
                    });
                } else {
                    console.log('No nested address object found, fields will remain empty');
                    // Initialize empty fields
                    borrower.address_street = '';
                    borrower.address_city = '';
                    borrower.address_state = '';
                    borrower.address_postal_code = '';
                    borrower.address_country = '';
                }
            });
        }
        
        application.value = res;
        // Ensure at least one security property exists for editing
        if (!application.value.security_properties || application.value.security_properties.length === 0) {
            application.value.security_properties = [{
                address_unit: "",
                address_street_no: "",
                address_street_name: "",
                address_suburb: "",
                address_state: "",
                address_postcode: "",
                property_type: "",
                description_if_applicable: "",
                bedrooms: null,
                bathrooms: null,
                car_spaces: null,
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
                first_mortgage_debt: null,
                second_mortgage_debt: null,
                occupancy: "",
                estimated_value: null,
                purchase_price: null
            }];
            console.log("Initialized blank security property for editing.");
        }
        console.log("Application data loaded:", application.value);
        
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
        
        // Validate stage value
        const validStages = [
            'received', 'sent_to_lender', 'funding_table_issued', 
            'indicative_letter_issued', 'indicative_letter_signed', 
            'commitment_fee_received', 'application_submitted',
            'valuation_ordered', 'valuation_received', 'more_info_required',
            'formal_approval', 'loan_docs_instructed', 'loan_docs_issued',
            'loan_docs_signed', 'settlement_conditions', 'settled',
            'closed', 'discharged'
        ];
        
        // If stage is not valid, set it to 'received'
        if (!validStages.includes(applicationData.stage)) {
            applicationData.stage = 'received';
        }
        
        // Transform related objects to IDs for API compatibility
        // Convert broker object to broker ID
        if (applicationData.broker && typeof applicationData.broker === 'object' && applicationData.broker.id) {
            applicationData.broker = applicationData.broker.id;
        }
        
        // Convert bd object to bd ID
        if (applicationData.bd && typeof applicationData.bd === 'object' && applicationData.bd.id) {
            applicationData.bd = applicationData.bd.id;
        }
        
        // Convert branch object to branch ID
        if (applicationData.branch && typeof applicationData.branch === 'object' && applicationData.branch.id) {
            applicationData.branch = applicationData.branch.id;
        }
        
        // Convert valuer object to valuer ID
        if (applicationData.valuer && typeof applicationData.valuer === 'object' && applicationData.valuer.id) {
            applicationData.valuer = applicationData.valuer.id;
        }
        
        // Convert quantity_surveyor object to quantity_surveyor ID
        if (applicationData.quantity_surveyor && typeof applicationData.quantity_surveyor === 'object' && applicationData.quantity_surveyor.id) {
            applicationData.quantity_surveyor = applicationData.quantity_surveyor.id;
        }
        
        // Transform structured address data for borrowers
        if (applicationData.borrowers && applicationData.borrowers.length > 0) {
            applicationData.borrowers.forEach((borrower, index) => {
                console.log(`=== EDIT BORROWER ${index} ADDRESS DEBUG ===`);
                console.log('Original borrower data:', {
                    address_street: borrower.address_street,
                    address_city: borrower.address_city,
                    address_state: borrower.address_state,
                    address_postal_code: borrower.address_postal_code,
                    address_country: borrower.address_country,
                    mailing_address: borrower.mailing_address
                });
                
                // Create structured address object for API
                if (borrower.address_street || borrower.address_city || borrower.address_state || borrower.address_postal_code || borrower.address_country) {
                    borrower.address = {
                        street: borrower.address_street || '',
                        city: borrower.address_city || '',
                        state: borrower.address_state || '',
                        postal_code: borrower.address_postal_code || '',
                        country: borrower.address_country || ''
                    };
                    console.log('Created nested address object:', borrower.address);
                } else {
                    console.log('No address fields found, skipping nested address creation');
                }
                
                // Clean up the individual address fields since we're sending them as nested object
                delete borrower.address_street;
                delete borrower.address_city;
                delete borrower.address_state;
                delete borrower.address_postal_code;
                delete borrower.address_country;
                
                console.log('Final borrower data:', {
                    address: borrower.address,
                    mailing_address: borrower.mailing_address
                });
            });
        }
        
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
        
        // Add debug logging for guarantors
        console.log("guarantors in save data:", applicationData.guarantors);
        console.log("guarantors length:", applicationData.guarantors?.length);
        if (applicationData.guarantors && applicationData.guarantors.length > 0) {
            applicationData.guarantors.forEach((guarantor, index) => {
                console.log(`Guarantor ${index}:`, guarantor);
                console.log(`Guarantor ${index} assets:`, guarantor.assets);
                console.log(`Guarantor ${index} liabilities:`, guarantor.liabilities);
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
        
        // Clean and validate guarantors data before sending
        if (applicationData.guarantors && applicationData.guarantors.length > 0) {
            applicationData.guarantors.forEach((guarantor, index) => {
                // Filter out empty assets (assets with no asset_type or description)
                if (guarantor.assets) {
                    guarantor.assets = guarantor.assets.filter(asset => 
                        asset.asset_type && asset.asset_type.trim() !== '' &&
                        asset.description && asset.description.trim() !== ''
                    );
                }
                
                // Filter out empty liabilities (liabilities with no liability_type or description)
                if (guarantor.liabilities) {
                    guarantor.liabilities = guarantor.liabilities.filter(liability => 
                        liability.liability_type && liability.liability_type.trim() !== '' &&
                        liability.description && liability.description.trim() !== ''
                    );
                }
                
                // Ensure numeric fields are properly formatted
                if (guarantor.annual_income === '') {
                    guarantor.annual_income = null;
                }
                
                console.log(`Cleaned guarantor ${index}:`, guarantor);
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
                    bedrooms: property.bedrooms === "" || property.bedrooms === null || property.bedrooms === undefined ? null : parseInt(property.bedrooms),
                    bathrooms: property.bathrooms === "" || property.bathrooms === null || property.bathrooms === undefined ? null : parseInt(property.bathrooms),
                    car_spaces: property.car_spaces === "" || property.car_spaces === null || property.car_spaces === undefined ? null : parseInt(property.car_spaces),
                    
                    // Set boolean fields to null if empty string or undefined
                    is_single_story: property.is_single_story === "" || property.is_single_story === undefined ? null : property.is_single_story,
                    has_garage: property.has_garage === "" || property.has_garage === undefined ? null : property.has_garage,
                    has_carport: property.has_carport === "" || property.has_carport === undefined ? null : property.has_carport,
                    has_off_street_parking: property.has_off_street_parking === "" || property.has_off_street_parking === undefined ? null : property.has_off_street_parking,
                    
                    // Convert string numbers to floats for decimal fields
                    current_debt_position: property.current_debt_position === "" || property.current_debt_position === null ? null : parseFloat(property.current_debt_position),
                    first_mortgage_debt: property.first_mortgage_debt === "" || property.first_mortgage_debt === null ? null : parseFloat(property.first_mortgage_debt),
                    second_mortgage_debt: property.second_mortgage_debt === "" || property.second_mortgage_debt === null ? null : parseFloat(property.second_mortgage_debt),
                    first_mortgage: property.first_mortgage === "" || property.first_mortgage === null ? null : parseFloat(property.first_mortgage),
                    second_mortgage: property.second_mortgage === "" || property.second_mortgage === null ? null : parseFloat(property.second_mortgage),
                    estimated_value: property.estimated_value === "" || property.estimated_value === null ? null : parseFloat(property.estimated_value),
                    purchase_price: property.purchase_price === "" || property.purchase_price === null ? null : parseFloat(property.purchase_price),
                    building_size: property.building_size === "" || property.building_size === null ? null : parseFloat(property.building_size),
                    land_size: property.land_size === "" || property.land_size === null ? null : parseFloat(property.land_size)
                };
            });
        }
        
        // Before calling api.updateApplicationWithCascade(props.applicationId, applicationData):
        if (applicationData.company_borrowers && applicationData.company_borrowers.length > 0) {
            applicationData.company_borrowers.forEach(company => {
                if (company.assets && company.assets.length > 0) {
                    company.assets.forEach(asset => {
                        if (asset.asset_type === 'Other') {
                            if (!asset.description_if_applicable || asset.description_if_applicable.trim() === "") {
                                ElMessage.error('Description (if applicable) is required for assets of type "Other".');
                                throw new Error('Validation failed: description_if_applicable required for Other asset');
                            }
                        } else {
                            // Remove the field if not needed
                            delete asset.description_if_applicable;
                        }
                    });
                }
            });
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
                
                // Handle guarantor validation errors
                if (err.data.guarantors) {
                    errorMessage += 'Guarantor errors:\n';
                    if (Array.isArray(err.data.guarantors)) {
                        err.data.guarantors.forEach((guarantorErrors, index) => {
                            if (guarantorErrors && typeof guarantorErrors === 'object') {
                                Object.keys(guarantorErrors).forEach(field => {
                                    errorMessage += `- Guarantor ${index + 1} ${field}: ${guarantorErrors[field]}\n`;
                                });
                            }
                        });
                    }
                }
                
                // Handle other validation errors
                Object.keys(err.data).forEach(field => {
                    if (field !== 'company_borrowers' && field !== 'guarantors' && err.data[field]) {
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

const addAsset = (companyIndex = 0) => {
    console.log("Adding asset to company index:", companyIndex);
    // Ensure company_borrowers array exists and has the requested element
    if (!application.value.company_borrowers || application.value.company_borrowers.length <= companyIndex) {
        console.error("Invalid company index or no company borrowers available");
        return;
    }
    
    if (!application.value.company_borrowers[companyIndex].assets) {
        application.value.company_borrowers[companyIndex].assets = [];
    }
    application.value.company_borrowers[companyIndex].assets.push({
        asset_type: "Property",
        description: "",
        value: "",
        amount_owing: "",
        to_be_refinanced: "",
        address: ""
    });
    
    // Force reactivity update
    application.value = { ...application.value };
    console.log("Assets after add:", application.value.company_borrowers[companyIndex].assets);
};

const removeAsset = (companyIndex = 0, assetIndex) => {
    console.log("Removing asset from company index:", companyIndex, "asset index:", assetIndex);
    if (application.value.company_borrowers && 
        application.value.company_borrowers[companyIndex] && 
        application.value.company_borrowers[companyIndex].assets) {
        if (assetIndex !== undefined) {
            application.value.company_borrowers[companyIndex].assets.splice(assetIndex, 1);
        } else {
            application.value.company_borrowers[companyIndex].assets.pop();
        }
        
        // Force reactivity update
        application.value = { ...application.value };
        console.log("Assets after remove:", application.value.company_borrowers[companyIndex].assets);
    }
};

const addLiability = (companyIndex = 0) => {
    console.log("Adding liability to company index:", companyIndex);
    // Ensure company_borrowers array exists and has the requested element
    if (!application.value.company_borrowers || application.value.company_borrowers.length <= companyIndex) {
        console.error("Invalid company index or no company borrowers available");
        return;
    }
    
    if (!application.value.company_borrowers[companyIndex].liabilities) {
        application.value.company_borrowers[companyIndex].liabilities = [];
    }
    application.value.company_borrowers[companyIndex].liabilities.push({
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
    console.log("Liabilities after add:", application.value.company_borrowers[companyIndex].liabilities);
};

const removeLiability = (companyIndex = 0, liabilityIndex) => {
    console.log("Removing liability from company index:", companyIndex, "liability index:", liabilityIndex);
    if (application.value.company_borrowers && 
        application.value.company_borrowers[companyIndex] && 
        application.value.company_borrowers[companyIndex].liabilities) {
        if (liabilityIndex !== undefined) {
            application.value.company_borrowers[companyIndex].liabilities.splice(liabilityIndex, 1);
        } else {
            application.value.company_borrowers[companyIndex].liabilities.pop();
        }
        
        // Force reactivity update
        application.value = { ...application.value };
        console.log("Liabilities after remove:", application.value.company_borrowers[companyIndex].liabilities);
    }
};

const addBorrower = () => {
    application.value.borrowers.push({
        // Personal Information
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        date_of_birth: "",
        tax_id: "",
        marital_status: "",
        residency_status: "",
        referral_source: "",
        tags: "",
        
        // Address Information
        address_street: "",
        address_city: "",
        address_state: "",
        address_postal_code: "",
        address_country: "",
        mailing_address: "",
        
        // Employment Information
        employment_type: "",
        employer_name: "",
        job_title: "",
        annual_income: null,
        employment_duration: null,
        employer_address: "",
        
        // Additional Financial Information
        other_income: null,
        monthly_expenses: null
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
        description_if_applicable: "",
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
        first_mortgage_debt: null,
        second_mortgage_debt: null,
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

// Add stage display helpers
const getStageDisplay = (stage) => {
    const stageMap = {
        'received': 'Received',
        'sent_to_lender': 'Sent to Lender/Investor',
        'funding_table_issued': 'Funding Table Issued',
        'indicative_letter_issued': 'Indicative Letter Issued',
        'indicative_letter_signed': 'Indicative Letter Signed',
        'commitment_fee_received': 'Commitment Fee Received',
        'application_submitted': 'Application Submitted',
        'valuation_ordered': 'Valuation Ordered',
        'valuation_received': 'Valuation Received',
        'more_info_required': 'More Information Required',
        'formal_approval': 'Formal Approval',
        'loan_docs_instructed': 'Loan Documents Instructed',
        'loan_docs_issued': 'Loan Documents Issued',
        'loan_docs_signed': 'Loan Documents Signed',
        'settlement_conditions': 'Settlement Conditions',
        'settled': 'Settled',
        'closed': 'Closed',
        'discharged': 'Discharged'
    };
    return stageMap[stage] || stage;
};

const getStageTagType = (stage) => {
    const stageTypes = {
        'received': 'info',
        'sent_to_lender': 'warning',
        'funding_table_issued': 'warning',
        'indicative_letter_issued': 'warning',
        'indicative_letter_signed': 'warning',
        'commitment_fee_received': 'success',
        'application_submitted': 'warning',
        'valuation_ordered': 'warning',
        'valuation_received': 'success',
        'more_info_required': 'danger',
        'formal_approval': 'success',
        'loan_docs_instructed': 'warning',
        'loan_docs_issued': 'warning',
        'loan_docs_signed': 'success',
        'settlement_conditions': 'warning',
        'settled': 'success',
        'closed': 'info',
        'discharged': 'info'
    };
    return stageTypes[stage] || 'info';
};

// Function to handle guarantor updates from the GuarantorAsset component
const updateGuarantors = (updatedGuarantors) => {
    application.value.guarantors = updatedGuarantors;
    console.log("Guarantors updated:", application.value.guarantors);
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

.stage-section {
    margin-bottom: 20px;
    padding: 16px;
    background-color: #f5f7fa;
    border-radius: 8px;
}

.stage-section h2 {
    margin: 0 0 12px 0;
    font-size: 16px;
    color: #606266;
}
</style>
