import sendRequest from '@/server/sendRequest'

export function brokers(params) {
  return sendRequest({
    url: '/api/brokers/',
    method: 'get',
    params: params,
  })
}
export function broker(params) {
  return sendRequest({
    url: `/api/brokers/${params}`,
    method: 'get',
  })
}
export function addBrokers(params) {
  return sendRequest({
    url: '/api/brokers/',
    method: 'post',
    data: params,
  })
}

export function deleteBrokers(params) {
  return sendRequest({
    url: `/api/brokers/${params}`,
    method: 'delete',
  })
}

export function putBrokers(id, data) {
  return sendRequest({
    url: `/api/brokers/${id}`,
    method: 'put',
    data,
  })
}

export function branches(params) {
  return sendRequest({
    url: '/api/brokers/branches/',
    method: 'get',
    params: params,
  })
}
export function branch(params) {
  return sendRequest({
    url: `/api/brokers/branches/${params}`,
    method: 'get',
  })
}

export function deleteBranch(params) {
  return sendRequest({
    url: `/api/brokers/branches/${params}`,
    method: 'delete',
  })
}

export function putBranch(id, data) {
  return sendRequest({
    url: `/api/brokers/branches/${id}`,
    method: 'put',
    data,
  })
}

export function addBranches(params) {
  return sendRequest({
    url: '/api/brokers/branches/',
    method: 'post',
    data: params,
  })
}

export function bdms(params) {
  return sendRequest({
    url: '/api/brokers/bdms/',
    method: 'get',
    params: params,
  })
}
export function bdm(params) {
  return sendRequest({
    url: `/api/brokers/bdms/${params}`,
    method: 'get',
  })
}
export function addBdms(params) {
  return sendRequest({
    url: '/api/brokers/bdms/create_with_branch/',
    method: 'post',
    data: params,
  })
}

export function deleteBdms(params) {
  return sendRequest({
    url: `/api/brokers/bdms/${params}`,
    method: 'delete',
  })
}
export function putBdms(id, data) {
  return sendRequest({
    url: `/api/brokers/bdms/${id}`,
    method: 'put',
    data,
  })
}

// Applications endpoints
export function brokerApplications(brokerId) {
  return sendRequest({
    url: `/api/brokers/${brokerId}/applications/`,
    method: 'get',
  })
}

export function branchApplications(branchId) {
  return sendRequest({
    url: `/api/brokers/branches/${branchId}/applications/`,
    method: 'get',
  })
}

export function bdmApplications(bdmId) {
  return sendRequest({
    url: `/api/brokers/bdms/${bdmId}/applications/`,
    method: 'get',
  })
}

export function bdmBrokers(bdmId) {
  return sendRequest({
    url: `/api/brokers/bdms/${bdmId}/brokers/`,
    method: 'get',
  })
}

export function lockCommissionAccount(brokerId) {
  return sendRequest({
    url: `/api/brokers/${brokerId}/lock_commission_account/`,
    method: 'post',
  })
}

export function unlockCommissionAccount(brokerId) {
  return sendRequest({
    url: `/api/brokers/${brokerId}/unlock_commission_account/`,
    method: 'post',
  })
}

export function bdmDropdown(params) {
  return sendRequest({
    url: '/api/brokers/bdms/dropdown/',
    method: 'get',
    params: params,
  })
}

// Branch related endpoints
export function branchBrokers(branchId) {
  return sendRequest({
    url: `/api/brokers/branches/${branchId}/brokers/`,
    method: 'get',
  })
}

export const brokerApi = {
  brokers,
  broker,
  addBrokers,
  deleteBrokers,
  putBrokers,
  branches,
  branch,
  addBranches,
  deleteBranch,
  putBranch,
  bdms,
  bdm,
  addBdms,
  deleteBdms,
  putBdms,
  brokerApplications,
  branchApplications,
  bdmApplications,
  bdmBrokers,
  branchBrokers,
  bdmDropdown,
  lockCommissionAccount,
  unlockCommissionAccount,
}

