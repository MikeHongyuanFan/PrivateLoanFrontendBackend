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
                        <Company v-if="application.company_borrowers && application.company_borrowers.length > 0" 
                            :company="application.company_borrowers" 
                            @add="addDirector" 
                            @remove="removeDirector">
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
                            v-if="application.company_borrowers && application.company_borrowers.length > 0"
                            :company="application.company_borrowers"
                            @addAsset="addAsset"
                            @removeAsset="removeAsset"
                            @addLiability="addLiability"
                            @removeLiability="removeLiability"
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
import { ref, computed, onMounted } from 'vue';
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

const emit = defineEmits(['close']);

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

// Fetch application data on mount
onMounted(async () => {
    try {
        isLoading.value = true;
        console.log("Fetching application data for ID:", props.applicationId);
        
        const [err, res] = await api.application(props.applicationId);
        if (err) {
            throw new Error(err.message || 'Failed to fetch application data');
        }
        
        // Ensure company_borrowers is initialized as an array
        if (!res.company_borrowers) {
            res.company_borrowers = [];
        }
        
        // Ensure borrowers is initialized as an array
        if (!res.borrowers) {
            res.borrowers = [];
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

// Computed properties for validation
const isCompanyValid = computed(() => {
    if (!application.value?.company_borrowers?.[0]) return false;
    const company = application.value.company_borrowers[0];
    return company.company_name && company.company_abn && company.industry_type;
});

const isCompanyAssetValid = computed(() => {
    if (!application.value?.company_borrowers?.[0]?.assets) return false;
    const assets = application.value.company_borrowers[0].assets;
    return assets.length > 0 && assets.every(asset => asset.asset_type && asset.value);
});

const isEnquiryValid = computed(() => {
    return application.value.has_pending_litigation !== null &&
           application.value.has_unsatisfied_judgements !== null &&
           application.value.has_been_bankrupt !== null &&
           application.value.has_been_refused_credit !== null;
});

const isIndividualValid = computed(() => {
    if (!application.value?.borrowers) return false;
    return application.value.borrowers.length > 0 && 
           application.value.borrowers.every(borrower => 
               borrower.first_name && borrower.last_name && borrower.email
           );
});

const isGuarantorAssetValid = computed(() => {
    const ga = guarantorAsset.value;
    return ga && (
        (ga.address1 && (ga.address1G1 || ga.address1G2)) ||
        (ga.address2 && (ga.address2G1 || ga.address2G2)) ||
        (ga.address3 && (ga.address3G1 || ga.address3G2)) ||
        (ga.address4 && (ga.address4G1 || ga.address4G2)) ||
        (ga.vehicleValue && (ga.vehicleG1 || ga.vehicleG2)) ||
        (ga.savingValue && (ga.savingG1 || ga.savingG2)) ||
        (ga.shareValue && (ga.shareG1 || ga.shareG2)) ||
        (ga.cardValue && (ga.cardG1 || ga.cardG2)) ||
        (ga.creditorValue && (ga.creditorG1 || ga.creditorG2)) ||
        (ga.otherValue && (ga.otherG1 || ga.otherG2))
    );
});

const isSecurityValid = computed(() => {
    if (!application.value?.security_properties) return false;
    return application.value.security_properties.length > 0 && 
           application.value.security_properties.every(property => 
               property.address_street_name && property.address_suburb && 
               property.address_state && property.address_postcode
           );
});

const isLoanDetailValid = computed(() => {
    return application.value.loan_amount && 
           application.value.repayment_frequency && 
           application.value.application_type && 
           application.value.product_id;
});

const isRequirementValid = computed(() => {
    if (!application.value?.loan_requirements) return false;
    return application.value.loan_requirements.length > 0 && 
           application.value.loan_requirements.every(req => req.description && req.amount);
});

const isExitValid = computed(() => {
    return application.value.exit_strategy && 
           (application.value.exit_strategy !== 'other' || application.value.exit_strategy_details);
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
        
        // Only transform guarantor assets if they exist
        if (applicationData.guarantors && applicationData.guarantors.length > 0) {
            try {
                applicationData.guarantors = transformGuarantorAssets(guarantorAsset.value, applicationData.guarantors);
            } catch (error) {
                console.error("Error transforming guarantor assets for save:", error);
                // Continue with save even if transformation fails
            }
        }
        
        // Update application
        const [err, res] = await api.updateApplication(props.applicationId, applicationData);
        
        if (err) {
            throw new Error(err.message || 'Failed to update application');
        }
        
        ElMessage.success('Application updated successfully');
        handleClose();
    } catch (error) {
        console.error("Error saving application:", error);
        ElMessage.error(error.message || 'Failed to update application');
    } finally {
        isSubmitting.value = false;
    }
};

// Add/remove handlers
const addDirector = () => {
    if (!application.value.company_borrowers[0].directors) {
        application.value.company_borrowers[0].directors = [];
    }
    application.value.company_borrowers[0].directors.push({
        name: "",
        roles: "",
        director_id: ""
    });
};

const removeDirector = (idx) => {
    application.value.company_borrowers[0].directors.splice(idx, 1);
};

const addAsset = () => {
    if (!application.value.company_borrowers[0].assets) {
        application.value.company_borrowers[0].assets = [];
    }
    application.value.company_borrowers[0].assets.push({
        asset_type: "",
        description: "",
        value: "",
        amount_owing: "",
        to_be_refinanced: "",
        address: ""
    });
};

const removeAsset = (idx) => {
    application.value.company_borrowers[0].assets.splice(idx, 1);
};

const addLiability = () => {
    if (!application.value.company_borrowers[0].liabilities) {
        application.value.company_borrowers[0].liabilities = [];
    }
    application.value.company_borrowers[0].liabilities.push({
        liability_type: "",
        description: "",
        amount: "",
        lender: "",
        monthly_payment: "",
        to_be_refinanced: "",
        bg_type: "bg1"
    });
};

const removeLiability = (idx) => {
    application.value.company_borrowers[0].liabilities.splice(idx, 1);
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
        bedrooms: "",
        bathrooms: "",
        car_spaces: "",
        building_size: "",
        land_size: "",
        has_garage: null,
        has_carport: null,
        is_single_story: null,
        has_off_street_parking: null,
        current_mortgagee: "",
        first_mortgage: "",
        second_mortgage: "",
        current_debt_position: "",
        occupancy: "",
        estimated_value: "",
        purchase_price: ""
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
