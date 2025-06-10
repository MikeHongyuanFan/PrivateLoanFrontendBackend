import sendRequest from "@/server/sendRequest";

export function applicationStatus(params) {
  return sendRequest({
    url: "/api/reports/application-status/",
    method: "get",
    params,
  });
}

export function applicationVolume(params) {
  return sendRequest({
    url: "/api/reports/application-volume/",
    method: "get",
    params,
  });
}

export function repaymentCompliance(params) {
  return sendRequest({
    url: "/api/reports/repayment-compliance/",
    method: "get",
    params,
  });
}

export function repayments(params) {
  return sendRequest({
    url: "/api/documents/repayments/",
    method: "get",
    params,
  });
}

export function addRepayments(formData) {
  return sendRequest({
    url: "/api/documents/repayments/",
    method: "post",
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}

export function updateRepayments(params, data) {
  return sendRequest({
    url: `/api/documents/repayments/${params}/`,
    method: "patch",
    data: data
  });
}

export const dashboardApi = {
  applicationStatus,
  applicationVolume,
  repaymentCompliance,
  repayments,
  addRepayments,
  updateRepayments
};
