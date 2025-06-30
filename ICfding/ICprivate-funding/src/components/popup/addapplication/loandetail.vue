<template>
    <div class="form">
        <div class="long_item">
            <h1>Loan Details</h1>
        </div>
        <div class="item">
            <p>Application Type</p>
            <el-select v-model="detail.application_type" placeholder="Select application type">
                <el-option value="acquisition" label="Acquisition" />
                <el-option value="refinance" label="Refinance" />
                <el-option value="equity_release" label="Equity Release" />
                <el-option value="refinance_equity_release" label="Refinance & Equity Release" />
                <el-option value="second_mortgage" label="2nd Mortgage" />
                <el-option value="caveat" label="Caveat" />
                <el-option value="other" label="Other" />
            </el-select>
            <span class="hint">Select the type of loan application</span>
        </div>
        <div class="item" v-if="detail.application_type === 'other'">
            <p>Other Application Type <span class="required">*</span></p>
            <el-input v-model="detail.application_type_other" placeholder="Specify other application type" />
            <span class="hint">Required if 'Other' is selected</span>
        </div>
        <div class="item">
            <p>Estimated Settlement Date <span class="required">*</span></p>
            <el-date-picker 
                v-model="detail.estimated_settlement_date" 
                type="date" 
                placeholder="YYYY-MM-DD" 
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD" />
            <span class="hint">Date must be in YYYY-MM-DD format</span>
        </div>
        <div class="item">
            <p>Net Loan Required ($) <span class="required">*</span></p>
            <el-input v-model="detail.loan_amount" type="number" placeholder="e.g. 500000" />
            <span class="hint">Enter the loan amount (max 10 digits before decimal)</span>
        </div>
        <div class="item">
            <p>Term Required (months)</p>
            <el-input v-model="detail.loan_term" type="number" placeholder="e.g. 12" />
            <span class="hint">Enter the loan term in months</span>
        </div>
        <div class="item">
            <p>Capitalised Interest Term (months)</p>
            <el-input v-model="detail.capitalised_interest_term" type="number" placeholder="e.g. 6" />
            <span class="hint">Enter the capitalised interest term in months</span>
        </div>
        <div class="item">
            <p>Expected Repayment Frequency <span class="required">*</span></p>
            <el-select v-model="detail.repayment_frequency" placeholder="Select frequency">
                <el-option value="weekly" label="Weekly" />
                <el-option value="fortnightly" label="Fortnightly" />
                <el-option value="monthly" label="Monthly" />
                <el-option value="quarterly" label="Quarterly" />
                <el-option value="annually" label="Annually" />
            </el-select>
            <span class="hint">How often repayments will be made</span>
        </div>
        <div class="item">
            <p>Reference Number <span class="required">*</span></p>
            <el-input v-model="detail.reference_number" placeholder="e.g. REF12345" />
            <span class="hint">Unique reference for this application (max 20 characters)</span>
        </div>
        <div class="item">
            <p>Product ID <span class="required">*</span></p>
            <el-select v-model="detail.product_id" placeholder="Select a product" filterable clearable>
                <el-option 
                    v-for="product in products" 
                    :key="product.id" 
                    :value="product.id.toString()" 
                    :label="product.name">
                    <div style="display: flex; flex-direction: column;">
                        <span style="font-weight: bold;">{{ product.name }}</span>
                        <span style="font-size: 12px; color: #8c8c8c;">ID: {{ product.id }}</span>
                    </div>
                </el-option>
            </el-select>
            <span class="hint">Select a product from the dropdown</span>
        </div>
        <div class="item">
            <p>Expected Interest Rate (p.a) (%)</p>
            <el-input v-model="detail.interest_rate" type="number" step="0.01" placeholder="e.g. 5.5" />
            <span class="hint">Enter rate as percentage (max 3 digits before decimal)</span>
        </div>
        <div class="prior">
            <el-checkbox v-model="detail.prior_application">Prior Application</el-checkbox>
            <el-input v-model="detail.prior_application_details" placeholder="Details of prior application" :disabled="!detail.prior_application"/>
            <span class="hint">Check if this is related to a previous application</span>
        </div>
        <div class="prior">
            <el-checkbox v-model="detail.has_other_credit_providers">Has any application in respect of this loan been submitted by you or any other person to other credit providers?</el-checkbox>
            <el-input v-if="detail.has_other_credit_providers" v-model="detail.other_credit_providers_details" placeholder="Please provide details" />
            <span class="hint">If yes, provide details of other credit provider applications</span>
        </div>
        <div class="long_item">
            <h1>Valuer</h1>
        </div>
        <div class="item">
            <p>Select Valuer</p>
            <el-select v-model="detail.valuer" placeholder="Select a valuer" filterable clearable>
                <el-option value="add_new" label="+ Add New Valuer">
                    <div style="display: flex; align-items: center; color: #409EFF;">
                        <span style="margin-left: 5px;">+ Add New Valuer</span>
                    </div>
                </el-option>
                <el-option 
                    v-for="valuer in valuers" 
                    :key="valuer.id" 
                    :value="valuer.id" 
                    :label="valuer.display_name">
                    <div style="display: flex; flex-direction: column;">
                        <span style="font-weight: bold;">{{ valuer.company_name }}</span>
                        <span style="font-size: 12px; color: #8c8c8c;">{{ valuer.contact_name }} - {{ valuer.phone }}</span>
                    </div>
                </el-option>
            </el-select>
            <span class="hint">Select an existing valuer or add a new one</span>
        </div>
        <div v-if="detail.valuer === 'add_new' || showValuerForm" class="valuer-form" style="grid-column: 1 / 3; display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px 20px; margin-top: 10px; padding: 15px; border: 1px solid #e1e1e1; border-radius: 5px;">
            <div class="item">
                <p>Company Name <span class="required">*</span></p>
                <el-input v-model="newValuer.company_name" placeholder="Valuation company name" />
                <span class="hint">Name of the valuation company</span>
            </div>
            <div class="item">
                <p>Contact Name <span class="required">*</span></p>
                <el-input v-model="newValuer.contact_name" placeholder="Contact person name" />
                <span class="hint">Name of the contact person</span>
            </div>
            <div class="item">
                <p>Phone Number <span class="required">*</span></p>
                <el-input v-model="newValuer.phone" placeholder="e.g. +61 2 1234 5678" />
                <span class="hint">Contact phone number</span>
            </div>
            <div class="item">
                <p>Email Address <span class="required">*</span></p>
                <el-input v-model="newValuer.email" type="email" placeholder="example@domain.com" />
                <span class="hint">Contact email address</span>
            </div>
            <div class="item" style="grid-column: 1 / 3;">
                <p>Address</p>
                <el-input v-model="newValuer.address" type="textarea" :rows="2" placeholder="Company address" />
                <span class="hint">Optional company address</span>
            </div>
            <div class="item" style="grid-column: 1 / 3;">
                <p>Notes</p>
                <el-input v-model="newValuer.notes" type="textarea" :rows="2" placeholder="Additional notes" />
                <span class="hint">Optional notes about this valuer</span>
            </div>
            <div class="item" style="grid-column: 1 / 3; display: flex; gap: 10px; justify-content: flex-end;">
                <el-button @click="cancelNewValuer">Cancel</el-button>
                <el-button type="primary" @click="saveNewValuer" :loading="savingValuer">Save Valuer</el-button>
            </div>
        </div>
        <div class="long_item">
            <h1>Quantity Surveyor</h1>
        </div>
        <div class="item">
            <p>Select Quantity Surveyor</p>
            <el-select v-model="detail.quantity_surveyor" placeholder="Select a quantity surveyor" filterable clearable>
                <el-option value="add_new" label="+ Add New QS">
                    <div style="display: flex; align-items: center; color: #409EFF;">
                        <span style="margin-left: 5px;">+ Add New Quantity Surveyor</span>
                    </div>
                </el-option>
                <el-option 
                    v-for="qs in quantitySurveyors" 
                    :key="qs.id" 
                    :value="qs.id" 
                    :label="qs.display_name">
                    <div style="display: flex; flex-direction: column;">
                        <span style="font-weight: bold;">{{ qs.company_name }}</span>
                        <span style="font-size: 12px; color: #8c8c8c;">{{ qs.contact_name }} - {{ qs.phone }}</span>
                    </div>
                </el-option>
            </el-select>
            <span class="hint">Select an existing quantity surveyor or add a new one</span>
        </div>
        <div v-if="detail.quantity_surveyor === 'add_new' || showQsForm" class="qs-form" style="grid-column: 1 / 3; display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px 20px; margin-top: 10px; padding: 15px; border: 1px solid #e1e1e1; border-radius: 5px;">
            <div class="item">
                <p>Company Name <span class="required">*</span></p>
                <el-input v-model="newQs.company_name" placeholder="QS company name" />
                <span class="hint">Name of the QS company</span>
            </div>
            <div class="item">
                <p>Contact Name <span class="required">*</span></p>
                <el-input v-model="newQs.contact_name" placeholder="Contact person name" />
                <span class="hint">Name of the contact person</span>
            </div>
            <div class="item">
                <p>Phone Number <span class="required">*</span></p>
                <el-input v-model="newQs.phone" placeholder="e.g. +61 2 1234 5678" />
                <span class="hint">Contact phone number</span>
            </div>
            <div class="item">
                <p>Email Address <span class="required">*</span></p>
                <el-input v-model="newQs.email" type="email" placeholder="example@domain.com" />
                <span class="hint">Contact email address</span>
            </div>
            <div class="item" style="grid-column: 1 / 3;">
                <p>Address</p>
                <el-input v-model="newQs.address" type="textarea" :rows="2" placeholder="Company address" />
                <span class="hint">Optional company address</span>
            </div>
            <div class="item" style="grid-column: 1 / 3;">
                <p>Notes</p>
                <el-input v-model="newQs.notes" type="textarea" :rows="2" placeholder="Additional notes" />
                <span class="hint">Optional notes about this quantity surveyor</span>
            </div>
            <div class="item" style="grid-column: 1 / 3; display: flex; gap: 10px; justify-content: flex-end;">
                <el-button @click="cancelNewQs">Cancel</el-button>
                <el-button type="primary" @click="saveNewQs" :loading="savingQs">Save Quantity Surveyor</el-button>
            </div>
        </div>
        <div class="long_item">
            <h1>Loan Purpose</h1>
        </div>
        <div class="item">
            <p>Purpose <span class="required">*</span></p>
            <el-select v-model="detail.loan_purpose" placeholder="Select loan purpose">
                <el-option value="purchase" label="Purchase" />
                <el-option value="refinance" label="Refinance" />
                <el-option value="construction" label="Construction" />
                <el-option value="equity_release" label="Equity Release" />
                <el-option value="debt_consolidation" label="Debt Consolidation" />
                <el-option value="business_expansion" label="Business Expansion" />
                <el-option value="working_capital" label="Working Capital" />
                <el-option value="other" label="Other" />
            </el-select>
            <span class="hint">Primary purpose of the loan</span>
        </div>
        <div class="item" v-if="detail.loan_purpose === 'other'">
            <p>Other Purpose <span class="required">*</span></p>
            <el-input v-model="otherPurpose" placeholder="Specify other purpose" @input="updateOtherPurpose" />
            <span class="hint">Required if 'Other' is selected</span>
        </div>
        <div class="long_item">
            <h1>Additional Comments</h1>
        </div>
        <div class="long_item">
            <p>Please provide any additional relevant information / comments regarding this application</p>
            <el-input v-model="detail.additional_comments" type="textarea" :rows="3" placeholder="Enter any additional information here" />
            <span class="hint">Optional additional information about the application</span>
        </div>
    </div>
</template>

<script setup>
    import { ref, watch, onMounted } from 'vue';
    import { ElMessage } from 'element-plus';
    import { api } from '@/api';

    const props = defineProps({
        detail: Object
    });

    // Create local ref for other purpose
    const otherPurpose = ref("");

    // Reactive data for valuers and quantity surveyors
    const valuers = ref([]);
    const quantitySurveyors = ref([]);
    const products = ref([]);
    const showValuerForm = ref(false);
    const showQsForm = ref(false);
    const savingValuer = ref(false);
    const savingQs = ref(false);

    // Forms for new valuer and QS
    const newValuer = ref({
        company_name: '',
        contact_name: '',
        phone: '',
        email: '',
        address: '',
        notes: ''
    });

    const newQs = ref({
        company_name: '',
        contact_name: '',
        phone: '',
        email: '',
        address: '',
        notes: ''
    });

    // Load valuers and quantity surveyors
    const loadValuers = async () => {
        try {
            const [err, data] = await api.valuers();
            if (!err && data) {
                valuers.value = data.results || data;
            }
        } catch (error) {
            console.error('Error loading valuers:', error);
        }
    };

    const loadQuantitySurveyors = async () => {
        try {
            const [err, data] = await api.quantitySurveyors();
            if (!err && data) {
                quantitySurveyors.value = data.results || data;
            }
        } catch (error) {
            console.error('Error loading quantity surveyors:', error);
        }
    };

    // Load products
    const loadProducts = async () => {
        try {
            const [err, data] = await api.getProducts();
            if (!err && data) {
                products.value = data.results || data;
            }
        } catch (error) {
            console.error('Error loading products:', error);
        }
    };

    // Save new valuer
    const saveNewValuer = async () => {
        // Validate required fields
        if (!newValuer.value.company_name || !newValuer.value.contact_name || 
            !newValuer.value.phone || !newValuer.value.email) {
            ElMessage.error('Please fill in all required fields for the valuer');
            return;
        }

        savingValuer.value = true;
        try {
            const [err, data] = await api.addValuer(newValuer.value);
            if (!err && data) {
                ElMessage.success('Valuer saved successfully');
                // Add display_name field to match the list serializer format
                const valuerWithDisplayName = {
                    ...data,
                    display_name: `${data.company_name} - ${data.contact_name}`
                };
                // Add to list and select it
                valuers.value.push(valuerWithDisplayName);
                props.detail.valuer = data.id;
                // Reset form
                newValuer.value = {
                    company_name: '',
                    contact_name: '',
                    phone: '',
                    email: '',
                    address: '',
                    notes: ''
                };
                showValuerForm.value = false;
            } else {
                ElMessage.error('Failed to save valuer: ' + (err.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error saving valuer:', error);
            ElMessage.error('Error saving valuer');
        } finally {
            savingValuer.value = false;
        }
    };

    // Save new quantity surveyor
    const saveNewQs = async () => {
        // Validate required fields
        if (!newQs.value.company_name || !newQs.value.contact_name || 
            !newQs.value.phone || !newQs.value.email) {
            ElMessage.error('Please fill in all required fields for the quantity surveyor');
            return;
        }

        savingQs.value = true;
        try {
            const [err, data] = await api.addQuantitySurveyor(newQs.value);
            if (!err && data) {
                ElMessage.success('Quantity Surveyor saved successfully');
                // Add display_name field to match the list serializer format
                const qsWithDisplayName = {
                    ...data,
                    display_name: `${data.company_name} - ${data.contact_name}`
                };
                // Add to list and select it
                quantitySurveyors.value.push(qsWithDisplayName);
                props.detail.quantity_surveyor = data.id;
                // Reset form
                newQs.value = {
                    company_name: '',
                    contact_name: '',
                    phone: '',
                    email: '',
                    address: '',
                    notes: ''
                };
                showQsForm.value = false;
            } else {
                ElMessage.error('Failed to save quantity surveyor: ' + (err.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error saving quantity surveyor:', error);
            ElMessage.error('Error saving quantity surveyor');
        } finally {
            savingQs.value = false;
        }
    };

    // Cancel new valuer
    const cancelNewValuer = () => {
        newValuer.value = {
            company_name: '',
            contact_name: '',
            phone: '',
            email: '',
            address: '',
            notes: ''
        };
        props.detail.valuer = null;
        showValuerForm.value = false;
    };

    // Cancel new QS
    const cancelNewQs = () => {
        newQs.value = {
            company_name: '',
            contact_name: '',
            phone: '',
            email: '',
            address: '',
            notes: ''
        };
        props.detail.quantity_surveyor = null;
        showQsForm.value = false;
    };

    // Initialize values from props
    onMounted(() => {
        // Load valuers and QS
        loadValuers();
        loadQuantitySurveyors();
        loadProducts();

        // Check if loan_purpose is already set and is a valid enum value
        const validPurposes = ["purchase", "refinance", "construction", "equity_release", 
                              "debt_consolidation", "business_expansion", "working_capital", "other"];
        
        if (props.detail.loan_purpose && validPurposes.includes(props.detail.loan_purpose)) {
            // If it's a valid enum value, keep it as is
        } else if (props.detail.loan_purpose) {
            // If it's set but not a valid enum, assume it's a custom value
            otherPurpose.value = props.detail.loan_purpose;
            props.detail.loan_purpose = "other";
        } else {
            // Set default loan purpose if not set
            props.detail.loan_purpose = "refinance";
        }
        
        // Set default repayment frequency if not set
        if (!props.detail.repayment_frequency) {
            props.detail.repayment_frequency = "monthly";
        }
    });

    // Function to update the loan purpose when "other" is selected
    const updateOtherPurpose = () => {
        if (props.detail.loan_purpose === 'other' && otherPurpose.value) {
            // Store the custom value in the loan_purpose field
            props.detail.custom_loan_purpose = otherPurpose.value;
        }
    };

    // Watch for changes in the loan purpose
    watch(() => props.detail.loan_purpose, (newVal) => {
        if (newVal !== 'other') {
            // Reset the other purpose input when a predefined purpose is selected
            otherPurpose.value = "";
        }
    });

    // Watch for changes in the application type
    watch(() => props.detail.application_type, (newVal) => {
        if (newVal !== 'other') {
            // Reset the other application type input when a predefined type is selected
            props.detail.application_type_other = "";
        }
    });

    // Watch for valuer selection changes
    watch(() => props.detail.valuer, (newVal) => {
        if (newVal === 'add_new') {
            showValuerForm.value = true;
        } else {
            showValuerForm.value = false;
        }
    });

    // Watch for QS selection changes
    watch(() => props.detail.quantity_surveyor, (newVal) => {
        if (newVal === 'add_new') {
            showQsForm.value = true;
        } else {
            showQsForm.value = false;
        }
    });
</script>

<style scoped>
    .form {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px 20px;
    }
    .item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    p {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
        margin: 0;
    }
    .long_item {
        grid-column: 1 / 3;
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .group {
        grid-column: 1 / 3;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .line {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    .prior {
        grid-column: 1 / 3;
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }
    :deep(.el-date-editor) {
        --el-date-editor-width: 100%;
    }
    :deep(.el-select) {
        width: 100%;
    }
    .hint {
        color: #8c8c8c;
        font-size: 0.7rem;
        font-style: italic;
    }
    .required {
        color: #f56c6c;
        margin-left: 2px;
    }
</style>
