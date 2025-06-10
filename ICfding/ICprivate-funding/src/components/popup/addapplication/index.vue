<template>
    <div class="popup">        
        <div class="popup_title">
            <h1>New Application</h1>
            <div class="close">
                <!-- <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleMinimize"><Minus /></el-icon> -->
                <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleClose"><Close /></el-icon>                    
            </div>
        </div>
        <el-scrollbar>
            <div class="popup_content">
                <el-collapse v-model="activeNames" accordion style="--el-collapse-border-color: none;">
                    <el-collapse-item name="1">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isCompanyValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isCompanyValid ? '#2984DE' : '#272727'}">Company Borrower Details</p>
                            </div>
                        </template>
                        <Company :company="application.company_borrowers" @add="addDirector" @remove="removeDirector"></Company>
                    </el-collapse-item>
                    <el-collapse-item name="2">
                        <template #title>
                            <div class="title">
                                <el-icon style="font-size: 20px" :color="isCompanyAssetValid ? '#2984DE' : '#E1E1E1'"><SuccessFilled /></el-icon>
                                <p :style="{color: isCompanyAssetValid ? '#2984DE' : '#272727'}">Company Assets & Liabilities</p>
                            </div>
                        </template>
                        <CompanyAssets 
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
            <Save @click="handleSave" :loading="isSubmitting" text="Save"></Save>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, watch, onMounted } from 'vue';
    import { ElMessage } from 'element-plus';
    import { api } from '@/api';
    import { transformGuarantorAssets } from '@/utils/guarantorAssetTransformer';
    import Company from './company.vue';
    import CompanyAssets from './companyasset.vue';
    import Enquiries from './enquiries.vue';
    import Inividual from './inividual.vue';
    import Guarantor from './guarantor.vue';
    import GuarantorAsset from './guarantorasset.vue';
    import Security from './security.vue';
    import LoanDetail from './loandetail.vue';
    import LoanRequirement from './loanrequirement.vue';
    import Calculation from './calculation.vue';
    import Exit from './exit.vue';
    import Cancel from '@/components/buttons/cancel.vue';
    import Save from '@/components/buttons/save.vue';

    const props = defineProps({
        action: String
    })
    
    console.log("AddApplication component initialized with props:", props);
    
    const activeNames = ref("1")
    const isSubmitting = ref(false)
    
    const createDirector = () => {
        return {
            name: "",
            roles: "",
            director_id: ""
        }
    }
    const createCompanyAsset = () => {
        return {
            asset_type: "",
            description: "",
            value: "",
            amount_owing: "",
            to_be_refinanced: "",
            address: ""
        }
    }
    const createCompanyLiability = () => {
        return {
            liability_type: "",
            description: "",
            amount: "",
            lender: "",
            monthly_payment: "",
            to_be_refinanced: "",
            bg_type: "bg1"
        }
    }    
    const createCompany = () => {
        return {
            company_name: "",
            company_abn: "",
            industry_type: "",
            contact_number: "",
            annual_company_income: "",
            is_trustee: null,
            is_smsf_trustee: null,
            trustee_name: "",
            directors: [createDirector()],
            registered_address_unit: "",
            registered_address_street_no: "",
            registered_address_street_name: "",
            registered_address_suburb: "",
            registered_address_state: "",
            registered_address_postcode: "",
            financial_info: {
                annual_revenue: "",
                net_profit: "",
                assets: 0,  // Initialize with 0, will be computed later
                liabilities: 0  // Initialize with 0, will be computed later
            },
            assets: [createCompanyAsset()],
            liabilities: [createCompanyLiability()]
        }
    }
    const createBorrower = () => {
        return {
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
        }
    }
    const createGuarantor = () => {
        return {
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
        }
    }
    const createSecurity = () => {
        return {
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
        }
    }
    const createRequirement = () => {
        return {
            description: "",
            amount: ""
        }
    }
    const application = ref({
        reference_number: "",
        loan_amount: "",
        loan_term: "",
        interest_rate: "",
        purpose: "",
        repayment_frequency: "",
        application_type: "",
        product_id: "",
        estimated_settlement_date: "",
        stage: "inquiry",
        borrowers: [createBorrower()],
        guarantors: [createGuarantor()],
        company_borrowers: [createCompany()],
        security_properties: [createSecurity()],
        loan_requirements: [createRequirement()],
        loan_purpose: "",
        additional_comments: "",
        prior_application: true,
        prior_application_details: "",
        exit_strategy: "",
        exit_strategy_details: "",
        valuer_company_name: "",
        valuer_contact_name: "",
        valuer_phone: "",
        valuer_email: "",
        qs_company_name: "",
        qs_contact_name: "",
        qs_phone: "",
        qs_email: "",
        funding_calculation_input: {
            establishment_fee_rate: "",
            capped_interest_months: "",
            monthly_line_fee_rate: "",
            brokerage_fee_rate: "",
            application_fee: "",
            due_diligence_fee: "",
            legal_fee_before_gst: "",
            valuation_fee: "",
            monthly_account_fee: "",
            working_fee: ""
        },
        has_pending_litigation: null,
        has_unsatisfied_judgements: null,
        has_been_bankrupt: null,
        has_been_refused_credit: null,
        has_outstanding_ato_debt: null,
        has_outstanding_tax_returns: null,
        has_payment_arrangements: null,
        solvency_enquiries_details: ""
    })
    
    // Add safeguards to computed properties to prevent crashes
    const totalAsset = computed(() => {
        if (!application.value?.company_borrowers?.[0]?.assets) {
            return 0;
        }
        return application.value.company_borrowers[0].assets
            .map(a => parseFloat(a.value) || 0)
            .reduce((sum, v) => sum + v, 0);
    })
    
    const totalLiability = computed(() => {
        if (!application.value?.company_borrowers?.[0]?.liabilities) {
            return 0;
        }
        return application.value.company_borrowers[0].liabilities
            .map(a => parseFloat(a.amount) || 0)
            .reduce((sum, v) => sum + v, 0);
    })
    
    // Watch for changes in computed totals and update financial_info
    watch(totalAsset, (newValue) => {
        if (application.value.company_borrowers && application.value.company_borrowers.length > 0) {
            application.value.company_borrowers[0].financial_info.assets = newValue;
        }
    });
    
    watch(totalLiability, (newValue) => {
        if (application.value.company_borrowers && application.value.company_borrowers.length > 0) {
            application.value.company_borrowers[0].financial_info.liabilities = newValue;
        }
    });    
    const guarantorAsset = ref({
        address1: "",
        address1Value: "",
        address1Owing: "",
        address1G1: false,
        address1G2: false,
        address2: "",
        address2Value: "",
        address2Owing: "",
        address2G1: false,
        address2G2: false,
        address3: "",
        address3Value: "",
        address3Owing: "",
        address3G1: false,
        address3G2: false,
        address4: "",
        address4Value: "",
        address4Owing: "",
        address4G1: false,
        address4G2: false,
        vehicleValue: "",
        vehicleOwing: "",
        vehicleG1: false,
        vehicleG2: false,
        savingValue: "",
        savingOwing: "",
        savingG1: false,
        savingG2: false,
        shareValue: "",
        shareOwing: "",
        shareG1: false,
        shareG2: false,
        cardValue: "",
        cardOwing: "",
        cardG1: false,
        cardG2: false,
        creditorValue: "",
        creditorOwing: "",
        creditorG1: false,
        creditorG2: false,
        otherValue: "",
        otherOwing: "",
        otherG1: false,
        otherG2: false,
        totalValue: "",
        totalOwing: ""
    })

    const emit = defineEmits(['close', 'minimize'])

    const handleClose = () => {
        emit('close')
    }
    const handleMinimize = () => {
        emit('minimize')
    }
    const addDirector = () => {
        application.value.company_borrowers[0].directors.push(createDirector())
    }
    const removeDirector = (idx) => {
        application.value.company_borrowers[0].directors.splice(idx, 1)
    }
    const addAsset = () => {
        application.value.company_borrowers[0].assets.push(createCompanyAsset())
    }
    const removeAsset = () => {
        application.value.company_borrowers[0].assets.pop()
    }
    const addLiability = () => {
        application.value.company_borrowers[0].liabilities.push(createCompanyLiability())
    }
    const removeLiability = () => {
        application.value.company_borrowers[0].liabilities.pop()
    }
    const addBorrower = () => {
        application.value.borrowers.push(createBorrower())
    }
    const removeBorrower = (idx) => {
        application.value.borrowers.splice(idx, 1)
    }
    const addGuarantor = () => {
        application.value.guarantors.push(createGuarantor())
    }
    const removeGuarantor = (idx) => {
        application.value.guarantors.splice(idx, 1)
    }
    const addSecurity = () => {
        application.value.security_properties.push(createSecurity())
    }
    const removeSecurity = (idx) => {
        application.value.security_properties.splice(idx, 1)
    }
    const addRequirement = () => {
        application.value.loan_requirements.push(createRequirement())
    }
    const removeRequirement = () => {
        application.value.loan_requirements.pop()
    }
    const isCompanyValid = computed(() => {
        if (!application.value?.company_borrowers?.[0]) return false;
        
        const company = application.value.company_borrowers[0];
        return company.company_name && company.company_abn && company.industry_type;
    })
    
    const isCompanyAssetValid = computed(() => {
        if (!application.value?.company_borrowers?.[0]?.assets) return false;
        
        const assets = application.value.company_borrowers[0].assets;
        return assets.length > 0 && assets.every(asset => asset.asset_type && asset.value);
    })
    
    const isEnquiryValid = computed(() => {
        // Check if all required solvency fields are filled
        return application.value.has_pending_litigation !== null &&
               application.value.has_unsatisfied_judgements !== null &&
               application.value.has_been_bankrupt !== null &&
               application.value.has_been_refused_credit !== null;
    })
    
    const isIndividualValid = computed(() => {
        if (!application.value?.borrowers) return false;
        
        return application.value.borrowers.length > 0 && 
               application.value.borrowers.every(borrower => 
                   borrower.first_name && borrower.last_name && borrower.email
               );
    })
    
    const isGuarantorAssetValid = computed(() => {
        // Check if at least one guarantor asset is defined
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
    })
    
    const isSecurityValid = computed(() => {
        if (!application.value?.security_properties) return false;
        
        return application.value.security_properties.length > 0 && 
               application.value.security_properties.every(property => 
                   property.address_street_name && property.address_suburb && 
                   property.address_state && property.address_postcode
               );
    })
    
    const isLoanDetailValid = computed(() => {
        return application.value.loan_amount && 
               application.value.repayment_frequency && 
               application.value.application_type && 
               application.value.product_id;
    })
    
    const isRequirementValid = computed(() => {
        if (!application.value?.loan_requirements) return false;
        
        return application.value.loan_requirements.length > 0 && 
               application.value.loan_requirements.every(req => req.description && req.amount);
    })
    
    const isExitValid = computed(() => {
        return application.value.exit_strategy && 
               (application.value.exit_strategy !== 'other' || application.value.exit_strategy_details);
    })
    
    // Format date to YYYY-MM-DD
    const formatDate = (dateString) => {
        if (!dateString) return null;
        try {
            const date = new Date(dateString);
            return date.toISOString().split('T')[0]; // Returns YYYY-MM-DD
        } catch (e) {
            return null;
        }
    };
    
    // Format all dates in the application object
    const formatDates = (obj) => {
        if (!obj || typeof obj !== 'object') return obj;
        
        // Create a copy to avoid modifying the original
        const result = Array.isArray(obj) ? [...obj] : {...obj};
        
        // Process each property
        Object.keys(result).forEach(key => {
            // If it's a date field, format it
            if (key.includes('date') && result[key]) {
                result[key] = formatDate(result[key]);
            } 
            // If it's an object or array, recursively format dates
            else if (typeof result[key] === 'object' && result[key] !== null) {
                result[key] = formatDates(result[key]);
            }
        });
        
        return result;
    };
    
    // Transform empty strings to null for optional fields
    const transformEmptyToNull = (obj) => {
        if (!obj || typeof obj !== 'object') return obj;
        
        // Create a copy to avoid modifying the original
        const result = Array.isArray(obj) ? [...obj] : {...obj};
        
        // Process each property
        Object.keys(result).forEach(key => {
            // If it's an empty string, set to null
            if (result[key] === '') {
                result[key] = null;
            } 
            // If it's an object or array, recursively transform
            else if (typeof result[key] === 'object' && result[key] !== null) {
                result[key] = transformEmptyToNull(result[key]);
            }
        });
        
        return result;
    };
    
    // Validate and format application data
    const validateAndFormatApplication = () => {
        // Required fields validation based on schema
        const requiredFields = [
            'reference_number',
            'loan_amount',
            'repayment_frequency',
            'application_type',
            'product_id',
            'stage'
        ];
        
        const missingFields = requiredFields.filter(field => !application.value[field]);
        
        if (missingFields.length > 0) {
            ElMessage.warning(`Please fill in all required fields: ${missingFields.join(', ')}`);
            return false;
        }
        
        // Format dates using the utility function
        application.value = formatDates(application.value);
        
        // Transform empty strings to null for optional fields
        application.value = transformEmptyToNull(application.value);
        
        // Validate repayment_frequency against schema choices
        const validRepaymentFrequencies = ["weekly", "fortnightly", "monthly", "quarterly", "annually"];
        if (!validRepaymentFrequencies.includes(application.value.repayment_frequency)) {
            application.value.repayment_frequency = "monthly"; // Default to monthly
        }
        
        // Validate application_type against schema choices
        const validApplicationTypes = ["residential", "commercial", "construction", "refinance", "investment", "smsf"];
        if (application.value.application_type && !validApplicationTypes.includes(application.value.application_type)) {
            application.value.application_type = "residential"; // Default to residential
        }
        
        // Validate exit_strategy against schema choices
        const validExitStrategies = ["sale", "refinance", "income", "other"];
        if (application.value.exit_strategy && !validExitStrategies.includes(application.value.exit_strategy)) {
            application.value.exit_strategy = "other";
        }
        
        // Validate borrowers
        if (application.value.borrowers && application.value.borrowers.length > 0) {
            application.value.borrowers = application.value.borrowers.filter(borrower => 
                borrower.first_name || borrower.last_name || borrower.email
            ).map(borrower => {
                // Validate marital_status against schema choices
                const validMaritalStatuses = ["single", "married", "de_facto", "divorced", "widowed"];
                if (borrower.marital_status && !validMaritalStatuses.includes(borrower.marital_status)) {
                    borrower.marital_status = null;
                }
                
                // Validate residency_status against schema choices
                const validResidencyStatuses = ["citizen", "permanent_resident", "temporary_resident", "foreign_investor"];
                if (borrower.residency_status && !validResidencyStatuses.includes(borrower.residency_status)) {
                    borrower.residency_status = null;
                }
                
                return borrower;
            });
        }
        
        // Validate guarantors
        if (application.value.guarantors && application.value.guarantors.length > 0) {
            application.value.guarantors = application.value.guarantors.filter(guarantor => 
                guarantor.first_name || guarantor.last_name || guarantor.email
            ).map(guarantor => {
                // Validate guarantor_type against schema choices
                const validGuarantorTypes = ["individual", "company"];
                if (!validGuarantorTypes.includes(guarantor.guarantor_type)) {
                    guarantor.guarantor_type = "individual"; // Default to individual
                }
                
                // Validate title against schema choices
                const validTitles = ["mr", "mrs", "ms", "miss", "dr", "other"];
                if (guarantor.title && !validTitles.includes(guarantor.title)) {
                    guarantor.title = null;
                }
                
                // Validate employment_type against schema choices
                const validEmploymentTypes = ["full_time", "part_time", "casual", "contract"];
                if (guarantor.employment_type && !validEmploymentTypes.includes(guarantor.employment_type)) {
                    guarantor.employment_type = null;
                }
                
                // Ensure borrower and application are set
                if (!guarantor.borrower && application.value.borrowers.length > 0) {
                    guarantor.borrower = 1; // Default to first borrower
                }
                
                if (!guarantor.application) {
                    guarantor.application = 1; // Default application ID
                }
                
                return guarantor;
            });
        }
        
        // Validate company_borrowers
        if (application.value.company_borrowers && application.value.company_borrowers.length > 0) {
            application.value.company_borrowers = application.value.company_borrowers.filter(company => 
                company.company_name || company.company_abn
            ).map(company => {
                // Validate industry_type against schema choices
                const validIndustryTypes = ["agriculture", "mining", "manufacturing", "construction", "retail", "transport", 
                                        "hospitality", "finance", "real_estate", "professional", "education", "healthcare", "arts", "other"];
                if (company.industry_type && !validIndustryTypes.includes(company.industry_type)) {
                    company.industry_type = "other";
                }
                
                // Format financial values
                if (company.financial_info) {
                    company.financial_info = {
                        ...company.financial_info,
                        annual_revenue: parseFloat(company.financial_info.annual_revenue) || 0,
                        net_profit: parseFloat(company.financial_info.net_profit) || 0
                    };
                }
                
                // Validate assets
                if (company.assets && company.assets.length > 0) {
                    company.assets = company.assets.filter(asset => asset.asset_type || asset.description).map(asset => {
                        // Validate asset_type against schema choices
                        const validAssetTypes = ["Property", "Vehicle", "Savings", "Investment Shares", "Credit Card", "Other Creditor", "Other", "To be refinanced"];
                        
                        return {
                            ...asset,
                            asset_type: asset.asset_type && !validAssetTypes.includes(asset.asset_type) ? "Other" : asset.asset_type,
                            value: parseFloat(asset.value) || 0,
                            amount_owing: parseFloat(asset.amount_owing) || 0,
                            to_be_refinanced: asset.to_be_refinanced === "" ? null : asset.to_be_refinanced
                        };
                    });
                }
                
                // Validate liabilities
                if (company.liabilities && company.liabilities.length > 0) {
                    company.liabilities = company.liabilities.filter(liability => liability.liability_type || liability.description).map(liability => {
                        // Validate liability_type against schema choices
                        const validLiabilityTypes = ["mortgage", "personal_loan", "car_loan", "credit_card", "tax_debt", "other_creditor", "other"];
                        
                        return {
                            ...liability,
                            liability_type: liability.liability_type && !validLiabilityTypes.includes(liability.liability_type) ? "other" : liability.liability_type,
                            amount: parseFloat(liability.amount) || 0,
                            monthly_payment: parseFloat(liability.monthly_payment) || 0,
                            to_be_refinanced: liability.to_be_refinanced === "" ? null : liability.to_be_refinanced
                        };
                    });
                }
                
                return company;
            });
        }
        
        // Validate security_properties
        if (application.value.security_properties && application.value.security_properties.length > 0) {
            application.value.security_properties = application.value.security_properties.filter(property => 
                property.address_street_name || property.address_suburb
            ).map(property => {
                // Validate property_type against schema choices
                const validPropertyTypes = ["residential", "commercial", "industrial", "retail", "land", "rural", "other"];
                if (property.property_type && !validPropertyTypes.includes(property.property_type)) {
                    property.property_type = "residential"; // Default to residential
                }
                
                return {
                    ...property,
                    // Convert string numbers to integers
                    bedrooms: parseInt(property.bedrooms) || null,
                    bathrooms: parseInt(property.bathrooms) || null,
                    car_spaces: parseInt(property.car_spaces) || null,
                    
                    // Set boolean fields to null if empty string
                    is_single_story: property.is_single_story === "" ? null : property.is_single_story,
                    has_garage: property.has_garage === "" ? null : property.has_garage,
                    has_carport: property.has_carport === "" ? null : property.has_carport,
                    has_off_street_parking: property.has_off_street_parking === "" ? null : property.has_off_street_parking,
                    
                    // Convert string numbers to floats
                    current_debt_position: parseFloat(property.current_debt_position) || null,
                    estimated_value: parseFloat(property.estimated_value) || null,
                    purchase_price: parseFloat(property.purchase_price) || null
                };
            });
        }
        
        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (application.value.qs_email && !emailRegex.test(application.value.qs_email)) {
            application.value.qs_email = null; // Clear invalid email
        }
        if (application.value.valuer_email && !emailRegex.test(application.value.valuer_email)) {
            application.value.valuer_email = null; // Clear invalid email
        }
        
        // Validate funding_calculation_input
        if (application.value.funding_calculation_input) {
            application.value.funding_calculation_input = {
                ...application.value.funding_calculation_input,
                monthly_line_fee_rate: parseFloat(application.value.funding_calculation_input.monthly_line_fee_rate) || 0,
                establishment_fee_rate: parseFloat(application.value.funding_calculation_input.establishment_fee_rate) || 0,
                capped_interest_months: parseInt(application.value.funding_calculation_input.capped_interest_months) || 9,
                brokerage_fee_rate: parseFloat(application.value.funding_calculation_input.brokerage_fee_rate) || 0,
                application_fee: parseFloat(application.value.funding_calculation_input.application_fee) || 0,
                due_diligence_fee: parseFloat(application.value.funding_calculation_input.due_diligence_fee) || 0,
                legal_fee_before_gst: parseFloat(application.value.funding_calculation_input.legal_fee_before_gst) || 0,
                valuation_fee: parseFloat(application.value.funding_calculation_input.valuation_fee) || 0,
                monthly_account_fee: parseFloat(application.value.funding_calculation_input.monthly_account_fee) || 0,
                working_fee: parseFloat(application.value.funding_calculation_input.working_fee) || 0
            };
        }
        
        return true;
    };


    
    // Initialize data when component mounts
    onMounted(() => {
        console.log("AddApplication component mounted");
    });

    const handleSave = async () => {
        try {
            if (!validateAndFormatApplication()) {
                return;
            }
            
            isSubmitting.value = true;
            
            // Create a deep copy of the application to avoid proxy issues
            const applicationData = JSON.parse(JSON.stringify(application.value));
            
            // CRITICAL FIX: For guarantors in new applications, set borrower and application to null
            if (applicationData.guarantors && applicationData.guarantors.length > 0) {
                applicationData.guarantors.forEach(guarantor => {
                    // For new applications, set these fields to null
                    // The backend will assign the proper values
                    guarantor.borrower = null;
                    guarantor.application = null;
                    
                    // Remove any nested objects that might cause issues
                    delete guarantor.borrower_details;
                    delete guarantor.application_details;
                });
            }
            
            // Transform guarantor assets from frontend format to backend format
            applicationData.guarantors = transformGuarantorAssets(guarantorAsset.value, applicationData.guarantors);
            
            // Manually compute and add the financial totals for API submission
            if (applicationData.company_borrowers && applicationData.company_borrowers.length > 0) {
                applicationData.company_borrowers.forEach(company => {
                    // Manually calculate assets total
                    company.financial_info.assets = company.assets
                        .map(a => parseFloat(a.value) || 0)
                        .reduce((sum, v) => sum + v, 0);
                    
                    // Manually calculate liabilities total
                    company.financial_info.liabilities = company.liabilities
                        .map(l => parseFloat(l.amount) || 0)
                        .reduce((sum, v) => sum + v, 0);
                });
            }
            
            let err, res;
            console.log("Creating new application");
            [err, res] = await api.createApplicationWithCascade(applicationData);

            if (!err) {
                ElMessage.success('Application created successfully');
                handleClose();
            } else {
                // Enhanced error handling
                if (typeof err === 'object' && err !== null) {
                    // Process field-level errors
                    const errorMessages = [];
                    
                    // Process top-level errors
                    Object.entries(err).forEach(([field, messages]) => {
                        if (Array.isArray(messages)) {
                            errorMessages.push(`${field}: ${messages.join(', ')}`);
                        } else if (typeof messages === 'string') {
                            errorMessages.push(`${field}: ${messages}`);
                        } else if (typeof messages === 'object' && messages !== null) {
                            // Handle nested errors (e.g., for borrowers, guarantors, etc.)
                            Object.entries(messages).forEach(([nestedField, nestedMessages]) => {
                                if (Array.isArray(nestedMessages)) {
                                    errorMessages.push(`${field}.${nestedField}: ${nestedMessages.join(', ')}`);
                                } else if (typeof nestedMessages === 'string') {
                                    errorMessages.push(`${field}.${nestedField}: ${nestedMessages}`);
                                }
                            });
                        }
                    });
                    
                    // Display error messages
                    if (errorMessages.length > 0) {
                        ElMessage({
                            message: `Validation errors:\n${errorMessages.join('\n')}`,
                            type: 'error',
                            duration: 5000,
                            showClose: true,
                            dangerouslyUseHTMLString: false
                        });
                    } else {
                        ElMessage.error(`Failed to ${props.isEditMode ? 'update' : 'create'} application: Validation errors`);
                    }
                } else {
                    ElMessage.error(`Failed to ${props.isEditMode ? 'update' : 'create'} application: Unknown error`);
                }
                
                console.error("API errors:", err);
            }
        } catch (error) {
            console.error("Exception during application operation:", error);
            ElMessage.error(`An unexpected error occurred: ${error.message || 'Unknown error'}`);
        } finally {
            isSubmitting.value = false;
        }
    }
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
        flex-direction: row;
        align-items: center;
        gap: 10px;
        padding-left: 5px;
    }
    .title p {
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 400;
        line-height: 12px;
    }
    .buttons {
        width: 100%;
        padding: 10px;
        margin-top: auto;
        display: flex;
        flex-direction: row;
        justify-content: end;
        align-items: center;
        border-top: 1.5px solid #E1E1E1;
        gap: 10px;
    }
</style>
