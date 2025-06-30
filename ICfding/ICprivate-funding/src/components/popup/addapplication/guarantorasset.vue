<template>
    <div class="form">
        <div v-if="!localGuarantors.length">
            <p>No guarantors found. Please add guarantors first.</p>
        </div>
        
        <div v-for="(guarantor, guarantorIndex) in localGuarantors" :key="guarantorIndex" class="guarantor-section">
            <div class="guarantor-header">
                <h2>{{ guarantor.first_name }} {{ guarantor.last_name }} - Financial Items</h2>
                <p class="subtitle">Assets and Liabilities (Unified Table)</p>
            </div>
            
            <!-- Assets Section -->
            <div class="section">
                <div class="section-header">
                    <h3>Assets</h3>
                    <el-button type="primary" size="small" @click="addAsset(guarantorIndex)">
                        <el-icon><Plus /></el-icon>
                        Add Asset
                    </el-button>
                </div>
                
                <div v-if="!guarantor.assets || guarantor.assets.length === 0" class="no-items">
                    <p>No assets for this guarantor</p>
                </div>
                
                <div v-else class="items-list">
                    <div v-for="(asset, assetIndex) in guarantor.assets" :key="assetIndex" class="item-card">
                        <div class="item-header">
                            <span class="item-type">Asset</span>
                            <el-button type="danger" size="small" @click="removeAsset(guarantorIndex, assetIndex)">
                                <el-icon><Delete /></el-icon>
                            </el-button>
                        </div>
                        
                        <div class="item-fields">
                            <div class="field">
                                <label>Asset Type *</label>
                                <el-select v-model="asset.asset_type" placeholder="Select asset type" style="width: 100%" @change="handleFieldChange">
                                    <el-option value="Property" label="Property" />
                                    <el-option value="Vehicle" label="Vehicle" />
                                    <el-option value="Savings" label="Savings" />
                                    <el-option value="Investment Shares" label="Investment Shares" />
                                    <el-option value="Credit Card" label="Credit Card" />
                                    <el-option value="Other Creditor" label="Other Creditor" />
                                    <el-option value="Other" label="Other" />
                                </el-select>
                            </div>
                            
                            <div class="field">
                                <label>Description *</label>
                                <el-input v-model="asset.description" placeholder="Enter description" @change="handleFieldChange" />
                            </div>
                            
                            <div class="field">
                                <label>Value ($)</label>
                                <el-input-number 
                                    v-model="asset.value" 
                                    :precision="2" 
                                    :step="1000"
                                    placeholder="0.00"
                                    style="width: 100%"
                                    @change="handleFieldChange"
                                />
                            </div>
                            
                            <div class="field">
                                <label>Amount Owing ($)</label>
                                <el-input-number 
                                    v-model="asset.amount_owing" 
                                    :precision="2" 
                                    :step="1000"
                                    placeholder="0.00"
                                    style="width: 100%"
                                    @change="handleFieldChange"
                                />
                            </div>
                            
                            <div class="field" v-if="asset.asset_type === 'Property'">
                                <label>Address</label>
                                <el-input v-model="asset.address" placeholder="Enter property address" @change="handleFieldChange" />
                            </div>
                            
                            <div class="field">
                                <label>BG Type</label>
                                <el-select v-model="asset.bg_type" placeholder="Select BG type" style="width: 100%" @change="handleFieldChange">
                                    <el-option value="BG1" label="BG1" />
                                    <el-option value="BG2" label="BG2" />
                                </el-select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Summary Section -->
            <div class="summary-section" v-if="guarantor.assets && guarantor.assets.length > 0">
                <h3>Financial Summary</h3>
                <div class="summary-grid">
                    <div class="summary-item">
                        <label>Total Assets:</label>
                        <span>${{ formatNumber(calculateTotalAssets(guarantor)) }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { Plus, Delete } from '@element-plus/icons-vue';

const props = defineProps({
    guarantors: {
        type: Array,
        default: () => []
    }
});

const emit = defineEmits(['update:guarantors']);

// Create a reactive copy of guarantors data
const localGuarantors = ref(JSON.parse(JSON.stringify(props.guarantors || [])));

// Helper function to convert string numbers to actual numbers
const convertNumericFields = (data) => {
    if (Array.isArray(data)) {
        return data.map(item => convertNumericFields(item));
    } else if (typeof data === 'object' && data !== null) {
        const converted = {};
        for (const [key, value] of Object.entries(data)) {
            if (key === 'value' || key === 'amount_owing') {
                // Convert string numbers to actual numbers for asset fields
                converted[key] = value === null || value === undefined || value === '' ? null : parseFloat(value);
            } else if (typeof value === 'object' && value !== null) {
                converted[key] = convertNumericFields(value);
            } else {
                converted[key] = value;
            }
        }
        return converted;
    }
    return data;
};

// Initialize localGuarantors with proper numeric conversion
const initializeLocalGuarantors = (guarantors) => {
    return convertNumericFields(guarantors || []);
};

localGuarantors.value = initializeLocalGuarantors(props.guarantors);

// Debug logging
console.log("GuarantorAsset component received props:", props);
console.log("GuarantorAsset component localGuarantors:", localGuarantors.value);

// Watch for changes in props and update local data
watch(() => props.guarantors, (newGuarantors, oldGuarantors) => {
    // Only update if there's an actual change in structure
    if (newGuarantors && (!oldGuarantors || newGuarantors.length !== oldGuarantors?.length)) {
        console.log("GuarantorAsset props.guarantors changed:", newGuarantors);
        localGuarantors.value = initializeLocalGuarantors(newGuarantors);
        console.log("GuarantorAsset localGuarantors updated:", localGuarantors.value);
    }
}, { deep: false, immediate: false });

// Helper functions
const formatNumber = (value) => {
    if (!value || isNaN(value)) return '0.00';
    return parseFloat(value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
};

const calculateTotalAssets = (guarantor) => {
    if (!guarantor.assets) return 0;
    return guarantor.assets.reduce((sum, asset) => sum + (parseFloat(asset.value) || 0), 0);
};

// Function to emit updates
const emitUpdate = () => {
    // Create a deep copy and ensure numeric fields are properly formatted
    const dataToEmit = JSON.parse(JSON.stringify(localGuarantors.value));
    emit('update:guarantors', dataToEmit);
};

// Function to handle form field changes
const handleFieldChange = () => {
    emitUpdate();
};

// Asset management
const addAsset = (guarantorIndex) => {
    if (!localGuarantors.value[guarantorIndex].assets) {
        localGuarantors.value[guarantorIndex].assets = [];
    }
    
    localGuarantors.value[guarantorIndex].assets.push({
        asset_type: '',
        description: '',
        value: null,
        amount_owing: null,
        address: '',
        bg_type: 'BG1'
    });
    
    emitUpdate();
};

const removeAsset = (guarantorIndex, assetIndex) => {
    localGuarantors.value[guarantorIndex].assets.splice(assetIndex, 1);
    emitUpdate();
};
</script>

<style scoped>
.form {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.guarantor-section {
    border: 1px solid #e1e1e1;
    border-radius: 8px;
    padding: 20px;
    background-color: #fafafa;
}

.guarantor-header {
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid #2984DE;
}

.guarantor-header h2 {
    margin: 0 0 5px 0;
    color: #2984DE;
    font-size: 1.2rem;
}

.subtitle {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
    font-style: italic;
}

.section {
    margin-bottom: 25px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.section-header h3 {
    margin: 0;
    color: #333;
    font-size: 1.1rem;
}

.no-items {
    text-align: center;
    padding: 20px;
    color: #666;
    font-style: italic;
    background-color: #f5f5f5;
    border-radius: 4px;
}

.items-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.item-card {
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 15px;
    background-color: white;
}

.item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
}

.item-type {
    background-color: #2984DE;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 500;
}

.item-fields {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.field label {
    font-size: 0.85rem;
    font-weight: 500;
    color: #333;
}

.summary-section {
    margin-top: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 6px;
    border: 1px solid #e9ecef;
}

.summary-section h3 {
    margin: 0 0 15px 0;
    color: #333;
    font-size: 1rem;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
}

.summary-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background-color: white;
    border-radius: 4px;
    border: 1px solid #dee2e6;
}

.summary-item label {
    font-weight: 500;
    color: #495057;
}

:deep(.el-input-number) {
    width: 100%;
}

:deep(.el-select) {
    width: 100%;
}
</style>