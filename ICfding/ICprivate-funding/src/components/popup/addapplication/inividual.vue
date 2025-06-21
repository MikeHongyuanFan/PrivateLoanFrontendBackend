<template>
    <div class="form">
        <div v-for="(item, index) in borrowers" :key="index" class="borrower">
            <!-- Personal Information Section -->
            <div class="section-header">
                <h3>Personal Information</h3>
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
                <p>Email <span class="optional">(optional)</span></p>
                <el-input v-model="item.email" type="email" placeholder="example@domain.com" />
                <span class="hint">Valid email address</span>
            </div>
            <div class="item">
                <p>Phone <span class="optional">(optional)</span></p>
                <el-input v-model="item.phone" placeholder="e.g. +61 4XX XXX XXX" />
                <span class="hint">Contact phone number</span>
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
                <p>Tax ID (TFN) <span class="optional">(optional)</span></p>
                <el-input v-model="item.tax_id" placeholder="e.g. 123 456 789" maxlength="11" />
                <span class="hint">Tax File Number</span>
            </div>
            <div class="item">
                <p>Marital Status <span class="optional">(optional)</span></p>
                <el-select v-model="item.marital_status" placeholder="Select status">
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
                <el-select v-model="item.residency_status" placeholder="Select status">
                    <el-option value="citizen" label="Citizen" />
                    <el-option value="permanent_resident" label="Permanent Resident" />
                    <el-option value="temporary_resident" label="Temporary Resident" />
                    <el-option value="foreign_investor" label="Foreign Investor" />
                </el-select>
                <span class="hint">Current Australian residency status</span>
            </div>
            <div class="item">
                <p>Referral Source <span class="optional">(optional)</span></p>
                <el-input v-model="item.referral_source" placeholder="How did you hear about us?" />
                <span class="hint">How the borrower was referred</span>
            </div>
            <div class="item">
                <p>Tags <span class="optional">(optional)</span></p>
                <el-input v-model="item.tags" placeholder="e.g. VIP, Repeat Customer" />
                <span class="hint">Comma-separated tags for categorization</span>
            </div>

            <!-- Address Information Section -->
            <div class="section-header">
                <h3>Address Information</h3>
            </div>
            <div class="item full-width">
                <p>Street Address <span class="optional">(optional)</span></p>
                <el-input 
                    v-model="item.address_street" 
                    placeholder="Enter street address (unit, street number, street name)" />
                <span class="hint">e.g., Unit 203/3 Samsung Street</span>
            </div>
            <div class="item">
                <p>City/Suburb <span class="optional">(optional)</span></p>
                <el-input v-model="item.address_city" placeholder="Enter city or suburb" />
                <span class="hint">e.g., Waterloo</span>
            </div>
            <div class="item">
                <p>State <span class="optional">(optional)</span></p>
                <el-select v-model="item.address_state" placeholder="Select state">
                    <el-option value="NSW" label="New South Wales (NSW)" />
                    <el-option value="VIC" label="Victoria (VIC)" />
                    <el-option value="QLD" label="Queensland (QLD)" />
                    <el-option value="WA" label="Western Australia (WA)" />
                    <el-option value="SA" label="South Australia (SA)" />
                    <el-option value="TAS" label="Tasmania (TAS)" />
                    <el-option value="ACT" label="Australian Capital Territory (ACT)" />
                    <el-option value="NT" label="Northern Territory (NT)" />
                </el-select>
                <span class="hint">Select your state/territory</span>
            </div>
            <div class="item">
                <p>Postal Code <span class="optional">(optional)</span></p>
                <el-input v-model="item.address_postal_code" placeholder="Enter postal code" maxlength="4" />
                <span class="hint">e.g., 2017</span>
            </div>
            <div class="item">
                <p>Country <span class="optional">(optional)</span></p>
                <el-input v-model="item.address_country" placeholder="Enter country" />
                <span class="hint">e.g., Australia</span>
            </div>
            <div class="item full-width">
                <p>Mailing Address <span class="optional">(optional)</span></p>
                <el-input 
                    v-model="item.mailing_address" 
                    type="textarea" 
                    :rows="2"
                    placeholder="Enter mailing address (if different from residential)" />
                <span class="hint">Leave empty if same as residential address</span>
            </div>

            <!-- Employment Information Section -->
            <div class="section-header">
                <h3>Employment Information</h3>
            </div>
            <div class="item">
                <p>Employment Type <span class="optional">(optional)</span></p>
                <el-select v-model="item.employment_type" placeholder="Select employment type">
                    <el-option value="full_time" label="Full Time" />
                    <el-option value="part_time" label="Part Time" />
                    <el-option value="casual" label="Casual" />
                    <el-option value="self_employed" label="Self Employed" />
                    <el-option value="contractor" label="Contractor" />
                    <el-option value="unemployed" label="Unemployed" />
                    <el-option value="retired" label="Retired" />
                </el-select>
                <span class="hint">Current employment status</span>
            </div>
            <div class="item">
                <p>Employer Name <span class="optional">(optional)</span></p>
                <el-input v-model="item.employer_name" placeholder="Enter employer name" />
                <span class="hint">Current or most recent employer</span>
            </div>
            <div class="item">
                <p>Job Title <span class="optional">(optional)</span></p>
                <el-input v-model="item.job_title" placeholder="Enter job title/position" />
                <span class="hint">Current or most recent job title</span>
            </div>
            <div class="item">
                <p>Annual Income <span class="optional">(optional)</span></p>
                <el-input-number 
                    v-model="item.annual_income" 
                    :min="0" 
                    :step="1000"
                    :precision="2"
                    placeholder="Enter annual income" 
                    style="width: 100%" />
                <span class="hint">Annual gross income in AUD</span>
            </div>
            <div class="item">
                <p>Employment Duration (months) <span class="optional">(optional)</span></p>
                <el-input-number 
                    v-model="item.employment_duration" 
                    :min="0" 
                    :step="1"
                    placeholder="Enter duration in months" 
                    style="width: 100%" />
                <span class="hint">How long employed with current employer (in months)</span>
            </div>
            <div class="item full-width">
                <p>Employer Address <span class="optional">(optional)</span></p>
                <el-input 
                    v-model="item.employer_address" 
                    type="textarea" 
                    :rows="2"
                    placeholder="Enter employer address" />
                <span class="hint">Address of current or most recent employer</span>
            </div>

            <!-- Financial Information Section -->
            <div class="section-header">
                <h3>Additional Financial Information</h3>
            </div>
            <div class="item">
                <p>Other Income <span class="optional">(optional)</span></p>
                <el-input-number 
                    v-model="item.other_income" 
                    :min="0" 
                    :step="100"
                    :precision="2"
                    placeholder="Enter other income" 
                    style="width: 100%" />
                <span class="hint">Additional income from other sources (AUD)</span>
            </div>
            <div class="item">
                <p>Monthly Expenses <span class="optional">(optional)</span></p>
                <el-input-number 
                    v-model="item.monthly_expenses" 
                    :min="0" 
                    :step="100"
                    :precision="2"
                    placeholder="Enter monthly expenses" 
                    style="width: 100%" />
                <span class="hint">Total monthly living expenses (AUD)</span>
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
