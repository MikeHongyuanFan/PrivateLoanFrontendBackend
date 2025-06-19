<template>
    <div class="quantity-surveyor-management">
        <div class="header">
            <h1>Quantity Surveyor Management</h1>
            <el-button type="primary" @click="showCreateDialog = true">
                <el-icon><Plus /></el-icon>
                Add New Quantity Surveyor
            </el-button>
        </div>

        <!-- Search and Filters -->
        <div class="filters">
            <el-input
                v-model="searchTerm"
                placeholder="Search quantity surveyors..."
                style="width: 300px; margin-right: 15px;"
                clearable
                @input="handleSearch"
            >
                <template #prefix>
                    <el-icon><Search /></el-icon>
                </template>
            </el-input>
            
            <el-select v-model="statusFilter" placeholder="All Status" style="width: 150px; margin-right: 15px;" @change="loadQuantitySurveyors">
                <el-option label="All Status" value="" />
                <el-option label="Active" value="true" />
                <el-option label="Inactive" value="false" />
            </el-select>

            <el-button @click="resetFilters">Clear Filters</el-button>
        </div>

        <!-- Quantity Surveyors Table -->
        <el-table 
            :data="quantitySurveyors" 
            style="width: 100%" 
            v-loading="loading"
            empty-text="No quantity surveyors found"
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
                    <el-button size="small" @click="editQuantitySurveyor(row)">
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
            :title="isEditing ? 'Edit Quantity Surveyor' : 'Add New Quantity Surveyor'"
            v-model="showCreateDialog"
            width="600px"
            :close-on-click-modal="false"
        >
            <el-form
                ref="qsFormRef"
                :model="qsForm"
                :rules="qsRules"
                label-width="120px"
            >
                <el-form-item label="Company Name" prop="company_name">
                    <el-input v-model="qsForm.company_name" />
                </el-form-item>
                
                <el-form-item label="Contact Name" prop="contact_name">
                    <el-input v-model="qsForm.contact_name" />
                </el-form-item>
                
                <el-form-item label="Phone" prop="phone">
                    <el-input v-model="qsForm.phone" />
                </el-form-item>
                
                <el-form-item label="Email" prop="email">
                    <el-input v-model="qsForm.email" type="email" />
                </el-form-item>
                
                <el-form-item label="Address">
                    <el-input v-model="qsForm.address" type="textarea" :rows="3" />
                </el-form-item>
                
                <el-form-item label="Notes">
                    <el-input v-model="qsForm.notes" type="textarea" :rows="3" />
                </el-form-item>
                
                <el-form-item label="Status">
                    <el-switch
                        v-model="qsForm.is_active"
                        active-text="Active"
                        inactive-text="Inactive"
                    />
                </el-form-item>
            </el-form>
            
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="showCreateDialog = false">Cancel</el-button>
                    <el-button type="primary" @click="saveQuantitySurveyor" :loading="saving">
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
    const quantitySurveyors = ref([]);
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
    const qsFormRef = ref();
    const qsForm = reactive({
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
    const qsRules = {
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

    // Load quantity surveyors
    const loadQuantitySurveyors = async () => {
        loading.value = true;
        try {
            const params = {
                page: currentPage.value,
                page_size: pageSize.value,
                search: searchTerm.value,
                ...(statusFilter.value !== '' && { is_active: statusFilter.value })
            };

            const [err, data] = await api.quantitySurveyors(params);
            if (!err && data) {
                quantitySurveyors.value = data.results || data;
                total.value = data.count || (Array.isArray(data) ? data.length : 0);
            } else {
                ElMessage.error('Failed to load quantity surveyors');
            }
        } catch (error) {
            console.error('Error loading quantity surveyors:', error);
            ElMessage.error('Error loading quantity surveyors');
        } finally {
            loading.value = false;
        }
    };

    // Handle search
    const handleSearch = () => {
        currentPage.value = 1;
        loadQuantitySurveyors();
    };

    // Reset filters
    const resetFilters = () => {
        searchTerm.value = '';
        statusFilter.value = '';
        currentPage.value = 1;
        loadQuantitySurveyors();
    };

    // Handle pagination
    const handleSizeChange = (newSize) => {
        pageSize.value = newSize;
        currentPage.value = 1;
        loadQuantitySurveyors();
    };

    const handleCurrentChange = (newPage) => {
        currentPage.value = newPage;
        loadQuantitySurveyors();
    };

    // Reset form
    const resetForm = () => {
        Object.assign(qsForm, {
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

    // Edit quantity surveyor
    const editQuantitySurveyor = (qs) => {
        Object.assign(qsForm, qs);
        isEditing.value = true;
        showCreateDialog.value = true;
    };

    // Save quantity surveyor
    const saveQuantitySurveyor = async () => {
        try {
            await qsFormRef.value.validate();
        } catch {
            return;
        }

        saving.value = true;
        try {
            let err, data;
            
            if (isEditing.value) {
                [err, data] = await api.updateQuantitySurveyor(qsForm.id, qsForm);
            } else {
                [err, data] = await api.addQuantitySurveyor(qsForm);
            }

            if (!err && data) {
                ElMessage.success(`Quantity Surveyor ${isEditing.value ? 'updated' : 'created'} successfully`);
                showCreateDialog.value = false;
                resetForm();
                loadQuantitySurveyors();
            } else {
                ElMessage.error(`Failed to ${isEditing.value ? 'update' : 'create'} quantity surveyor`);
            }
        } catch (error) {
            console.error('Error saving quantity surveyor:', error);
            ElMessage.error('Error saving quantity surveyor');
        } finally {
            saving.value = false;
        }
    };

    // Toggle status
    const toggleStatus = async (qs) => {
        const action = qs.is_active ? 'deactivate' : 'activate';
        
        try {
            await ElMessageBox.confirm(
                `Are you sure you want to ${action} this quantity surveyor?`,
                'Confirm Action',
                {
                    confirmButtonText: 'Yes',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }
            );

            let err;
            if (qs.is_active) {
                [err] = await api.deactivateQuantitySurveyor(qs.id);
            } else {
                [err] = await api.activateQuantitySurveyor(qs.id);
            }

            if (!err) {
                ElMessage.success(`Quantity Surveyor ${action}d successfully`);
                loadQuantitySurveyors();
            } else {
                ElMessage.error(`Failed to ${action} quantity surveyor`);
            }
        } catch (error) {
            if (error !== 'cancel') {
                console.error('Error toggling quantity surveyor status:', error);
                ElMessage.error('Error updating quantity surveyor status');
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
        loadQuantitySurveyors();
    });
</script>

<style scoped>
    .quantity-surveyor-management {
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