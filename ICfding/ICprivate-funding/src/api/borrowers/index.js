import sendRequest from '@/server/sendRequest'

//http://3.25.83.191/api/borrowers/borrowers/
export function borrowers(params) {
  return sendRequest({
    url: '/api/borrowers/borrowers/',
    method: 'get',
    params: params,
  })
}

export function addBorrowers(params) {
  return sendRequest({
    url: '/api/borrowers/borrowers/',
    method: 'post',
    data: params,
  })
}
export function borrower(params) {
  return sendRequest({
    url: `/api/borrowers/borrowers/${params}`,
    method: 'get',
  })
}
//http://3.25.83.191/api/borrowers/borrowers/{id}/
export function deleteBorrower(params) {
  return sendRequest({
    url: `/api/borrowers/borrowers/${params}`,
    method: 'delete',
  })
}
export function putBorrower(id, data) {
  return sendRequest({
    url: `/api/borrowers/borrowers/${id}`,
    method: 'put',
    data,
  })
}

// Company assets endpoints
export function getBorrowerAssets(borrowerId, params) {
  return sendRequest({
    url: `/api/borrowers/borrowers/${borrowerId}/assets/`,
    method: 'get',
    params,
  })
}

export function createBorrowerAsset(borrowerId, data) {
  return sendRequest({
    url: `/api/borrowers/borrowers/${borrowerId}/assets/`,
    method: 'post',
    data,
  })
}

export function getBorrowerAsset(borrowerId, assetId) {
  return sendRequest({
    url: `/api/borrowers/borrowers/${borrowerId}/assets/${assetId}/`,
    method: 'get',
  })
}

export function updateBorrowerAsset(borrowerId, assetId, data) {
  return sendRequest({
    url: `/api/borrowers/borrowers/${borrowerId}/assets/${assetId}/`,
    method: 'put',
    data,
  })
}

export function deleteBorrowerAsset(borrowerId, assetId) {
  return sendRequest({
    url: `/api/borrowers/borrowers/${borrowerId}/assets/${assetId}/`,
    method: 'delete',
  })
}

export function guarantors(params) {
  return sendRequest({
    url: '/api/borrowers/guarantors/',
    method: 'get',
    params: params,
  })
}
export function guarantor(params) {
  return sendRequest({
    url: `/api/borrowers/guarantors/${params}`,
    method: 'get',
  })
}

export const borrowerApi = {
  borrowers,
  borrower,
  guarantors,
  guarantor,
  addBorrowers,
  deleteBorrower,
  putBorrower,
  // Add company assets API functions
  getBorrowerAssets,
  createBorrowerAsset,
  getBorrowerAsset,
  updateBorrowerAsset,
  deleteBorrowerAsset,
}
