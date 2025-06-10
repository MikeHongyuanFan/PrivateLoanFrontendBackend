<template>
  <div class="user-container">
    <el-card v-loading="loading" shadow="never" class="user-card">
      <!-- Header section with user basic info -->
      <div class="user-header">
        <div class="user-avatar">
          <el-avatar :size="64">
            {{ userInitials }}
          </el-avatar>
        </div>
        <div class="user-info">
          <h1 class="user-name">{{ fullName }}</h1>
          <div class="user-meta">
            <el-tag :type="getRoleType(user?.role)" class="user-role">{{ formattedRole }}</el-tag>
            <span class="user-id">ID: {{ userId }}</span>
            <span class="user-created" v-if="user?.created_at">Member since {{ formattedDate }}</span>
          </div>
        </div>
        <div class="user-actions" v-if="canEdit">
          <el-button type="primary" @click="openEditDialog" size="small">
            <el-icon><Edit /></el-icon> Edit
          </el-button>
          <el-button type="danger" @click="confirmDelete" size="small" v-if="isAdmin && !isSelf">
            <el-icon><Delete /></el-icon> Delete
          </el-button>
        </div>
      </div>

      <!-- Main content with tabs -->
      <el-tabs v-model="activeTab" class="user-tabs">
        <!-- Overview tab -->
        <el-tab-pane label="Overview" name="overview">
          <div class="user-details">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="Full Name">{{ fullName }}</el-descriptions-item>
              <el-descriptions-item label="Email">{{ user?.email || 'Not provided' }}</el-descriptions-item>
              <el-descriptions-item label="Role">{{ formattedRole }}</el-descriptions-item>
              <el-descriptions-item label="Phone">{{ user?.phone || 'Not provided' }}</el-descriptions-item>
              <el-descriptions-item label="User ID" :span="2">{{ userId }}</el-descriptions-item>
              <el-descriptions-item label="Created" :span="2" v-if="user?.created_at">{{ formattedDate }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-tab-pane>

        <!-- Profile tab (only for current user) -->
        <el-tab-pane label="Profile" name="profile" v-if="isSelf">
          <el-form 
            ref="profileFormRef"
            :model="profileForm"
            :rules="formRules"
            label-position="top"
            class="profile-form">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="First Name" prop="first_name">
                  <el-input v-model="profileForm.first_name" placeholder="First Name" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Last Name" prop="last_name">
                  <el-input v-model="profileForm.last_name" placeholder="Last Name" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Email" prop="email">
                  <el-input v-model="profileForm.email" type="email" placeholder="Email" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Phone" prop="phone">
                  <el-input v-model="profileForm.phone" placeholder="Phone Number" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item>
              <el-button type="primary" @click="updateUserProfile" :loading="submitting">
                Update Profile
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- Edit user dialog -->
    <el-dialog 
      v-model="editDialogVisible" 
      title="Edit User" 
      width="500px"
      :close-on-click-modal="false"
      destroy-on-close>
      <el-form 
        ref="editFormRef"
        :model="editForm"
        :rules="formRules"
        label-position="top">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="First Name" prop="first_name">
              <el-input v-model="editForm.first_name" placeholder="First Name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Last Name" prop="last_name">
              <el-input v-model="editForm.last_name" placeholder="Last Name" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Email" prop="email">
              <el-input v-model="editForm.email" type="email" placeholder="Email" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Phone" prop="phone">
              <el-input v-model="editForm.phone" placeholder="Phone Number" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="Role" prop="role" v-if="isAdmin">
          <el-select v-model="editForm.role" placeholder="Select Role" class="w-100">
            <el-option label="Administrator" value="admin" />
            <el-option label="Broker" value="broker" />
            <el-option label="Business Development" value="bd" />
            <el-option label="Client" value="client" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="saveUserChanges" :loading="submitting">
            Save
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useUsers } from '@/hooks/useUsers';
import { Edit, Delete } from '@element-plus/icons-vue';

// Component setup
const route = useRoute();
const router = useRouter();
const userId = route.params.userId;

// State management
const activeTab = ref('overview');
const editDialogVisible = ref(false);
const submitting = ref(false);
const profileFormRef = ref(null);
const editFormRef = ref(null);
const isAdmin = ref(false); // We'll set this based on user role

// Get user management functions from hook
const { 
  user,
  profile,
  loading,
  getUser,
  getCurrentUser,
  getProfile,
  updateUser,
  updateProfile,
  deleteUser 
} = useUsers();

// Form models
const profileForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: ''
});

const editForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  role: ''
});

// Form validation rules
const formRules = {
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
  ]
};

// Computed properties
const fullName = computed(() => {
  if (!user.value) return 'Loading...';
  return `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim() || 'No Name';
});

const formattedDate = computed(() => {
  if (!user.value?.created_at) return 'N/A';
  return new Date(user.value.created_at).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
});

const formattedRole = computed(() => {
  if (!user.value?.role) return 'N/A';
  
  const roleMap = {
    'admin': 'Administrator',
    'broker': 'Broker',
    'bd': 'Business Development',
    'client': 'Client'
  };
  
  return roleMap[user.value.role] || user.value.role;
});

const userInitials = computed(() => {
  if (!user.value) return '';
  const first = user.value.first_name?.charAt(0) || '';
  const last = user.value.last_name?.charAt(0) || '';
  return (first + last).toUpperCase();
});

const isSelf = computed(() => {
  return userId === 'me' || (user.value && profile.value && user.value.id === profile.value.id);
});

const canEdit = computed(() => {
  return isAdmin.value || isSelf.value;
});

// Lifecycle hooks
onMounted(async () => {
  try {
    await Promise.all([
      loadUserData(),
      loadProfileData()
    ]);
    
    // Check if current user is admin
    if (profile.value?.role === 'admin') {
      isAdmin.value = true;
    }
  } catch (error) {
    console.error('Error loading user data:', error);
    ElMessage.error('Failed to load user data');
  }
});

// Methods
const loadUserData = async () => {
  try {
    if (userId === 'me') {
      await getCurrentUser();
    } else {
      await getUser(userId);
    }
  } catch (error) {
    console.error('Error loading user data:', error);
    throw error;
  }
};

const loadProfileData = async () => {
  try {
    await getProfile();
    if (isSelf.value) {
      updateProfileForm();
    }
  } catch (error) {
    console.error('Error loading profile data:', error);
    throw error;
  }
};

const updateProfileForm = () => {
  if (!profile.value) return;
  
  profileForm.value = {
    first_name: profile.value.first_name || '',
    last_name: profile.value.last_name || '',
    email: profile.value.email || '',
    phone: profile.value.phone || ''
  };
};

const updateEditForm = () => {
  if (!user.value) return;
  
  editForm.value = {
    first_name: user.value.first_name || '',
    last_name: user.value.last_name || '',
    email: user.value.email || '',
    phone: user.value.phone || '',
    role: user.value.role || ''
  };
};

const openEditDialog = () => {
  editDialogVisible.value = true;
  updateEditForm();
};

const updateUserProfile = async () => {
  if (!profileFormRef.value) return;
  
  try {
    await profileFormRef.value.validate(async (valid) => {
      if (!valid) {
        ElMessage.warning('Please correct the form errors');
        return;
      }
      
      submitting.value = true;
      const [err] = await updateProfile(profileForm.value);
      
      if (!err) {
        ElMessage.success('Profile updated successfully');
        await loadProfileData();
      }
    });
  } catch (error) {
    ElMessage.error('Failed to update profile');
    console.error('Error updating profile:', error);
  } finally {
    submitting.value = false;
  }
};

const saveUserChanges = async () => {
  if (!editFormRef.value) return;
  
  try {
    await editFormRef.value.validate(async (valid) => {
      if (!valid) {
        ElMessage.warning('Please correct the form errors');
        return;
      }
      
      submitting.value = true;
      const [err] = await updateUser(userId, editForm.value);
      
      if (!err) {
        ElMessage.success('User updated successfully');
        editDialogVisible.value = false;
        await loadUserData();
      }
    });
  } catch (error) {
    ElMessage.error('Failed to update user');
    console.error('Error updating user:', error);
  } finally {
    submitting.value = false;
  }
};

const confirmDelete = () => {
  ElMessageBox.confirm(
    'Are you sure you want to delete this user? This action cannot be undone.',
    'Delete User',
    {
      confirmButtonText: 'Delete',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  ).then(async () => {
    try {
      submitting.value = true;
      const [err] = await deleteUser(userId);
      
      if (!err) {
        ElMessage.success('User deleted successfully');
        router.push('/users');
      }
    } catch (error) {
      ElMessage.error('Failed to delete user');
      console.error('Error deleting user:', error);
    } finally {
      submitting.value = false;
    }
  }).catch(() => {
    // User cancelled the deletion
  });
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
</script>

<style scoped>
.user-container {
  padding: 20px;
}

.user-card {
  background-color: #fff;
  border-radius: 8px;
}

.user-header {
  display: flex;
  align-items: center;
  padding-bottom: 24px;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 24px;
}

.user-avatar {
  margin-right: 24px;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #303133;
}

.user-meta {
  display: flex;
  gap: 16px;
  color: #909399;
  font-size: 14px;
  align-items: center;
}

.user-role {
  font-weight: 500;
}

.user-actions {
  display: flex;
  gap: 12px;
}

.user-tabs {
  margin-top: 16px;
}

.user-details {
  padding: 16px 0;
}

.profile-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 16px 0;
}

.w-100 {
  width: 100%;
}

@media (max-width: 768px) {
  .user-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .user-avatar {
    margin-right: 0;
    margin-bottom: 16px;
  }
  
  .user-meta {
    flex-wrap: wrap;
  }
  
  .user-actions {
    margin-top: 16px;
    align-self: flex-end;
  }
}
</style>

