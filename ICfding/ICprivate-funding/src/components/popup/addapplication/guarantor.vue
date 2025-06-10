<template>
    <div class="form">
        <div v-for="(item, index) in guarantors" :key="index" class="guarantor">
            <div class="item">
                <p>Guarantor Type <span class="required">*</span></p>
                <el-select v-model="item.guarantor_type" placeholder="Select type">
                    <el-option value="individual" label="Individual" />
                    <el-option value="company" label="Company" />
                </el-select>
                <span class="hint">Type of guarantor</span>
            </div>
            <div class="item">
                <p>Title</p>
                <el-select v-model="item.title" placeholder="Select title">
                    <el-option value="mr" label="Mr" />
                    <el-option value="mrs" label="Mrs" />
                    <el-option value="ms" label="Ms" />
                    <el-option value="miss" label="Miss" />
                    <el-option value="dr" label="Dr" />
                    <el-option value="other" label="Other" />
                </el-select>
                <span class="hint">Title/honorific</span>
            </div>
            <div class="item">
                <p>First Name <span class="required">*</span></p>
                <el-input v-model="item.first_name" placeholder="Enter first name" />
                <span class="hint">Legal first name</span>
            </div>
            <div class="item">
                <p>Last Name <span class="required">*</span></p>
                <el-input v-model="item.last_name" placeholder="Enter last name" />
                <span class="hint">Legal last name</span>
            </div>
            <div class="item">
                <p>Date of Birth <span class="required">*</span></p>
                <el-date-picker 
                    v-model="item.date_of_birth" 
                    type="date" 
                    placeholder="YYYY-MM-DD" 
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD" />
                <span class="hint">Date must be in YYYY-MM-DD format</span>
            </div>
            <div class="item">
                <p>Driver's License No</p>
                <el-input v-model="item.drivers_licence_no" placeholder="e.g. 12345678" />
                <span class="hint">Driver's license number</span>
            </div>
            <div class="item">
                <p>Home Phone</p>
                <el-input v-model="item.home_phone" placeholder="e.g. +61 2 1234 5678" />
                <span class="hint">Home phone number</span>
            </div>
            <div class="item">
                <p>Mobile <span class="required">*</span></p>
                <el-input v-model="item.mobile" placeholder="e.g. +61 4XX XXX XXX" />
                <span class="hint">Mobile phone number</span>
            </div>
            <div class="item">
                <p>Email <span class="required">*</span></p>
                <el-input v-model="item.email" type="email" placeholder="example@domain.com" />
                <span class="hint">Valid email address</span>
            </div>
            <div class="long_item">
                <h1>Address</h1>
            </div>
            <div class="item">
                <p>Unit/Suite</p>
                <el-input v-model="item.address_unit" placeholder="e.g. Unit 5" />
                <span class="hint">Unit or suite number if applicable</span>
            </div>
            <div class="item">
                <p>Street No <span class="required">*</span></p>
                <el-input v-model="item.address_street_no" placeholder="e.g. 123" />
                <span class="hint">Street number</span>
            </div>
            <div class="item">
                <p>Street Name <span class="required">*</span></p>
                <el-input v-model="item.address_street_name" placeholder="e.g. Main Street" />
                <span class="hint">Street name</span>
            </div>
            <div class="item">
                <p>Suburb <span class="required">*</span></p>
                <el-input v-model="item.address_suburb" placeholder="e.g. Richmond" />
                <span class="hint">Suburb name</span>
            </div>
            <div class="item">
                <p>State <span class="required">*</span></p>
                <el-select v-model="item.address_state" placeholder="Select state">
                    <el-option value="NSW" label="NSW" />
                    <el-option value="VIC" label="VIC" />
                    <el-option value="QLD" label="QLD" />
                    <el-option value="SA" label="SA" />
                    <el-option value="WA" label="WA" />
                    <el-option value="TAS" label="TAS" />
                    <el-option value="NT" label="NT" />
                    <el-option value="ACT" label="ACT" />
                </el-select>
                <span class="hint">Australian state or territory</span>
            </div>
            <div class="item">
                <p>Postcode <span class="required">*</span></p>
                <el-input v-model="item.address_postcode" placeholder="e.g. 3000" maxlength="4" />
                <span class="hint">4-digit postcode</span>
            </div>
            <div class="long_item">
                <h1>Employment Details</h1>
            </div>
            <div class="item">
                <p>Occupation</p>
                <el-input v-model="item.occupation" placeholder="e.g. Software Engineer" />
                <span class="hint">Current job title or occupation</span>
            </div>
            <div class="item">
                <p>Employer Name</p>
                <el-input v-model="item.employer_name" placeholder="e.g. ABC Company" />
                <span class="hint">Name of current employer</span>
            </div>
            <div class="item">
                <p>Employment Type</p>
                <el-select v-model="item.employment_type" placeholder="Select type">
                    <el-option value="full_time" label="Full Time" />
                    <el-option value="part_time" label="Part Time" />
                    <el-option value="casual" label="Casual/Temp" />
                    <el-option value="contract" label="Contract" />
                </el-select>
                <span class="hint">Type of employment</span>
            </div>
            <div class="item">
                <p>Annual Income ($)</p>
                <el-input v-model="item.annual_income" type="number" placeholder="e.g. 120000" />
                <span class="hint">Annual income in dollars</span>
            </div>
            <div class="long_item" v-if="item.guarantor_type === 'company'">
                <h1>Company Details</h1>
            </div>
            <div class="item" v-if="item.guarantor_type === 'company'">
                <p>Company Name <span class="required">*</span></p>
                <el-input v-model="item.company_name" placeholder="Enter company name" />
                <span class="hint">Legal registered name of the company</span>
            </div>
            <div class="item" v-if="item.guarantor_type === 'company'">
                <p>ABN <span class="required">*</span></p>
                <el-input v-model="item.company_abn" placeholder="e.g. 12 345 678 901" maxlength="14" />
                <span class="hint">Australian Business Number (11 digits)</span>
            </div>
            <div class="item" v-if="item.guarantor_type === 'company'">
                <p>ACN</p>
                <el-input v-model="item.company_acn" placeholder="e.g. 123 456 789" maxlength="9" />
                <span class="hint">Australian Company Number (9 digits)</span>
            </div>
            <div class="long_item">
                <h1>Relationship</h1>
            </div>
            <div class="item">
                <p>Borrower <span class="required">*</span></p>
                <el-select 
                    v-model="item.borrower" 
                    placeholder="Select Borrower" 
                    :loading="loadingBorrowers"
                    filterable
                    clearable
                    required>
                    <el-option 
                        v-for="option in borrowerOptions" 
                        :key="option.value" 
                        :value="option.value" 
                        :label="option.label" />
                </el-select>
                <span class="hint">Select the borrower this guarantor is related to</span>
            </div>
            <div class="item">
                <p>Application <span class="required">*</span></p>
                <el-select 
                    v-model="item.application" 
                    placeholder="Select Application" 
                    :loading="loadingApplications"
                    filterable
                    clearable
                    required>
                    <el-option 
                        v-for="option in applicationOptions" 
                        :key="option.value" 
                        :value="option.value" 
                        :label="option.label" />
                </el-select>
                <span class="hint">Select the application this guarantor belongs to</span>
            </div>
            <div class="buttons">
                <el-button type="danger" @click="$emit('remove', index)" :disabled="guarantors.length <= 1">Remove</el-button>
            </div>
        </div>
        <div class="add">
            <el-button type="primary" @click="$emit('add')">Add Guarantor</el-button>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { borrowerApi } from '@/api/borrowers';
    import { applicationApi } from '@/api/application';
    import { ElLoading, ElMessage } from 'element-plus';

    const props = defineProps({
        guarantors: Array
    });

    defineEmits(['add', 'remove']);

    // Define borrower options with reactive reference
    const borrowerOptions = ref([]);
    const applicationOptions = ref([]);
    
    // Loading states
    const loadingBorrowers = ref(false);
    const loadingApplications = ref(false);

    // Fetch borrowers from API
    const fetchBorrowers = async () => {
        loadingBorrowers.value = true;
        try {
            const [error, data] = await borrowerApi.borrowers();
            if (error) {
                ElMessage.error('Failed to load borrowers: ' + (error.detail || 'Unknown error'));
                return;
            }
            
            // Extract results from paginated response and handle different data formats
            const borrowersArray = data && data.results ? data.results : 
                                  (Array.isArray(data) ? data : []);
            
            // Map API response to dropdown options with safe access to properties
            borrowerOptions.value = borrowersArray.map(borrower => ({
                value: borrower.id || '', // Store only the ID as value with fallback
                label: borrower.first_name && borrower.last_name ? 
                       `${borrower.first_name} ${borrower.last_name}` : 
                       (borrower.name || 'Unknown Borrower') // Display name as label with fallback
            }));
        } catch (err) {
            console.error('Error fetching borrowers:', err);
            ElMessage.error('Failed to load borrowers');
        } finally {
            loadingBorrowers.value = false;
        }
    };

    // Fetch applications from API
    const fetchApplications = async () => {
        loadingApplications.value = true;
        try {
            const [error, data] = await applicationApi.applications();
            if (error) {
                ElMessage.error('Failed to load applications: ' + (error.detail || 'Unknown error'));
                return;
            }
            
            // Extract results from paginated response and handle different data formats
            const applicationsArray = data && data.results ? data.results : 
                                     (Array.isArray(data) ? data : []);
            
            // Map API response to dropdown options with safe access to properties
            applicationOptions.value = applicationsArray.map(application => ({
                value: application.id || '', // Store only the ID as value with fallback
                label: application.reference_number || 'Unknown Reference' // Display reference number as label with fallback
            }));
        } catch (err) {
            console.error('Error fetching applications:', err);
            ElMessage.error('Failed to load applications');
        } finally {
            loadingApplications.value = false;
        }
    };

    onMounted(async () => {
        // Load data from APIs
        await Promise.all([fetchBorrowers(), fetchApplications()]);
        
        // Set default guarantor type if not set
        props.guarantors.forEach(guarantor => {
            if (!guarantor.guarantor_type) {
                guarantor.guarantor_type = "individual";
            }
            
            // Set default borrower if not set and options are available
            if (!guarantor.borrower && borrowerOptions.value.length > 0) {
                guarantor.borrower = borrowerOptions.value[0].value;
            }
            
            // Set default application if not set and options are available
            if (!guarantor.application && applicationOptions.value.length > 0) {
                guarantor.application = applicationOptions.value[0].value;
            }
        });
    });
</script>

<style scoped>
    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .guarantor {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        padding: 15px;
        border: 1px solid #e1e1e1;
        border-radius: 5px;
    }
    .item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .long_item {
        grid-column: 1 / 4;
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
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }
    .buttons {
        grid-column: 1 / 4;
        display: flex;
        justify-content: flex-end;
        margin-top: 10px;
    }
    .add {
        display: flex;
        justify-content: center;
        margin-top: 10px;
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
