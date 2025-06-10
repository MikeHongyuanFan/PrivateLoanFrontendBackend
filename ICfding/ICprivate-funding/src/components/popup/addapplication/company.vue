<template>
    <div class="form">
        <div class="long_item">
            <h1>Company Details</h1>
        </div>
        <div v-for="(item, index) in company" :key="index" class="company">
            <div class="item">
                <p>Company Name <span class="required">*</span></p >
                <el-input v-model="item.company_name" placeholder="Enter company name" />
                <span class="hint">Legal registered name of the company</span>
            </div>
            <div class="item">
                <p>ABN <span class="required">*</span></p >
                <el-input v-model="item.company_abn" placeholder="e.g. 12 345 678 901" maxlength="14" />
                <span class="hint">Australian Business Number (11 digits)</span>
            </div>
            <div class="item">
                <p>ACN</p >
                <el-input v-model="item.company_acn" placeholder="e.g. 123 456 789" maxlength="9" />
                <span class="hint">Australian Company Number (9 digits)</span>
            </div>
            <div class="item">
                <p>Industry Type <span class="required">*</span></p >
                <el-select v-model="item.industry_type" placeholder="Select industry">
                    <el-option value="agriculture" label="Agriculture" />
                    <el-option value="mining" label="Mining" />
                    <el-option value="manufacturing" label="Manufacturing" />
                    <el-option value="construction" label="Construction" />
                    <el-option value="retail" label="Retail" />
                    <el-option value="transport" label="Transport" />
                    <el-option value="hospitality" label="Hospitality" />
                    <el-option value="finance" label="Finance" />
                    <el-option value="real_estate" label="Real Estate" />
                    <el-option value="professional" label="Professional Services" />
                    <el-option value="education" label="Education" />
                    <el-option value="healthcare" label="Healthcare" />
                    <el-option value="arts" label="Arts and Recreation" />
                    <el-option value="other" label="Other" />
                </el-select>
                <span class="hint">Primary industry of the company</span>
            </div>
            <div class="item">
                <p>Contact Number <span class="required">*</span></p >
                <el-input v-model="item.contact_number" placeholder="e.g. +61 2 1234 5678" />
                <span class="hint">Primary contact number for the company</span>
            </div>
            <div class="item">
                <p>Annual Company Income ($) <span class="required">*</span></p >
                <el-input v-model="item.annual_company_income" type="number" placeholder="e.g. 1000000" />
                <span class="hint">Annual income in dollars (max 10 digits)</span>
            </div>
            <div class="item">
                <p>Trust Structure</p >
                <div class="trust">
                    <el-checkbox v-model="item.is_trustee">Is Trustee</el-checkbox>
                    <el-checkbox v-model="item.is_smsf_trustee">Is SMSF Trustee</el-checkbox>
                </div>
                <span class="hint">Check if company acts as a trustee</span>
            </div>
            <div class="item">
                <p>Trustee Name</p >
                <el-input v-model="item.trustee_name" placeholder="Enter trustee name" :disabled="!item.is_trustee && !item.is_smsf_trustee" />
                <span class="hint">Required if company is a trustee</span>
            </div>
            <div class="long_item">
                <h1>Registered Address</h1>
            </div>
            <div class="item">
                <p>Unit/Suite</p >
                <el-input v-model="item.registered_address_unit" placeholder="e.g. Unit 5" />
                <span class="hint">Unit or suite number if applicable</span>
            </div>
            <div class="item">
                <p>Street No <span class="required">*</span></p >
                <el-input v-model="item.registered_address_street_no" placeholder="e.g. 123" />
                <span class="hint">Street number</span>
            </div>
            <div class="item">
                <p>Street Name <span class="required">*</span></p >
                <el-input v-model="item.registered_address_street_name" placeholder="e.g. Main Street" />
                <span class="hint">Street name</span>
            </div>
            <div class="item">
                <p>Suburb <span class="required">*</span></p >
                <el-input v-model="item.registered_address_suburb" placeholder="e.g. Richmond" />
                <span class="hint">Suburb name</span>
            </div>
            <div class="item">
                <p>State <span class="required">*</span></p >
                <el-select v-model="item.registered_address_state" placeholder="Select state">
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
                <p>Postcode <span class="required">*</span></p >
                <el-input v-model="item.registered_address_postcode" placeholder="e.g. 3000" maxlength="4" />
                <span class="hint">4-digit postcode</span>
            </div>
            <div class="long_item">
                <h1>Directors</h1>
            </div>
            <div v-for="(director, idx) in item.directors" :key="idx" class="director">
                <div class="item">
                    <p>Director Name <span class="required">*</span></p >
                    <el-input v-model="director.name" placeholder="Enter director's full name" />
                    <span class="hint">Full legal name of the director</span>
                </div>
                <div class="item">
                    <p>Roles <span class="required">*</span></p >
                    <el-select v-model="director.selectedRoles" multiple placeholder="Select roles" @change="updateRoles(director)">
                        <el-option value="director" label="Director" />
                        <el-option value="secretary" label="Secretary" />
                        <el-option value="public_officer" label="Public Officer" />
                        <el-option value="shareholder" label="Shareholder" />
                    </el-select>
                    <span class="hint">Select one or more roles</span>
                </div>
                <div class="item">
                    <p>Director ID</p >
                    <el-input v-model="director.director_id" placeholder="e.g. D12345678" />
                    <span class="hint">Official director identification number</span>
                </div>
                <div class="buttons">
                    <el-button type="danger" @click="$emit('remove', idx)" :disabled="item.directors.length <= 1">Remove</el-button>
                </div>
            </div>
            <div class="add">
                <el-button type="primary" @click="$emit('add')">Add Director</el-button>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { onMounted, watch } from 'vue';

    const props = defineProps({
        company: Array
    });

    defineEmits(['add', 'remove']);

    // Function to update the roles string from the selected roles array
    const updateRoles = (director) => {
        director.roles = director.selectedRoles.join(',');
    };

    // Initialize the selectedRoles array for each director based on the roles string
    onMounted(() => {
        props.company.forEach(company => {
            if (company.directors) {
                company.directors.forEach(director => {
                    // Initialize selectedRoles array if it doesn't exist
                    if (!director.selectedRoles) {
                        director.selectedRoles = director.roles ? director.roles.split(',').map(role => role.trim()) : ['director'];
                        
                        // If roles is not set, initialize it with the default value
                        if (!director.roles) {
                            director.roles = 'director';
                        }
                    }
                });
            }
        });
    });

    // Watch for changes in the company array (e.g., when adding new directors)
    watch(() => props.company, (newCompany) => {
        newCompany.forEach(company => {
            if (company.directors) {
                company.directors.forEach(director => {
                    // Initialize selectedRoles array for new directors
                    if (!director.selectedRoles) {
                        director.selectedRoles = director.roles ? director.roles.split(',').map(role => role.trim()) : ['director'];
                        
                        // If roles is not set, initialize it with the default value
                        if (!director.roles) {
                            director.roles = 'director';
                        }
                    }
                });
            }
        });
    }, { deep: true });
</script>

<style scoped>
    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .company {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
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
    .director {
        grid-column: 1 / 4;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        padding: 15px;
        border: 1px solid #e1e1e1;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .trust {
        display: flex;
        gap: 20px;
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
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
    }
    .add {
        grid-column: 1 / 4;
        display: flex;
        justify-content: center;
        margin-top: 10px;
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