import sendRequest from '@/server/sendRequest'

// Notification Preferences
export function getNotificationPreferences() {
  return sendRequest({
    url: '/api/users/notification-preferences/',
    method: 'get'
  })
}

export function updateNotificationPreferences(data) {
  return sendRequest({
    url: '/api/users/notification-preferences/',
    method: 'put',
    data
  })
}

// Notifications List
export function getNotifications(params) {
  return sendRequest({
    url: '/api/users/notifications/',
    method: 'get',
    params
  })
}

export function getDetailedNotifications(params) {
  return sendRequest({
    url: '/api/users/notifications-viewset/',
    method: 'get',
    params
  })
}

export function getNotificationDetails(id) {
  return sendRequest({
    url: `/api/users/notifications-viewset/${id}/`,
    method: 'get'
  })
}

// Mark as Read
export function markAsRead(id) {
  return sendRequest({
    url: `/api/users/notifications-viewset/${id}/mark_as_read/`,
    method: 'post'
  })
}

export function markAllAsRead() {
  return sendRequest({
    url: '/api/users/notifications-viewset/mark_all_as_read/',
    method: 'post'
  })
}

export function markBatchAsRead(notificationIds) {
  return sendRequest({
    url: '/api/users/notifications/mark-read/',
    method: 'post',
    data: { notification_ids: notificationIds }
  })
}

// Unread Counts
export function getUnreadCount() {
  return sendRequest({
    url: '/api/users/notifications-viewset/unread_count/',
    method: 'get'
  })
}

export function getNotificationCount() {
  return sendRequest({
    url: '/api/users/notifications/count/',
    method: 'get'
  })
}

export const notificationApi = {
  getNotificationPreferences,
  updateNotificationPreferences,
  getNotifications,
  getDetailedNotifications,
  getNotificationDetails,
  markAsRead,
  markAllAsRead,
  markBatchAsRead,
  getUnreadCount,
  getNotificationCount
}