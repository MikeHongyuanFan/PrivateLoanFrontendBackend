<template>
  <div class="popup">
    <div class="popup_title">
      <h1>{{ action }}</h1>
      <div class="close">
        <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="$emit('minimize')">
          <Minus />
        </el-icon>
        <el-icon :size="20" style="cursor: pointer; color: #7A858E;" @click="$emit('close')">
          <Close />
        </el-icon>
      </div>
    </div>
    <div class="popup_content">
      <el-collapse v-model="activeNames" accordion style="--el-collapse-border-color: none;">
        <el-collapse-item name="1">
          <template #title>
            <div class="title">
              <el-icon style="font-size: 20px" :color="isBasicInfoValid ? '#2984DE' : '#E1E1E1'">
                <SuccessFilled />
              </el-icon>
              <p :style="{ color: isBasicInfoValid ? '#2984DE' : '#272727' }">Basic Information</p>
            </div>
          </template>
          <div class="form">
            <div class="item">
              <p>First Name</p>
              <el-input v-model="form.first_name" placeholder="Enter first name" />
            </div>
            <div class="item">
              <p>Last Name</p>
              <el-input v-model="form.last_name" placeholder="Enter last name" />
            </div>
            <div class="item">
              <p>Date of Birth</p>
              <el-date-picker
                v-model="form.date_of_birth"
                type="date"
                placeholder="Select date"
                format="YYYY-MM-DD"
                style="width: 100%"
              />
            </div>
            <div class="item">
              <p>Email</p>
              <el-input v-model="form.email" placeholder="Enter email address" />
            </div>
            <div class="item">
              <p>Phone Number</p>
              <el-input v-model="form.phone" placeholder="Enter phone number" />
            </div>
            <div class="item">
              <p>Street Address</p>
              <el-input v-model="form.address" placeholder="Enter street address" />
            </div>
            <div class="item">
              <p>City</p>
              <el-input v-model="form.city" placeholder="Enter city" />
            </div>
            <div class="item">
              <p>State</p>
              <el-input v-model="form.state" placeholder="Enter state" />
            </div>
            <div class="item">
              <p>Postal Code</p>
              <el-input v-model="form.postal_code" placeholder="Enter postal code" />
            </div>
          </div>
        </el-collapse-item>
        
        <el-collapse-item name="2">
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
              <el-select v-model="form.employment_type" placeholder="Select employment type" style="width: 100%">
                <el-option label="Full-time" value="full_time" />
                <el-option label="Part-time" value="part_time" />
                <el-option label="Casual" value="casual" />
                <el-option label="Contract" value="contract" />
              </el-select>
            </div>
            <div class="item">
              <p>Annual Income</p>
              <el-input-number 
                v-model="form.annual_income"
                :min="0"
                :precision="2"
                :step="1000"
                :controls="false"
                placeholder="Enter annual income"
                style="width: 100%"
              />
            </div>
            <div class="item">
              <p>Employer Name</p>
              <el-input v-model="form.employer_name" placeholder="Enter employer name" />
            </div>
            <div class="item">
              <p>Years with Employer</p>
              <el-input-number 
                v-model="form.years_with_employer"
                :min="0"
                :precision="1"
                :step="0.5"
                :controls="false"
                placeholder="Enter years with employer"
                style="width: 100%"
              />
            </div>
          </div>
        </el-collapse-item>
        
        <el-collapse-item name="3">
          <template #title>
            <div class="title">
              <el-icon style="font-size: 20px" :color="isRelationshipValid ? '#2984DE' : '#E1E1E1'">
                <SuccessFilled />
              </el-icon>
              <p :style="{ color: isRelationshipValid ? '#2984DE' : '#272727' }">Relationship Information</p>
            </div>
          </template>
          <div class="form">
            <div class="item">
              <p>Relationship to Borrower</p>
              <el-select v-model="form.relationship" placeholder="Select relationship" style="width: 100%">
                <el-option label="Spouse" value="spouse" />
                <el-option label="Parent" value="parent" />
                <el-option label="Child" value="child" />
                <el-option label="Sibling" value="sibling" />
                <el-option label="Business Partner" value="business_partner" />
                <el-option label="Other" value="other" />
              </el-select>
            </div>
            <div class="item" v-if="form.relationship === 'other'">
              <p>Specify Relationship</p>
              <el-input v-model="form.relationship_other" placeholder="Please specify relationship" />
            </div>
            <div class="item">
              <p>Related Borrower</p>
              <el-select 
                v-model="form.borrower_id" 
                placeholder="Select related borrower"
                filterable
                clearable
                :loading="loadingBorrowers"
                style="width: 100%"
              >
                <el-option 
                  v-for="borrower in borrowerOptions" 
                  :key="borrower.id" 
                  :label="borrower.name" 
                  :value="borrower.id" 
                />
              </el-select>
            </div>
            <div class="item">
              <p>Related Application</p>
              <el-select 
                v-model="form.application_id" 
                placeholder="Select related application"
                filterable
                clearable
                :loading="loadingApplications"
                style="width: 100%"
              >
                <el-option 
                  v-for="application in applicationOptions" 
                  :key="application.id" 
                  :label="application.name" 
                  :value="application.id" 
                />
              </el-select>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
    <div class="buttons">
      <Cancel @click="$emit('close')" />
      <Save @click="handleSubmit" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { SuccessFilled, Minus, Close } from '@element-plus/icons-vue';
import { api } from '@/api';
import { mapGuarantorFormToApi, mapGuarantorApiToForm } from '@/utils/dataMappers';
import Cancel from '../buttons/cancel.vue';
import Save from '../buttons/save.vue';

const props = defineProps({
  action: {
    type: String,
    required: true
  },
  guarantorData: {
    type: Object,
    default: () => ({})
  },
  borrowerId: {
    type: [String, Number],
    default: null
  },
  applicationId: {
    type: [String, Number],
    default: null
  }
});

const emit = defineEmits(['close', 'minimize', 'refresh']);

const activeNames = ref("1");
const loading = ref(false);
const loadingBorrowers = ref(false);
const loadingApplications = ref(false);
const borrowerOptions = ref([]);
const applicationOptions = ref([]);

const isEdit = computed(() => props.action.startsWith('Edit'));

const form = ref({
  first_name: '',
  last_name: '',
  date_of_birth: '',
  email: '',
  phone: '',
  address: '',
  city: '',
  state: '',
  postal_code: '',
  employment_type: '',
  annual_income: null,
  employer_name: '',
  years_with_employer: null,
  relationship: '',
  relationship_other: '',
  guarantor_type: 'individual',
  borrower_id: null,
  application_id: null,
  ...props.guarantorData
});

// Validation computed properties
const isBasicInfoValid = computed(() => {
  return form.value.first_name && form.value.last_name && form.value.date_of_birth && 
         form.value.email && form.value.phone && form.value.address && 
         form.value.city && form.value.state && form.value.postal_code;
});

const isEmploymentValid = computed(() => {
  return form.value.employment_type && form.value.annual_income;
});

const isRelationshipValid = computed(() => {
  return form.value.relationship && 
         (form.value.relationship !== 'other' || form.value.relationship_other);
});

// Watch for prop changes and update form accordingly
watch(() => props.borrowerId, (newVal) => {
  console.log('borrowerId prop changed:', newVal);
  if (newVal) {
    form.value.borrower_id = parseInt(newVal);
    console.log('Set form.borrower_id to:', form.value.borrower_id);
  }
}, { immediate: true });

watch(() => props.applicationId, (newVal) => {
  console.log('applicationId prop changed:', newVal);
  if (newVal) {
    form.value.application_id = parseInt(newVal);
    console.log('Set form.application_id to:', form.value.application_id);
  }
}, { immediate: true });

// Load all borrowers
const loadAllBorrowers = async () => {
  loadingBorrowers.value = true;
  try {
    const [error, response] = await api.borrowers();
    if (error) {
      console.error('Error loading borrowers:', error);
      return;
    }
    
    borrowerOptions.value = response.results.map(borrower => ({
      id: borrower.id,
      name: `${borrower.first_name || ''} ${borrower.last_name || ''}`.trim() || 'Unnamed Borrower'
    }));
  } catch (error) {
    console.error('Error loading borrowers:', error);
  } finally {
    loadingBorrowers.value = false;
  }
};

// Load all applications
const loadAllApplications = async () => {
  loadingApplications.value = true;
  try {
    const [error, response] = await api.applications();
    if (error) {
      console.error('Error loading applications:', error);
      return;
    }
    
    applicationOptions.value = response.results.map(application => ({
      id: application.id,
      name: `Application #${application.id} - ${application.borrower_name || 'Untitled'}`
    }));
  } catch (error) {
    console.error('Error loading applications:', error);
  } finally {
    loadingApplications.value = false;
  }
};

// Load related data if editing
const loadRelatedData = async () => {
  if (isEdit.value && props.guarantorData.id) {
    try {
      // Get the guarantor data and map it to form format
      const [error, response] = await api.getGuarantor(props.guarantorData.id);
      if (!error && response) {
        console.log('Guarantor data received:', response);
        const formData = mapGuarantorApiToForm(response);
        form.value = { ...form.value, ...formData };
        
        // Ensure relationship fields are properly set from the API response
        if (response.borrower) {
          form.value.borrower_id = parseInt(response.borrower);
        }
        if (response.application) {
          form.value.application_id = parseInt(response.application);
        }
      } else {
        console.error('Error loading guarantor data:', error);
        ElMessage.error('Failed to load guarantor data');
      }
      
      // Load related borrowers (for display purposes)
      const [borrowerError, borrowerResponse] = await api.getGuarantorBorrowers(props.guarantorData.id);
      if (!borrowerError && borrowerResponse && borrowerResponse.results && borrowerResponse.results.length > 0) {
        const borrower = borrowerResponse.results[0];
        // Only set if not already set from the main response
        if (!form.value.borrower_id) {
          form.value.borrower_id = borrower.id;
        }
      }
      
      // Load related applications (for display purposes)
      const [appError, appResponse] = await api.getGuarantorApplications(props.guarantorData.id);
      if (!appError && appResponse && appResponse.results && appResponse.results.length > 0) {
        const application = appResponse.results[0];
        // Only set if not already set from the main response
        if (!form.value.application_id) {
          form.value.application_id = application.id;
        }
      }
    } catch (error) {
      console.error('Error loading related data:', error);
      ElMessage.error('Failed to load guarantor data');
    }
  }
};

onMounted(() => {
  // Load all borrowers and applications
  loadAllBorrowers();
  loadAllApplications();
  
  // Load related data if editing
  if (isEdit.value) {
    loadRelatedData();
  }
});

const handleSubmit = async () => {
  try {
    loading.value = true;

    // Use the data mapper to map form data to API format
    const formData = mapGuarantorFormToApi(form.value);
    
    // For debugging - log the relationship fields
    console.log('Form relationship fields:', {
      borrower_id: form.value.borrower_id,
      application_id: form.value.application_id
    });
    console.log('API relationship fields:', {
      borrower: formData.borrower,
      application: formData.application
    });
    console.log('Submitting guarantor data:', formData);

    // Make API call to create/update guarantor
    let guarantorId;
    if (isEdit.value) {
      const [error, response] = await api.updateGuarantor(props.guarantorData.id, formData);
      if (error) {
        console.error('API Error:', error);
        throw error;
      }
      guarantorId = props.guarantorData.id;
      
      ElMessage.success({
        message: 'Guarantor successfully updated!',
        type: 'success'
      });
    } else {
      const [error, response] = await api.createGuarantor(formData);
      if (error) {
        console.error('API Error:', error);
        throw error;
      }
      guarantorId = response.id;
      
      ElMessage.success({
        message: 'Guarantor successfully created!',
        type: 'success'
      });
    }

    emit('refresh');
    emit('close');
  } catch (error) {
    console.error('Form submission error:', error);
    
    // Format error message for better user experience
    let errorMessage = 'An error occurred. Please try again.';
    
    if (error && typeof error === 'object') {
      // Handle API validation errors
      const errorFields = Object.keys(error);
      if (errorFields.length > 0) {
        const fieldErrors = [];
        
        errorFields.forEach(field => {
          if (Array.isArray(error[field])) {
            fieldErrors.push(`${field.replace(/_/g, ' ')}: ${error[field].join(', ')}`);
          } else {
            fieldErrors.push(`${field.replace(/_/g, ' ')}: ${error[field]}`);
          }
        });
        
        errorMessage = `Please fix the following errors:\n${fieldErrors.join('\n')}`;
      } else if (error.message) {
        errorMessage = error.message;
      }
    } else if (typeof error === 'string') {
      errorMessage = error;
    }
    
    ElMessage.error({
      message: errorMessage,
      type: 'error',
      duration: 5000
    });
  } finally {
    loading.value = false;
  }
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
  width: 40%;
  height: 100vh;
  overflow: hidden;
  z-index: 1999;
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