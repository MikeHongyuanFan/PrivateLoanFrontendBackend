<template>
    <div class="popup">
        <div class="popup_title">
            <h1>{{ action }}</h1>
            <div class="close">
                <!-- <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleMinimize"><Minus /></el-icon> -->
                <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="handleClose">
                    <Close />
                </el-icon>
            </div>
        </div>
        <div class="popup_content">
            <el-collapse v-model="activeNames" accordion style="--el-collapse-border-color: none;">
                <el-collapse-item name="1">
                    <template #title>
                        <div class="title">
                            <el-icon style="font-size: 20px" :color="isPersonalInfoValid ? '#2984DE' : '#E1E1E1'">
                                <SuccessFilled />
                            </el-icon>
                            <p :style="{ color: isPersonalInfoValid ? '#2984DE' : '#272727' }">Personal Information</p>
                        </div>
                    </template>
                    <div class="form">
                        <div class="item">
                            <p>First Name</p>
                            <el-input v-model="overview.first_name" placeholder="Enter first name" />
                        </div>
                        <div class="item">
                            <p>Last Name</p>
                            <el-input v-model="overview.last_name" placeholder="Enter last name" />
                        </div>
                        <div class="item">
                            <p>Email</p>
                            <el-input v-model="overview.email" type="email" placeholder="example@domain.com" />
                        </div>
                        <div class="item">
                            <p>Phone</p>
                            <el-input v-model="overview.phone" placeholder="e.g. +61 4XX XXX XXX" />
                        </div>
                        <div class="item">
                            <p>Date of Birth</p>
                            <el-date-picker 
                                v-model="overview.date_of_birth" 
                                type="date" 
                                placeholder="YYYY-MM-DD" 
                                format="YYYY-MM-DD"
                                value-format="YYYY-MM-DD"
                                style="width: 100%" />
                        </div>
                        <div class="item">
                            <p>Tax ID (TFN)</p>
                            <el-input v-model="overview.tax_id" placeholder="e.g. 123 456 789" maxlength="11" />
                        </div>
                        <div class="item">
                            <p>Marital Status</p>
                            <el-select v-model="overview.marital_status" placeholder="Select status" style="width: 100%">
                                <el-option value="single" label="Single" />
                                <el-option value="married" label="Married" />
                                <el-option value="de_facto" label="De Facto" />
                                <el-option value="divorced" label="Divorced" />
                                <el-option value="widowed" label="Widowed" />
                            </el-select>
                        </div>
                        <div class="item">
                            <p>Residency Status</p>
                            <el-select v-model="overview.residency_status" placeholder="Select status" style="width: 100%">
                                <el-option value="citizen" label="Citizen" />
                                <el-option value="permanent_resident" label="Permanent Resident" />
                                <el-option value="temporary_resident" label="Temporary Resident" />
                                <el-option value="foreign_investor" label="Foreign Investor" />
                            </el-select>
                        </div>
                        <div class="item">
                            <p>Referral Source</p>
                            <el-input v-model="overview.referral_source" placeholder="How did you hear about us?" />
                        </div>
                        <div class="item">
                            <p>Tags</p>
                            <el-input v-model="overview.tags" placeholder="e.g. VIP, Repeat Customer" />
                        </div>
                    </div>
                </el-collapse-item>
                
                <el-collapse-item name="2">
                    <template #title>
                        <div class="title">
                            <el-icon style="font-size: 20px" :color="isAddressValid ? '#2984DE' : '#E1E1E1'">
                                <SuccessFilled />
                            </el-icon>
                            <p :style="{ color: isAddressValid ? '#2984DE' : '#272727' }">Address Information</p>
                        </div>
                    </template>
                    <div class="form">
                        <div class="item full-width">
                            <p>Street Address</p>
                            <el-input 
                                v-model="overview.address_street" 
                                placeholder="Enter street address (unit, street number, street name)" />
                        </div>
                        <div class="item">
                            <p>City/Suburb</p>
                            <el-input v-model="overview.address_city" placeholder="Enter city or suburb" />
                        </div>
                        <div class="item">
                            <p>State</p>
                            <el-select v-model="overview.address_state" placeholder="Select state" style="width: 100%">
                                <el-option value="NSW" label="New South Wales (NSW)" />
                                <el-option value="VIC" label="Victoria (VIC)" />
                                <el-option value="QLD" label="Queensland (QLD)" />
                                <el-option value="WA" label="Western Australia (WA)" />
                                <el-option value="SA" label="South Australia (SA)" />
                                <el-option value="TAS" label="Tasmania (TAS)" />
                                <el-option value="ACT" label="Australian Capital Territory (ACT)" />
                                <el-option value="NT" label="Northern Territory (NT)" />
                            </el-select>
                        </div>
                        <div class="item">
                            <p>Postal Code</p>
                            <el-input v-model="overview.address_postal_code" placeholder="Enter postal code" maxlength="4" />
                        </div>
                        <div class="item">
                            <p>Country</p>
                            <el-input v-model="overview.address_country" placeholder="Enter country" />
                        </div>
                        <div class="item full-width">
                            <p>Mailing Address</p>
                            <el-input 
                                v-model="overview.mailing_address" 
                                type="textarea" 
                                :rows="2"
                                placeholder="Enter mailing address (if different from residential)" />
                        </div>
                    </div>
                </el-collapse-item>
                
                <el-collapse-item name="3">
                    <template #title>
                        <div class="title">
                            <el-icon style="font-size: 20px" :color="isEmploymentValid ? '#2984DE' : '#E1E1E1'">
                                <SuccessFilled />
                            </el-icon>
                            <p :style="{ color: isEmploymentValid ? '#2984DE' : '#272727' }">Employment Information</p>
                        </div>
                    </template>
                    <div class="form">
                        <div class="item">
                            <p>Employment Type</p>
                            <el-select v-model="overview.employment_type" placeholder="Select employment type" style="width: 100%">
                                <el-option value="full_time" label="Full Time" />
                                <el-option value="part_time" label="Part Time" />
                                <el-option value="casual" label="Casual" />
                                <el-option value="self_employed" label="Self Employed" />
                                <el-option value="contractor" label="Contractor" />
                                <el-option value="unemployed" label="Unemployed" />
                                <el-option value="retired" label="Retired" />
                            </el-select>
                        </div>
                        <div class="item">
                            <p>Employer Name</p>
                            <el-input v-model="overview.employer_name" placeholder="Enter employer name" />
                        </div>
                        <div class="item">
                            <p>Job Title</p>
                            <el-input v-model="overview.job_title" placeholder="Enter job title/position" />
                        </div>
                        <div class="item">
                            <p>Annual Income</p>
                            <el-input-number 
                                v-model="overview.annual_income" 
                                :min="0" 
                                :step="1000"
                                :precision="2"
                                placeholder="Enter annual income" 
                                style="width: 100%" />
                        </div>
                        <div class="item">
                            <p>Employment Duration (months)</p>
                            <el-input-number 
                                v-model="overview.employment_duration" 
                                :min="0" 
                                :step="1"
                                placeholder="Enter duration in months" 
                                style="width: 100%" />
                        </div>
                        <div class="item full-width">
                            <p>Employer Address</p>
                            <el-input 
                                v-model="overview.employer_address" 
                                type="textarea" 
                                :rows="2"
                                placeholder="Enter employer address" />
                        </div>
                    </div>
                </el-collapse-item>
                
                <el-collapse-item name="4">
                    <template #title>
                        <div class="title">
                            <el-icon style="font-size: 20px" :color="isFinancialValid ? '#2984DE' : '#E1E1E1'">
                                <SuccessFilled />
                            </el-icon>
                            <p :style="{ color: isFinancialValid ? '#2984DE' : '#272727' }">Financial Information</p>
                        </div>
                    </template>
                    <div class="form">
                        <div class="item">
                            <p>Other Income</p>
                            <el-input-number 
                                v-model="overview.other_income" 
                                :min="0" 
                                :step="100"
                                :precision="2"
                                placeholder="Enter other income" 
                                style="width: 100%" />
                        </div>
                        <div class="item">
                            <p>Monthly Expenses</p>
                            <el-input-number 
                                v-model="overview.monthly_expenses" 
                                :min="0" 
                                :step="100"
                                :precision="2"
                                placeholder="Enter monthly expenses" 
                                style="width: 100%" />
                        </div>
                        <div class="item">
                            <p>Credit Score</p>
                            <el-input-number 
                                v-model="overview.credit_score" 
                                :min="300" 
                                :max="850"
                                :step="1"
                                placeholder="Enter credit score" 
                                style="width: 100%" />
                        </div>
                    </div>
                </el-collapse-item>
            </el-collapse>
        </div>
        <div class="buttons">
            <Cancel @click="handleClose"></Cancel>
            <Save @click="handleAddOrEdit"></Save>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import Cancel from '../buttons/cancel.vue';
import Save from '../buttons/save.vue';
import { api } from '@/api';
import useSystem from '@/hooks/useSystem'
import { ElMessage } from 'element-plus'
import { mapBorrowerApiToForm, mapBorrowerFormToApi } from '@/utils/dataMappers';
import { SuccessFilled, Close } from '@element-plus/icons-vue';

const { userInfo } = useSystem()

const props = defineProps({
    action: String,
    editId: [String, Number]
})

const activeNames = ref("1")
const overview = ref({
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
    employment_type: "",
    address_street: "",
    address_city: "",
    address_state: "",
    address_postal_code: "",
    address_country: "",
    mailing_address: "",
    employer_name: "",
    job_title: "",
    annual_income: null,
    employment_duration: null,
    employer_address: "",
    other_income: null,
    monthly_expenses: null,
    credit_score: null,
})

watch(() => props.editId, (newVal) => {
    if (newVal) {
        console.log("watch", newVal);
        getBorrower()
    }
}, { deep: true, immediate: true })

const emit = defineEmits(['close', 'minimize'])

const handleClose = () => {
    emit('close')
}
const handleMinimize = () => {
    emit('minimize')
}

// Validation computed properties
const isPersonalInfoValid = computed(() => {
    return overview.value.first_name && overview.value.last_name && overview.value.email && overview.value.phone;
})

const isAddressValid = computed(() => {
    return overview.value.address_street && overview.value.address_city && overview.value.address_state && overview.value.address_postal_code;
})

const isEmploymentValid = computed(() => {
    return overview.value.employment_type && overview.value.employer_name && overview.value.annual_income;
})

const isFinancialValid = computed(() => {
    return true; // Financial information is optional
})

async function getBorrower() {
    try {
        const [err, res] = await api.borrower(props.editId)
        if (!err && res) {
            console.log('Borrower data received:', res);
            // Use the data mapper to map API response to form fields
            const formData = mapBorrowerApiToForm(res);
            overview.value = { ...overview.value, ...formData };
        } else {
            console.error('Error loading borrower:', err);
            ElMessage.error('Failed to load borrower data');
        }
    } catch (error) {
        console.error('Exception in getBorrower:', error);
        ElMessage.error('Failed to load borrower data');
    }
}

const addBorrower = async () => {
    try {
        // Use the data mapper to map form data to API format
        const data = mapBorrowerFormToApi(overview.value);
        console.log('Sending borrower data to API:', data);
        
        const [err, res] = await api.addBorrowers(data)
        if (!err && res) {
            console.log('Borrower created successfully:', res);
            ElMessage.success('Borrower added successfully');
            emit('close')
        } else {
            console.error('Error creating borrower:', err);
            ElMessage.error(err?.detail || err?.message || 'Failed to create borrower');
        }
    } catch (error) {
        console.error('Exception in addBorrower:', error);
        ElMessage.error('Failed to create borrower');
    }
}

const editBorrower = async () => {
    try {
        // Use the data mapper to map form data to API format
        const data = mapBorrowerFormToApi(overview.value);
        console.log('Sending borrower update data to API:', data);
        
        const [err, res] = await api.putBorrower(props.editId, data)
        if (!err && res) {
            console.log('Borrower updated successfully:', res);
            ElMessage.success('Borrower updated successfully');
            emit('close')
        } else {
            console.error('Error updating borrower:', err);
            ElMessage.error(err?.detail || err?.message || 'Failed to update borrower');
        }
    } catch (error) {
        console.error('Exception in editBorrower:', error);
        ElMessage.error('Failed to update borrower');
    }
}

const handleAddOrEdit = async () => {
    if (props.editId) {
        editBorrower()
    } else {
        addBorrower()
    }
}
</script>

<style lang="scss" scoped>
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
    width: 40%;
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

.item.full-width {
    grid-column: 1 / 3;
}

.item p {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.75rem;
    font-style: normal;
    font-weight: 500;
    line-height: 12px;
    margin: 0;
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