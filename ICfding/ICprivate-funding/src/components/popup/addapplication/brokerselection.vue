<template>
    <div class="form">
        <div class="long_item">
            <h1>Broker & BDM Assignment <span class="required">*</span></h1>
            <span class="hint">Select the broker and Business Development Manager for this application</span>
        </div>
        
        <div class="item">
            <p>Broker <span class="required">*</span></p>
            <el-select 
                v-model="selection.broker" 
                placeholder="Select a broker"
                filterable
                clearable
                loading-text="Loading brokers..."
                :loading="loadingBrokers"
                style="width: 100%"
                @change="handleBrokerChange"
            >
                <el-option
                    v-for="broker in brokers"
                    :key="broker.id"
                    :label="broker.display_name"
                    :value="broker.id"
                >
                    <span style="float: left">{{ broker.display_name }}</span>
                    <span style="float: right; color: #8492a6; font-size: 13px">ID: {{ broker.id }}</span>
                </el-option>
            </el-select>
            <span class="hint">Choose the broker responsible for this application</span>
        </div>

        <div class="item">
            <p>Business Development Manager</p>
            <el-select 
                v-model="selection.bd_id" 
                placeholder="Select a BDM (optional)"
                filterable
                clearable
                loading-text="Loading BDMs..."
                :loading="loadingBDMs"
                style="width: 100%"
                @change="handleBDMChange"
            >
                <el-option
                    v-for="bdm in bdms"
                    :key="bdm.id"
                    :label="bdm.display_name"
                    :value="bdm.id"
                >
                    <span style="float: left">{{ bdm.display_name }}</span>
                    <span style="float: right; color: #8492a6; font-size: 13px">ID: {{ bdm.id }}</span>
                </el-option>
            </el-select>
            <span class="hint">Optional: Select the BDM overseeing this application</span>
        </div>

        <div class="item">
            <p>Branch/Subsidiary</p>
            <el-select 
                v-model="selection.branch_id" 
                placeholder="Select a branch/subsidiary (optional)"
                filterable
                clearable
                loading-text="Loading branches..."
                :loading="loadingBranches"
                style="width: 100%"
                @change="handleBranchChange"
            >
                <el-option
                    v-for="branch in branches"
                    :key="branch.id"
                    :label="branch.display_name"
                    :value="branch.id"
                >
                    <span style="float: left">{{ branch.display_name }}</span>
                    <span style="float: right; color: #8492a6; font-size: 13px">ID: {{ branch.id }}</span>
                </el-option>
            </el-select>
            <span class="hint">Optional: Select the branch/subsidiary for this application</span>
        </div>

        <div v-if="selection.broker || selection.bd_id || selection.branch_id" class="summary">
            <h2>Assignment Summary</h2>
            <div class="summary-item" v-if="selectedBroker">
                <strong>Broker:</strong> {{ selectedBroker.display_name }}
            </div>
            <div class="summary-item" v-if="selectedBDM">
                <strong>BDM:</strong> {{ selectedBDM.display_name }}
            </div>
            <div class="summary-item" v-if="selectedBranch">
                <strong>Branch/Subsidiary:</strong> {{ selectedBranch.display_name }}
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted } from 'vue';
    import { ElMessage } from 'element-plus';
    import { api } from '@/api';

    const props = defineProps({
        selection: {
            type: Object,
            required: true
        }
    });

    const emit = defineEmits(['update:selection']);

    // Reactive data
    const brokers = ref([]);
    const bdms = ref([]);
    const branches = ref([]);
    const loadingBrokers = ref(false);
    const loadingBDMs = ref(false);
    const loadingBranches = ref(false);

    // Computed properties for selected items
    const selectedBroker = computed(() => 
        brokers.value.find(broker => broker.id === props.selection.broker)
    );
    
    const selectedBDM = computed(() => 
        bdms.value.find(bdm => bdm.id === props.selection.bd_id)
    );
    
    const selectedBranch = computed(() => 
        branches.value.find(branch => branch.id === props.selection.branch_id)
    );

    // API calls for dropdown data
    const loadBrokers = async () => {
        try {
            loadingBrokers.value = true;
            
            // Get user info from localStorage for authentication
            let userInfo = localStorage.getItem('userInfo');
            if (!userInfo) {
                ElMessage.error('Please log in to access this feature');
                return;
            }
            userInfo = JSON.parse(userInfo);
            
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || ''}/api/brokers/dropdown/`, {
                headers: {
                    'Authorization': `Bearer ${userInfo.access}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                brokers.value = data || [];
            } else {
                console.error('Failed to load brokers:', response.statusText);
                ElMessage.error('Failed to load brokers');
            }
        } catch (error) {
            console.error('Error loading brokers:', error);
            ElMessage.error('Error loading brokers');
        } finally {
            loadingBrokers.value = false;
        }
    };

    const loadBDMs = async () => {
        try {
            loadingBDMs.value = true;
            
            // Get user info from localStorage for authentication
            let userInfo = localStorage.getItem('userInfo');
            if (!userInfo) {
                ElMessage.error('Please log in to access this feature');
                return;
            }
            userInfo = JSON.parse(userInfo);
            
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || ''}/api/brokers/bdms/dropdown/`, {
                headers: {
                    'Authorization': `Bearer ${userInfo.access}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                bdms.value = data || [];
            } else {
                console.error('Failed to load BDMs:', response.statusText);
                ElMessage.error('Failed to load BDMs');
            }
        } catch (error) {
            console.error('Error loading BDMs:', error);
            ElMessage.error('Error loading BDMs');
        } finally {
            loadingBDMs.value = false;
        }
    };

    const loadBranches = async () => {
        try {
            loadingBranches.value = true;
            
            // Get user info from localStorage for authentication
            let userInfo = localStorage.getItem('userInfo');
            if (!userInfo) {
                ElMessage.error('Please log in to access this feature');
                return;
            }
            userInfo = JSON.parse(userInfo);
            
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || ''}/api/brokers/branches/dropdown/`, {
                headers: {
                    'Authorization': `Bearer ${userInfo.access}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                branches.value = data || [];
            } else {
                console.error('Failed to load branches:', response.statusText);
                ElMessage.error('Failed to load branches');
            }
        } catch (error) {
            console.error('Error loading branches:', error);
            ElMessage.error('Error loading branches');
        } finally {
            loadingBranches.value = false;
        }
    };

    // Event handlers
    const handleBrokerChange = (value) => {
        const updatedSelection = { ...props.selection, broker: value };
        emit('update:selection', updatedSelection);
    };

    const handleBDMChange = (value) => {
        const updatedSelection = { ...props.selection, bd_id: value };
        emit('update:selection', updatedSelection);
    };

    const handleBranchChange = (value) => {
        const updatedSelection = { ...props.selection, branch_id: value };
        emit('update:selection', updatedSelection);
    };

    // Load data on component mount
    onMounted(() => {
        loadBrokers();
        loadBDMs();
        loadBranches();
    });
</script>

<style scoped>
    .form {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }
    
    .long_item {
        grid-column: 1 / 3;
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    
    .item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    
    .summary {
        grid-column: 1 / 3;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 5px;
        border: 1px solid #e1e4e8;
    }
    
    .summary h2 {
        color: #384144;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 10px 0;
    }
    
    .summary-item {
        margin: 5px 0;
        color: #384144;
        font-size: 0.8rem;
    }
    
    p {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 500;
        line-height: 16px;
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