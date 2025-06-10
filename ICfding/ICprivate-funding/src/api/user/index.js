import sendRequest from '@/server/sendRequest'

// Authentication
export function login(params) {
  return sendRequest({
    url: '/api/users/auth/login/',
    method: 'post',
    data: params,
  })
}

export function logout(params) {
  return sendRequest({
    url: '/api/users/auth/logout/',
    method: 'post',
    data: params,
  })
}

// User Management
export function users(params) {
  // Log the actual parameters being sent to the API
  console.log('API call to /api/users/users/ with params:', params);
  
  // Ensure role parameter is correctly formatted if present
  if (params && params.role) {
    console.log('Role filter being applied:', params.role);
  }
  
  return sendRequest({
    url: '/api/users/users/',
    method: 'get',
    params: params,
  })
}

export function addUsers(params) {
  return sendRequest({
    url: '/api/users/users/',
    method: 'post',
    data: params,
  })
}

export function userInfo(params) {
  return sendRequest({
    url: `/api/users/users/${params}`,
    method: 'get',
  })
}

export function deleteUser(params) {
  return sendRequest({
    url: `/api/users/users/${params}`,
    method: 'delete',
  })
}

export function putUser(id, data) {
  return sendRequest({
    url: `/api/users/users/${id}`,
    method: 'put',
    data,
  })
}

export function patchUser(id, data) {
  return sendRequest({
    url: `/api/users/users/${id}`,
    method: 'patch',
    data,
  })
}

// Current User
export function getCurrentUser() {
  return sendRequest({
    url: '/api/users/users/me/',
    method: 'get',
  })
}

// Profile Management
export function getProfile() {
  return sendRequest({
    url: '/api/users/profile/',
    method: 'get',
  })
}

export function updateProfile(data) {
  return sendRequest({
    url: '/api/users/profile/update/',
    method: 'put',
    data,
  })
}

// Notifications
export function notifications(params) {
  return sendRequest({
    url: '/api/users/notifications/',
    method: 'get',
    params: params,
  })
}

export const userApi = {
  // Authentication
  login,
  logout,

  // User Management
  users,
  addUsers,
  userInfo,
  deleteUser,
  putUser,
  patchUser,

  // Current User
  getCurrentUser,

  // Profile Management
  getProfile,
  updateProfile,

  // Notifications
  notifications,
}
