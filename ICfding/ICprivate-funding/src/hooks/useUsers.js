import { ref } from 'vue'
import { api } from '@/api'
import { ElMessage } from 'element-plus'

export function useUsers() {
    const users = ref([])
    const user = ref(null)
    const profile = ref(null)
    const loading = ref(false)
    const total = ref(0)

    const getUsers = async (params) => {
        loading.value = true
        try {
            // Create a clean params object with only defined values
            const cleanParams = {};
            
            // Only add parameters that have values
            if (params) {
                Object.keys(params).forEach(key => {
                    if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
                        cleanParams[key] = params[key];
                    }
                });
            }
            
            console.log('Fetching users with params:', cleanParams);
            
            const [err, res] = await api.users(cleanParams);
            
            if (!err && res) {
                users.value = res.results || [];
                total.value = res.count || 0;
                console.log('Users fetched successfully:', users.value.length, 'Total:', total.value);
                return [null, res];
            }
            
            console.error('API Error:', err);
            ElMessage.error(err?.message || err?.detail || 'Failed to fetch users');
            return [err, null];
        } catch (error) {
            console.error('Error fetching users:', error);
            ElMessage.error('An error occurred while fetching users');
            return [error, null];
        } finally {
            loading.value = false;
        }
    }

    const getUser = async (id) => {
        loading.value = true
        try {
            const [err, res] = await api.userInfo(id)
            if (!err && res) {
                user.value = res
                return [null, res]
            }
            ElMessage.error(err?.message || 'Failed to fetch user')
            return [err, null]
        } catch (error) {
            console.error('Error fetching user:', error)
            ElMessage.error('An error occurred while fetching user')
            return [error, null]
        } finally {
            loading.value = false
        }
    }

    const getCurrentUser = async () => {
        loading.value = true
        try {
            const [err, res] = await api.getCurrentUser()
            if (!err && res) {
                user.value = res
                return [null, res]
            }
            ElMessage.error(err?.message || 'Failed to fetch current user')
            return [err, null]
        } catch (error) {
            console.error('Error fetching current user:', error)
            ElMessage.error('An error occurred while fetching current user')
            return [error, null]
        } finally {
            loading.value = false
        }
    }

    const getProfile = async () => {
        loading.value = true
        try {
            const [err, res] = await api.getProfile()
            if (!err && res) {
                profile.value = res
                return [null, res]
            }
            ElMessage.error(err?.message || 'Failed to fetch profile')
            return [err, null]
        } catch (error) {
            console.error('Error fetching profile:', error)
            ElMessage.error('An error occurred while fetching profile')
            return [error, null]
        } finally {
            loading.value = false
        }
    }

    const createUser = async (userData) => {
        loading.value = true
        try {
            const [err, res] = await api.addUsers(userData)
            if (!err && res) {
                ElMessage.success('User created successfully')
                return [null, res]
            }
            ElMessage.error(err?.message || 'Failed to create user')
            return [err, null]
        } catch (error) {
            console.error('Error creating user:', error)
            ElMessage.error('An error occurred while creating user')
            return [error, null]
        } finally {
            loading.value = false
        }
    }

    const updateUser = async (id, userData) => {
        loading.value = true
        try {
            const [err, res] = await api.putUser(id, userData)
            if (!err && res) {
                ElMessage.success('User updated successfully')
                return [null, res]
            }
            ElMessage.error(err?.message || 'Failed to update user')
            return [err, null]
        } catch (error) {
            console.error('Error updating user:', error)
            ElMessage.error('An error occurred while updating user')
            return [error, null]
        } finally {
            loading.value = false
        }
    }

    const updateProfile = async (profileData) => {
        loading.value = true
        try {
            const [err, res] = await api.updateProfile(profileData)
            if (!err && res) {
                ElMessage.success('Profile updated successfully')
                return [null, res]
            }
            ElMessage.error(err?.message || 'Failed to update profile')
            return [err, null]
        } catch (error) {
            console.error('Error updating profile:', error)
            ElMessage.error('An error occurred while updating profile')
            return [error, null]
        } finally {
            loading.value = false
        }
    }

    const patchUser = async (id, userData) => {
        loading.value = true
        try {
            const [err, res] = await api.patchUser(id, userData)
            if (!err && res) {
                ElMessage.success('User updated successfully')
                return [null, res]
            }
            ElMessage.error(err?.message || 'Failed to update user')
            return [err, null]
        } catch (error) {
            console.error('Error updating user:', error)
            ElMessage.error('An error occurred while updating user')
            return [error, null]
        } finally {
            loading.value = false
        }
    }

    const deleteUser = async (id) => {
        loading.value = true
        try {
            const [err, res] = await api.deleteUser(id)
            if (!err) {
                ElMessage.success('User deleted successfully')
                return [null, res]
            }
            ElMessage.error(err?.message || 'Failed to delete user')
            return [err, null]
        } catch (error) {
            console.error('Error deleting user:', error)
            ElMessage.error('An error occurred while deleting user')
            return [error, null]
        } finally {
            loading.value = false
        }
    }

    return {
        users,
        user,
        profile,
        loading,
        total,
        getUsers,
        getUser,
        getCurrentUser,
        getProfile,
        createUser,
        updateUser,
        updateProfile,
        patchUser,
        deleteUser
    }
}
