<template>
    <div class="user">
        <el-card class="filter-card" shadow="never">
            <div class="filters">
                <div class="left">
                    <el-form :inline="true" :model="searchForm" @submit.prevent="handleSearch">
                        <el-form-item label="Search">
                            <el-input
                                v-model="searchForm.search"
                                placeholder="Search by name, email..."
                                prefix-icon="Search"
                                clearable
                                @clear="handleSearch"
                                @keyup.enter="handleSearch"
                            />
                        </el-form-item>
                        <el-form-item label="Role">
                            <el-select
                                v-model="searchForm.role"
                                style="width: 200px;"
                                placeholder="Select Role"
                                clearable
                                @clear="handleSearch"
                                @change="handleSearch"
                            >
                                <el-option label="Administrator" value="admin" />
                                <el-option label="Broker" value="broker" />
                                <el-option label="Business Development" value="bd" />
                                <el-option label="Client" value="client" />
                            </el-select>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="handleSearch" :loading="loading">
                                <el-icon><Search /></el-icon> Search
                            </el-button>
                            <el-button @click="handleClear" :disabled="loading">
                                <el-icon><RefreshRight /></el-icon> Reset
                            </el-button>
                        </el-form-item>
                    </el-form>
                </div>
                <el-button type="primary" @click="handleAdd" :disabled="loading">
                    <el-icon><Plus /></el-icon> Create User
                </el-button>
            </div>
        </el-card>

        <el-card class="list-card" shadow="never">
            <el-table
                ref="userListTable" 
                v-loading="loading"
                :data="users" 
                style="width: 100%"
                :default-sort="{ prop: 'id', order: 'ascending' }" 
                row-key="id"
                @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection" align="center" width="50" fixed />
                <el-table-column prop="id" label="User ID" sortable width="100">
                    <template #default="{ row }">
                        <el-link type="primary" @click="handleView(row)">#{{ row.id }}</el-link>
                    </template>
                </el-table-column>
                <el-table-column label="Name" min-width="180" sortable>
                    <template #default="{ row }">
                        <div class="user-info">
                            <el-avatar :size="32">
                                {{ getUserInitials(row) }}
                            </el-avatar>
                            <div class="user-details">
                                <span class="user-name">{{ row.first_name }} {{ row.last_name }}</span>
                                <span class="user-email">{{ row.email }}</span>
                            </div>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="role" label="Role" width="150">
                    <template #default="{ row }">
                        <el-tag :type="getRoleType(row.role)">
                            {{ formatRole(row.role) }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="phone" label="Phone" width="150" />
                <el-table-column prop="created_at" label="Created" width="180">
                    <template #default="{ row }">
                        {{ formatDate(row.created_at) }}
                    </template>
                </el-table-column>
                <el-table-column label="Actions" align="right" width="150" fixed="right">
                    <template #default="{ row }">
                        <el-button-group>
                            <el-button
                                type="primary"
                                link
                                @click="handleView(row)"
                                :title="'View user details'"
                            >
                                <el-icon><View /></el-icon>
                            </el-button>
                            <el-button
                                type="primary"
                                link
                                @click="handleEdit(row)"
                                :title="'Edit user'"
                            >
                                <el-icon><Edit /></el-icon>
                            </el-button>
                            <el-button
                                type="danger"
                                link
                                @click="handleDelete(row)"
                                :title="'Delete user'"
                            >
                                <el-icon><Delete /></el-icon>
                            </el-button>
                        </el-button-group>
                    </template>
                </el-table-column>
            </el-table>

            <div class="table-footer">
                <div class="bulk-actions" v-if="selectedItems.length">
                    <el-button type="danger" @click="handleBatchDelete" :loading="loading">
                        Delete Selected ({{ selectedItems.length }})
                    </el-button>
                </div>
                <el-pagination
                    v-model:current-page="searchForm.page"
                    v-model:page-size="searchForm.pageSize"
                    :page-sizes="[10, 20, 50, 100]"
                    :total="total"
                    background
                    layout="total, sizes, prev, pager, next, jumper"
                    @size-change="handleSizeChange"
                    @current-change="handlePageChange"
                />
            </div>
        </el-card>

        <!-- User Form Dialog -->
        <el-dialog 
            v-model="dialogVisible" 
            :title="dialogTitle"
            width="500px"
            :close-on-click-modal="false"
            destroy-on-close>
            <el-form 
                ref="userFormRef"
                :model="userForm"
                :rules="rules"
                label-position="top"
                @submit.prevent="handleSubmit">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="First Name" prop="first_name">
                            <el-input v-model="userForm.first_name" placeholder="First Name" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="Last Name" prop="last_name">
                            <el-input v-model="userForm.last_name" placeholder="Last Name" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="Email" prop="email">
                            <el-input v-model="userForm.email" type="email" placeholder="Email" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="Phone" prop="phone">
                            <el-input v-model="userForm.phone" placeholder="Phone Number" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item label="Role" prop="role">
                    <el-select v-model="userForm.role" placeholder="Select Role" class="w-100">
                        <el-option label="Administrator" value="admin" />
                        <el-option label="Broker" value="broker" />
                        <el-option label="Business Development" value="bd" />
                        <el-option label="Client" value="client" />
                    </el-select>
                </el-form-item>
                <el-form-item v-if="!editMode" label="Password" prop="password">
                    <el-input 
                        v-model="userForm.password" 
                        type="password" 
                        placeholder="Minimum 8 characters"
                        show-password />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">Cancel</el-button>
                    <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
                        {{ editMode ? 'Update' : 'Create' }}
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useUsers } from '@/hooks/useUsers';
import { Search, RefreshRight, Plus, View, Edit, Delete } from '@element-plus/icons-vue';

const router = useRouter();
const { users, total, loading, getUsers, createUser, updateUser, deleteUser } = useUsers();

// State
const userListTable = ref(null);
const userFormRef = ref(null);
const selectedItems = ref([]);
const dialogVisible = ref(false);
const editMode = ref(false);
const submitLoading = ref(false);
const currentUserId = ref(null);

// Form data
const searchForm = reactive({
  search: '',
  role: '',
  page: 1,
  pageSize: 20
});

const userForm = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  role: '',
  password: '',
});

// Form validation rules
const rules = {
  first_name: [
    { required: true, message: 'First name is required', trigger: 'blur' },
    { min: 2, max: 50, message: 'Length should be 2 to 50 characters', trigger: 'blur' }
  ],
  last_name: [
    { required: true, message: 'Last name is required', trigger: 'blur' },
    { min: 2, max: 50, message: 'Length should be 2 to 50 characters', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Email is required', trigger: 'blur' },
    { type: 'email', message: 'Please enter a valid email address', trigger: 'blur' }
  ],
  role: [
    { required: true, message: 'Role is required', trigger: 'change' }
  ],
  password: [
    { required: true, message: 'Password is required', trigger: 'blur' },
    { min: 8, message: 'Password must be at least 8 characters', trigger: 'blur' }
  ],
  username: [
    { required: true, message: 'Username is required', trigger: 'blur' },
    { min: 3, max: 30, message: 'Username should be 3 to 30 characters', trigger: 'blur' }
  ]
};

// Computed properties
const dialogTitle = computed(() => {
  return editMode.value ? 'Edit User' : 'Create New User';
});

// Lifecycle hooks
onMounted(() => {
  fetchUsers();
});

// Methods
const fetchUsers = async () => {
  // Create a custom filter function to filter users by role client-side
  const queryParams = {};
      
  // Only add parameters that have values
  if (searchForm.search) {
    queryParams.search = searchForm.search;
  }
  
  // Don't include role in API params, we'll filter client-side
  
  if (searchForm.page) {
    queryParams.page = searchForm.page;
  }
  
  if (searchForm.pageSize) {
    queryParams.page_size = searchForm.pageSize;
  }
  
  console.log('Fetching users with params:', queryParams);
  const [err, data] = await getUsers(queryParams);
  
  if (!err && data && data.results) {
    // If role filter is active, filter the results client-side
    if (searchForm.role) {
      console.log('Filtering users by role client-side:', searchForm.role);
      const filteredUsers = data.results.filter(user => user.role === searchForm.role);
      users.value = filteredUsers;
      total.value = filteredUsers.length;
    }
  }
};

const handleSearch = () => {
  searchForm.page = 1;
  fetchUsers();
};

const handleClear = () => {
  searchForm.search = '';
  searchForm.role = '';
  searchForm.page = 1;
  fetchUsers();
};

const handleSizeChange = (size) => {
  searchForm.pageSize = size;
  fetchUsers();
};

const handlePageChange = (page) => {
  searchForm.page = page;
  fetchUsers();
};

const handleSelectionChange = (selection) => {
  selectedItems.value = selection;
};

const handleAdd = () => {
  editMode.value = false;
  resetForm();
  dialogVisible.value = true;
};

const handleEdit = (row) => {
  editMode.value = true;
  currentUserId.value = row.id;
  
  // Fill the form with user data
  userForm.first_name = row.first_name || '';
  userForm.last_name = row.last_name || '';
  userForm.email = row.email || '';
  userForm.phone = row.phone || '';
  userForm.role = row.role || '';
  userForm.password = ''; // Don't fill password for edit mode
  
  dialogVisible.value = true;
};

const handleView = (row) => {
  router.push(`/user/${row.id}`);
};

const handleDelete = (row) => {
  ElMessageBox.confirm(
    'Are you sure you want to delete this user? This action cannot be undone.',
    'Delete User',
    {
      confirmButtonText: 'Delete',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  ).then(async () => {
    const [err] = await deleteUser(row.id);
    if (!err) {
      ElMessage.success('User deleted successfully');
      fetchUsers();
    }
  }).catch(() => {
    // User cancelled the deletion
  });
};

const handleBatchDelete = () => {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('Please select users to delete');
    return;
  }

  ElMessageBox.confirm(
    `Are you sure you want to delete ${selectedItems.value.length} selected users? This action cannot be undone.`,
    'Delete Users',
    {
      confirmButtonText: 'Delete',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  ).then(async () => {
    const deletePromises = selectedItems.value.map(item => deleteUser(item.id));
    
    try {
      await Promise.all(deletePromises);
      ElMessage.success(`${selectedItems.value.length} users deleted successfully`);
      fetchUsers();
    } catch (error) {
      ElMessage.error('Failed to delete some users');
    }
  }).catch(() => {
    // User cancelled the deletion
  });
};

const handleSubmit = async () => {
  if (!userFormRef.value) return;
  
  await userFormRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.warning('Please correct the form errors');
      return;
    }
    
    submitLoading.value = true;
    
    try {
      if (editMode.value) {
        // Update existing user
        const userData = { ...userForm };
        if (!userData.password) {
          delete userData.password; // Don't send empty password
        }
        
        const [err] = await updateUser(currentUserId.value, userData);
        if (!err) {
          ElMessage.success('User updated successfully');
          dialogVisible.value = false;
          fetchUsers();
        }
      } else {
        // Create new user
        const [err] = await createUser(userForm);
        if (!err) {
          ElMessage.success('User created successfully');
          dialogVisible.value = false;
          fetchUsers();
        }
      }
    } catch (error) {
      console.error('Error submitting user form:', error);
      ElMessage.error('An error occurred while saving user data');
    } finally {
      submitLoading.value = false;
    }
  });
};

const resetForm = () => {
  userForm.first_name = '';
  userForm.last_name = '';
  userForm.email = '';
  userForm.phone = '';
  userForm.role = '';
  userForm.password = '';
  
  if (userFormRef.value) {
    userFormRef.value.resetFields();
  }
};

// Helper functions
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const formatRole = (role) => {
  if (!role) return 'N/A';
  
  const roles = {
    'admin': 'Administrator',
    'broker': 'Broker',
    'bd': 'Business Development',
    'client': 'Client'
  };
  
  return roles[role] || role;
};

const getRoleType = (role) => {
  const types = {
    'admin': 'danger',
    'broker': 'success',
    'bd': 'warning',
    'client': 'info'
  };
  
  return types[role] || 'info';
};

const getUserInitials = (user) => {
  if (!user) return '';
  const first = user.first_name?.charAt(0) || '';
  const last = user.last_name?.charAt(0) || '';
  return (first + last).toUpperCase();
};
</script>

<style scoped>
.user {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  flex: 1;
}

.list-card {
  margin-bottom: 20px;
}

.table-footer {
  display: flex;
  justify-content: end;
  align-items: center;
  margin-top: 20px;
}

.bulk-actions {
  margin-right: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.user-details {
  margin-left: 10px;
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  color: #303133;
}

.user-email {
  font-size: 12px;
  color: #909399;
}

.w-100 {
  width: 100%;
}

    :deep(.el-table .el-table__cell) {
        padding: 0;
    }
    :deep(.el-table tbody .cell) {
        height: auto;
        padding: 0 5px;
        color: #272727;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 400;
        line-height: 140%;
    }
    :deep(.el-table th.el-table__cell) {
        background: #F8F8F8;
    }
    :deep(.el-table thead .cell) {
        padding: 10px 5px;
        color: #272727;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 140%;
    }

    :deep(.el-pagination) {
        --el-pagination-button-bg-color: #FFF;
        --el-pagination-button-disabled-bg-color: #FFF;
    }
    :deep(.el-pager li) {
        background: #FFF;
        color: rgba(0, 0, 0, 0.20);
        border-radius: 4px;
        border: 1.5px solid rgba(64, 64, 64, 0.16);
        font-weight: 500;
    }
    :deep(.el-pager li):hover {
        border: 1.5px solid #2984DE;
    }
    :deep(.el-pagination button) {
        height: 32px;
        padding: 0 15px;
        gap: 5px;
        border-radius: 4px;
        color: #1F1F1F;
        border: 1.5px solid rgba(64, 64, 64, 0.16);
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 140%;
    }
    :deep(.el-pagination button):hover {
        border: 1.5px solid #2984DE;
    }
    :deep(.el-pagination .btn-prev) {
        margin-right: 8px;
    }
    :deep(.el-pagination .btn-prev::after) {
        content: "Previous";
    }
    :deep(.el-pagination .btn-next) {
        margin-left: 8px;
    }
    :deep(.el-pagination .btn-next::before) {
        content: "Next";
    }
    :deep(.el-pagination.is-background .btn-prev:disabled) {
        background: #FFF;
    }
    :deep(.el-pagination.is-background .btn-next:disabled) {
        background: #FFF;
    }
    :deep(.el-pagination.is-background .el-pager li.is-active) {
        background: rgba(114, 114, 114, 0.08);
        color: #625E5E;
        font-weight: 500;
    }

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .left {
    margin-bottom: 15px;
    width: 100%;
  }
  
  .table-footer {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .bulk-actions {
    margin-bottom: 15px;
  }
}
</style>
