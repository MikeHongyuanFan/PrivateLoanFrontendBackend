<template>
    <div class="form">
        <div v-for="(item, index) in borrowers" :key="index" class="borrower">
            <!-- Personal Information Section -->
            <div class="section-header">
                <h3>Personal Information</h3>
            </div>
            <div class="item">
                <p>Title <span class="optional">(optional)</span></p>
                <el-select v-model="item.title" placeholder="Select title" style="width: 100%">
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
                <p>First Name <span class="optional">(optional)</span></p>
                <el-input v-model="item.first_name" placeholder="Enter first name" />
                <span class="hint">Legal first name</span>
            </div>
            <div class="item">
                <p>Last Name <span class="optional">(optional)</span></p>
                <el-input v-model="item.last_name" placeholder="Enter last name" />
                <span class="hint">Legal last name</span>
            </div>
            <div class="item">
                <p>Date of Birth <span class="optional">(optional)</span></p>
                <el-date-picker 
                    v-model="item.date_of_birth" 
                    type="date" 
                    placeholder="YYYY-MM-DD" 
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD" />
                <span class="hint">Date must be in YYYY-MM-DD format</span>
            </div>
            <div class="item">
                <p>Driver's License Number <span class="optional">(optional)</span></p>
                <el-input v-model="item.drivers_licence_no" placeholder="Enter driver's license number" />
                <span class="hint">Driver's license number</span>
            </div>
            <div class="item">
                <p>Home Phone <span class="optional">(optional)</span></p>
                <el-input v-model="item.home_phone" placeholder="e.g. +61 2 XXXX XXXX" />
                <span class="hint">Home phone number</span>
            </div>
            <div class="item">
                <p>Mobile Phone <span class="optional">(optional)</span></p>
                <el-input v-model="item.mobile" placeholder="e.g. +61 4XX XXX XXX" />
                <span class="hint">Mobile phone number</span>
            </div>
            <div class="item">
                <p>Email <span class="optional">(optional)</span></p>
                <el-input v-model="item.email" type="email" placeholder="example@domain.com" />
                <span class="hint">Valid email address</span>
            </div>

            <!-- Residential Address Section -->
            <div class="section-header">
                <h3>Residential Address</h3>
            </div>
            <div class="item">
                <p>Unit Number <span class="optional">(optional)</span></p>
                <el-input v-model="item.address_unit" placeholder="e.g. Unit 1" />
                <span class="hint">Unit, apartment, or suite number</span>
            </div>
            <div class="item">
                <p>Street Number <span class="optional">(optional)</span></p>
                <el-input v-model="item.address_street_no" placeholder="e.g. 123" />
                <span class="hint">Street number</span>
            </div>
            <div class="item">
                <p>Street Name <span class="optional">(optional)</span></p>
                <el-input v-model="item.address_street_name" placeholder="e.g. Main Street" />
                <span class="hint">Street name</span>
            </div>
            <div class="item">
                <p>Suburb <span class="optional">(optional)</span></p>
                <el-input v-model="item.address_suburb" placeholder="e.g. Sydney" />
                <span class="hint">Suburb or city</span>
            </div>
            <div class="item">
                <p>State <span class="optional">(optional)</span></p>
                <el-select v-model="item.address_state" placeholder="Select state" style="width: 100%">
                    <el-option value="NSW" label="New South Wales" />
                    <el-option value="VIC" label="Victoria" />
                    <el-option value="QLD" label="Queensland" />
                    <el-option value="WA" label="Western Australia" />
                    <el-option value="SA" label="South Australia" />
                    <el-option value="TAS" label="Tasmania" />
                    <el-option value="ACT" label="Australian Capital Territory" />
                    <el-option value="NT" label="Northern Territory" />
                </el-select>
                <span class="hint">State or territory</span>
            </div>
            <div class="item">
                <p>Postcode <span class="optional">(optional)</span></p>
                <el-input v-model="item.address_postcode" placeholder="e.g. 2000" maxlength="4" />
                <span class="hint">4-digit postcode</span>
            </div>

            <!-- Employment Details Section -->
            <div class="section-header">
                <h3>Employment Details</h3>
            </div>
            <div class="item">
                <p>Occupation <span class="optional">(optional)</span></p>
                <el-input v-model="item.occupation" placeholder="e.g. Software Engineer" />
                <span class="hint">Current job title or occupation</span>
            </div>
            <div class="item">
                <p>Employer Name <span class="optional">(optional)</span></p>
                <el-input v-model="item.employer_name" placeholder="e.g. ABC Company" />
                <span class="hint">Name of current employer</span>
            </div>
            <div class="item">
                <p>Employment Type <span class="optional">(optional)</span></p>
                <el-select v-model="item.employment_type" placeholder="Select type" style="width: 100%">
                    <el-option value="full_time" label="Full Time" />
                    <el-option value="part_time" label="Part Time" />
                    <el-option value="casual" label="Casual/Temp" />
                    <el-option value="contractor" label="Contractor" />
                </el-select>
                <span class="hint">Type of employment</span>
            </div>
            <div class="item">
                <p>Annual Income ($) <span class="optional">(optional)</span></p>
                <el-input-number 
                    v-model="item.annual_income" 
                    :min="0" 
                    :step="1000"
                    :precision="2"
                    placeholder="Enter annual income" 
                    style="width: 100%" />
                <span class="hint">Annual income in dollars</span>
            </div>

            <!-- Additional Information Section -->
            <div class="section-header">
                <h3>Additional Information</h3>
            </div>
            <div class="item">
                <p>Tax ID (TFN) <span class="optional">(optional)</span></p>
                <el-input v-model="item.tax_id" placeholder="e.g. 123 456 789" maxlength="11" />
                <span class="hint">Tax File Number</span>
            </div>
            <div class="item">
                <p>Marital Status <span class="optional">(optional)</span></p>
                <el-select v-model="item.marital_status" placeholder="Select status" style="width: 100%">
                    <el-option value="single" label="Single" />
                    <el-option value="married" label="Married" />
                    <el-option value="de_facto" label="De Facto" />
                    <el-option value="divorced" label="Divorced" />
                    <el-option value="widowed" label="Widowed" />
                </el-select>
                <span class="hint">Current marital status</span>
            </div>
            <div class="item">
                <p>Residency Status <span class="optional">(optional)</span></p>
                <el-select v-model="item.residency_status" placeholder="Select status" style="width: 100%">
                    <el-option value="citizen" label="Citizen" />
                    <el-option value="permanent_resident" label="Permanent Resident" />
                    <el-option value="temporary_resident" label="Temporary Resident" />
                    <el-option value="foreign_investor" label="Foreign Investor" />
                </el-select>
                <span class="hint">Australian residency status</span>
            </div>
            <div class="item">
                <p>Referral Source <span class="optional">(optional)</span></p>
                <el-input v-model="item.referral_source" placeholder="e.g. Broker, Website, etc." />
                <span class="hint">How did you hear about us?</span>
            </div>
            <div class="item">
                <p>Tags <span class="optional">(optional)</span></p>
                <el-input v-model="item.tags" placeholder="e.g. VIP, Priority, etc." />
                <span class="hint">Any tags or notes</span>
            </div>

            <div class="buttons">
                <el-button type="danger" @click="$emit('remove', index)" :disabled="borrowers.length <= 1">Remove</el-button>
            </div>
        </div>
        <div class="add">
            <el-button type="primary" @click="$emit('add')">Add Borrower</el-button>
        </div>
    </div>
</template>

<script setup>
    const props = defineProps({
        borrowers: Array
    });

    defineEmits(['add', 'remove']);
</script>

<style scoped>
    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .borrower {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        padding: 15px;
        border: 1px solid #e1e1e1;
        border-radius: 5px;
    }
    .section-header {
        grid-column: 1 / 4;
        padding: 10px 0;
        border-bottom: 1px solid #e8e8e8;
        margin-bottom: 10px;
    }
    .section-header h3 {
        color: #2984DE;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0;
    }
    .item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .item.full-width {
        grid-column: 1 / 4;
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
    :deep(.el-input-number) {
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
    
    .optional {
        color: #909399;
        font-weight: normal;
        font-style: italic;
        margin-left: 2px;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .borrower {
            grid-template-columns: 1fr;
        }
        .item.full-width,
        .section-header,
        .buttons {
            grid-column: 1;
        }
    }
</style>
