<template>
    <div class="valuer-management">
        <div class="header">
            <h1>Valuer Management</h1>
            <el-button type="primary" @click="showCreateDialog = true">
                <el-icon><Plus /></el-icon>
                Add New Valuer
            </el-button>
        </div>

        <!-- Search and Filters -->
        <div class="filters">
            <el-input
                v-model="searchTerm"
                placeholder="Search valuers..."
                style="width: 300px; margin-right: 15px;"
                clearable
                @input="handleSearch"
            >
                <template #prefix>
                    <el-icon><Search /></el-icon>
                </template>
            </el-input>
            
            <el-select v-model="statusFilter" placeholder="All Status" style="width: 150px; margin-right: 15px;" @change="loadValuers">
                <el-option label="All Status" value="" />
                <el-option label="Active" value="true" />
                <el-option label="Inactive" value="false" />
            </el-select>

            <el-button @click="resetFilters">Clear Filters</el-button>
        </div>

        <!-- Valuers Table -->
        <el-table 
            :data="valuers" 
            style="width: 100%" 
            v-loading="loading"
            empty-text="No valuers found"
        >
            <el-table-column prop="company_name" label="Company Name" sortable />
            <el-table-column prop="contact_name" label="Contact Name" sortable />
            <el-table-column prop="phone" label="Phone" />
            <el-table-column prop="email" label="Email" />
            <el-table-column prop="application_count" label="Applications" width="120" align="center" />
            <el-table-column prop="is_active" label="Status" width="100" align="center">
                <template #default="{ row }">
                    <el-tag :type="row.is_active ? 'success' : 'danger'">
                        {{ row.is_active ? 'Active' : 'Inactive' }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="created_at" label="Created" width="120" sortable>
                <template #default="{ row }">
                    {{ formatDate(row.created_at) }}
                </template>
            </el-table-column>
            <el-table-column label="Actions" width="150" align="center">
                <template #default="{ row }">
                    <el-button size="small" @click="editValuer(row)">
                        <el-icon><Edit /></el-icon>
                    </el-button>
                    <el-button 
                        size="small" 
                        :type="row.is_active ? 'warning' : 'success'"
                        @click="toggleStatus(row)"
                    >
                        {{ row.is_active ? 'Deactivate' : 'Activate' }}
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- Pagination -->
        <div class="pagination">
            <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
            />
        </div>

        <!-- Create/Edit Dialog -->
        <el-dialog
            :title="isEditing ? 'Edit Valuer' : 'Add New Valuer'"
            v-model="showCreateDialog"
            width="600px"
            :close-on-click-modal="false"
        >
            <el-form
                ref="valuerFormRef"
                :model="valuerForm"
                :rules="valuerRules"
                label-width="120px"
            >
                <el-form-item label="Company Name" prop="company_name">
                    <el-input v-model="valuerForm.company_name" />
                </el-form-item>
                
                <el-form-item label="Contact Name" prop="contact_name">
                    <el-input v-model="valuerForm.contact_name" />
                </el-form-item>
                
                <el-form-item label="Phone" prop="phone">
                    <el-input v-model="valuerForm.phone" />
                </el-form-item>
                
                <el-form-item label="Email" prop="email">
                    <el-input v-model="valuerForm.email" type="email" />
                </el-form-item>
                
                <el-form-item label="Address">
                    <el-input v-model="valuerForm.address" type="textarea" :rows="3" />
                </el-form-item>
                
                <el-form-item label="Notes">
                    <el-input v-model="valuerForm.notes" type="textarea" :rows="3" />
                </el-form-item>
                
                <el-form-item label="Status">
                    <el-switch
                        v-model="valuerForm.is_active"
                        active-text="Active"
                        inactive-text="Inactive"
                    />
                </el-form-item>
            </el-form>
            
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="showCreateDialog = false">Cancel</el-button>
                    <el-button type="primary" @click="saveValuer" :loading="saving">
                        {{ isEditing ? 'Update' : 'Create' }}
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
    import { ref, reactive, onMounted } from 'vue';
    import { ElMessage, ElMessageBox } from 'element-plus';
    import { Plus, Search, Edit } from '@element-plus/icons-vue';
    import { api } from '@/api';

    // Reactive data
    const valuers = ref([]);
    const loading = ref(false);
    const saving = ref(false);
    const showCreateDialog = ref(false);
    const isEditing = ref(false);
    const searchTerm = ref('');
    const statusFilter = ref('');
    const currentPage = ref(1);
    const pageSize = ref(20);
    const total = ref(0);

    // Form data
    const valuerFormRef = ref();
    const valuerForm = reactive({
        id: null,
        company_name: '',
        contact_name: '',
        phone: '',
        email: '',
        address: '',
        notes: '',
        is_active: true
    });

    // Form validation rules
    const valuerRules = {
        company_name: [
            { required: true, message: 'Please enter company name', trigger: 'blur' }
        ],
        contact_name: [
            { required: true, message: 'Please enter contact name', trigger: 'blur' }
        ],
        phone: [
            { required: true, message: 'Please enter phone number', trigger: 'blur' }
        ],
        email: [
            { required: true, message: 'Please enter email address', trigger: 'blur' },
            { type: 'email', message: 'Please enter a valid email address', trigger: 'blur' }
        ]
    };

    // Load valuers
    const loadValuers = async () => {
        loading.value = true;
        try {
            const params = {
                page: currentPage.value,
                page_size: pageSize.value,
                search: searchTerm.value,
                ...(statusFilter.value !== '' && { is_active: statusFilter.value })
            };

            const [err, data] = await api.valuers(params);
            if (!err && data) {
                valuers.value = data.results || data;
                total.value = data.count || (Array.isArray(data) ? data.length : 0);
            } else {
                ElMessage.error('Failed to load valuers');
            }
        } catch (error) {
            console.error('Error loading valuers:', error);
            ElMessage.error('Error loading valuers');
        } finally {
            loading.value = false;
        }
    };

    // Handle search
    const handleSearch = () => {
        currentPage.value = 1;
        loadValuers();
    };

    // Reset filters
    const resetFilters = () => {
        searchTerm.value = '';
        statusFilter.value = '';
        currentPage.value = 1;
        loadValuers();
    };

    // Handle pagination
    const handleSizeChange = (newSize) => {
        pageSize.value = newSize;
        currentPage.value = 1;
        loadValuers();
    };

    const handleCurrentChange = (newPage) => {
        currentPage.value = newPage;
        loadValuers();
    };

    // Reset form
    const resetForm = () => {
        Object.assign(valuerForm, {
            id: null,
            company_name: '',
            contact_name: '',
            phone: '',
            email: '',
            address: '',
            notes: '',
            is_active: true
        });
        isEditing.value = false;
    };

    // Edit valuer
    const editValuer = (valuer) => {
        Object.assign(valuerForm, valuer);
        isEditing.value = true;
        showCreateDialog.value = true;
    };

    // Save valuer
    const saveValuer = async () => {
        try {
            await valuerFormRef.value.validate();
        } catch {
            return;
        }

        saving.value = true;
        try {
            let err, data;
            
            if (isEditing.value) {
                [err, data] = await api.updateValuer(valuerForm.id, valuerForm);
            } else {
                [err, data] = await api.addValuer(valuerForm);
            }

            if (!err && data) {
                ElMessage.success(`Valuer ${isEditing.value ? 'updated' : 'created'} successfully`);
                showCreateDialog.value = false;
                resetForm();
                loadValuers();
            } else {
                ElMessage.error(`Failed to ${isEditing.value ? 'update' : 'create'} valuer`);
            }
        } catch (error) {
            console.error('Error saving valuer:', error);
            ElMessage.error('Error saving valuer');
        } finally {
            saving.value = false;
        }
    };

    // Toggle status
    const toggleStatus = async (valuer) => {
        const action = valuer.is_active ? 'deactivate' : 'activate';
        
        try {
            await ElMessageBox.confirm(
                `Are you sure you want to ${action} this valuer?`,
                'Confirm Action',
                {
                    confirmButtonText: 'Yes',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }
            );

            let err;
            if (valuer.is_active) {
                [err] = await api.deactivateValuer(valuer.id);
            } else {
                [err] = await api.activateValuer(valuer.id);
            }

            if (!err) {
                ElMessage.success(`Valuer ${action}d successfully`);
                loadValuers();
            } else {
                ElMessage.error(`Failed to ${action} valuer`);
            }
        } catch (error) {
            if (error !== 'cancel') {
                console.error('Error toggling valuer status:', error);
                ElMessage.error('Error updating valuer status');
            }
        }
    };

    // Format date
    const formatDate = (dateString) => {
        if (!dateString) return '';
        return new Date(dateString).toLocaleDateString();
    };

    // Initialize
    onMounted(() => {
        loadValuers();
    });
</script>

<style scoped>
    .valuer-management {
        padding: 20px;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .header h1 {
        margin: 0;
        color: #2c3e50;
    }

    .filters {
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    }

    .pagination {
        margin-top: 20px;
        display: flex;
        justify-content: center;
    }

    .dialog-footer {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
    }
</style> 