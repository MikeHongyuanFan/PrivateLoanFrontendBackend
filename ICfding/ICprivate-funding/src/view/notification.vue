<template>
  <div class="notification">
    <!-- Notification Preferences Section -->
    <el-drawer
      v-model="showPreferences"
      title="Notification Preferences"
      direction="rtl"
      size="500px"
    >
      <el-form v-loading="loadingPreferences" :model="preferences" label-position="top">
        <el-form-item label="In-App Notifications">
          <div class="preference-group">
            <el-checkbox v-model="preferences.application_status_in_app">Application Status Changes</el-checkbox>
            <el-checkbox v-model="preferences.repayment_upcoming_in_app">Upcoming Repayments</el-checkbox>
            <el-checkbox v-model="preferences.repayment_overdue_in_app">Overdue Repayments</el-checkbox>
            <el-checkbox v-model="preferences.note_reminder_in_app">Note Reminders</el-checkbox>
            <el-checkbox v-model="preferences.document_uploaded_in_app">Document Uploads</el-checkbox>
            <el-checkbox v-model="preferences.signature_required_in_app">Signature Required</el-checkbox>
            <el-checkbox v-model="preferences.system_in_app">System Notifications</el-checkbox>
            <el-checkbox v-model="preferences.active_loan_payment_in_app">Loan Payment Alerts</el-checkbox>
            <el-checkbox v-model="preferences.active_loan_expiry_in_app">Loan Expiry Warnings</el-checkbox>
            <el-checkbox v-model="preferences.active_loan_critical_in_app">Critical Loan Alerts</el-checkbox>
            <el-checkbox v-model="preferences.active_loan_manual_in_app">Manual Loan Alerts</el-checkbox>
          </div>
        </el-form-item>
        
        <el-form-item label="Email Notifications">
          <div class="preference-group">
            <el-checkbox v-model="preferences.application_status_email">Application Status Changes</el-checkbox>
            <el-checkbox v-model="preferences.repayment_upcoming_email">Upcoming Repayments</el-checkbox>
            <el-checkbox v-model="preferences.repayment_overdue_email">Overdue Repayments</el-checkbox>
            <el-checkbox v-model="preferences.note_reminder_email">Note Reminders</el-checkbox>
            <el-checkbox v-model="preferences.document_uploaded_email">Document Uploads</el-checkbox>
            <el-checkbox v-model="preferences.signature_required_email">Signature Required</el-checkbox>
            <el-checkbox v-model="preferences.system_email">System Notifications</el-checkbox>
            <el-checkbox v-model="preferences.active_loan_payment_email">Loan Payment Alerts</el-checkbox>
            <el-checkbox v-model="preferences.active_loan_expiry_email">Loan Expiry Warnings</el-checkbox>
            <el-checkbox v-model="preferences.active_loan_critical_email">Critical Loan Alerts</el-checkbox>
            <el-checkbox v-model="preferences.active_loan_manual_email">Manual Loan Alerts</el-checkbox>
          </div>
        </el-form-item>
        
        <el-form-item label="Email Digest">
          <div class="preference-group">
            <el-checkbox v-model="preferences.daily_digest">Daily Digest</el-checkbox>
            <el-checkbox v-model="preferences.weekly_digest">Weekly Digest</el-checkbox>
          </div>
        </el-form-item>
        
        <el-button type="primary" @click="savePreferences" :loading="savingPreferences">
          Save Preferences
        </el-button>
      </el-form>
    </el-drawer>

    <!-- Header Section -->
    <div class="header">
      <div class="select_title">
        <div @click="showAll" class="all" :class="{ active: !showUnreadOnly }">All</div>
        <div @click="showUnread" class="unread" :class="{ active: showUnreadOnly }">
          Unread
          <el-badge v-if="unreadCount > 0" :value="unreadCount" class="unread-badge" />
        </div>
      </div>
      <div class="actions">
        <el-button @click="showPreferences = true" link>
          <el-icon><Setting /></el-icon>
          Preferences
        </el-button>
        <el-button @click="markAllAsRead" type="primary" plain :loading="markingAllAsRead">
          Mark All as Read
        </el-button>
        <el-button @click="clearAllNotifications" type="danger" plain>
          Clear All
        </el-button>
      </div>
    </div>

    <!-- Notifications List -->
    <div class="list" v-loading="loading">
      <el-table
        ref="notificationTable"
        :data="paginatedNotifications"
        style="width: 100%"
        :show-header="false"
        :row-class-name="tableRowClassName"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" align="center" width="50" />
        <el-table-column label="Type" width="220">
          <template #default="scope">
            <div class="notification-type">
              <el-icon :size="20">
                <component :is="getNotificationIcon(scope.row.notification_type)" />
              </el-icon>
              <div class="type-details">
                <h1>{{ getNotificationTypeLabel(scope.row.notification_type) }}</h1>
                <p>{{ formatDate(scope.row.created_at) }}</p>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="Message">
          <template #default="scope">
            <div class="notification-message">
              {{ scope.row.message || scope.row.title || 'No message available' }}
            </div>
          </template>
        </el-table-column>
        <el-table-column width="100">
          <template #default="scope">
            <el-button
              v-if="!scope.row.is_read"
              @click="markAsRead(scope.row.id)"
              link
              :loading="markingRead === scope.row.id"
            >
              Mark as Read
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Batch Actions and Pagination -->
      <div class="multiple">
        <div class="select">
          <el-checkbox
            v-model="selectAll"
            :indeterminate="isIndeterminate"
            @change="handleCheckAllChange"
          />
          <el-button
            v-if="selectedNotifications.length > 0"
            @click="markSelectedAsRead"
            type="primary"
            plain
            :loading="markingBatch"
          >
            Mark Selected as Read
          </el-button>
        </div>
        <el-pagination
          v-if="totalNotifications > 0"
          layout="prev, pager, next"
          background
          :total="totalNotifications"
          :page-size="pageSize"
          :current-page="currentPage"
          @current-change="handlePageChange"
          class="mt-4"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Setting, Bell, Calendar, Document, Warning } from '@element-plus/icons-vue'
import { notificationApi } from '@/api/notifications'
import { formatDistanceToNow } from 'date-fns'

// State
const loading = ref(false)
const loadingPreferences = ref(false)
const savingPreferences = ref(false)
const markingRead = ref(null)
const markingAllAsRead = ref(false)
const markingBatch = ref(false)
const showPreferences = ref(false)
const showUnreadOnly = ref(false)
const currentPage = ref(1)
const pageSize = 10
const notifications = ref([])
const totalNotifications = ref(0)
const unreadCount = ref(0)
const selectedNotifications = ref([])
const selectAll = ref(false)
const isIndeterminate = ref(false)
const notificationTable = ref(null)

// Preferences state
const preferences = ref({
  // In-app preferences
  application_status_in_app: true,
  repayment_upcoming_in_app: true,
  repayment_overdue_in_app: true,
  note_reminder_in_app: true,
  document_uploaded_in_app: true,
  signature_required_in_app: true,
  system_in_app: true,
  active_loan_payment_in_app: true,
  active_loan_expiry_in_app: true,
  active_loan_critical_in_app: true,
  active_loan_manual_in_app: true,
  
  // Email preferences
  application_status_email: true,
  repayment_upcoming_email: true,
  repayment_overdue_email: true,
  note_reminder_email: true,
  document_uploaded_email: false,
  signature_required_email: true,
  system_email: false,
  active_loan_payment_email: true,
  active_loan_expiry_email: true,
  active_loan_critical_email: true,
  active_loan_manual_email: true,
  
  // Digest preferences
  daily_digest: false,
  weekly_digest: false
})

// Computed
const paginatedNotifications = computed(() => {
  return notifications.value
})

// Methods
const loadNotifications = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize
    }
    if (showUnreadOnly.value) {
      params.is_read = false
    }
    console.log('Loading notifications with params:', params)
    const response = await notificationApi.getDetailedNotifications(params)
    console.log('Notifications response:', response)
    
    // Handle the [null, data] response format from sendRequest
    const [error, data] = response
    if (error) {
      console.error('Error in notification response:', error)
      ElMessage.error('Failed to load notifications')
      return
    }
    
    console.log('Notifications data:', data)
    console.log('Total count:', data?.count)
    
    notifications.value = data?.results || []
    totalNotifications.value = data?.count || 0
    
    // Debug: Log the structure of the first notification
    if (data?.results && data.results.length > 0) {
      console.log('First notification object:', data.results[0])
      console.log('Available fields:', Object.keys(data.results[0]))
    }
    
    await updateUnreadCount()
  } catch (error) {
    console.error('Error loading notifications:', error)
    ElMessage.error('Failed to load notifications')
  } finally {
    loading.value = false
  }
}

const loadPreferencesData = async () => {
  try {
    loadingPreferences.value = true
    const response = await notificationApi.getNotificationPreferences()
    
    // Handle the [null, data] response format from sendRequest
    const [error, data] = response
    if (error) {
      console.error('Error loading preferences:', error)
      ElMessage.error('Failed to load notification preferences')
      return
    }
    
    preferences.value = data
  } catch (error) {
    ElMessage.error('Failed to load notification preferences')
  } finally {
    loadingPreferences.value = false
  }
}

const savePreferences = async () => {
  try {
    savingPreferences.value = true
    
    // Ensure preferences object is properly structured
    const preferencesToSave = { ...preferences.value }
    
    // Remove any undefined or null values
    Object.keys(preferencesToSave).forEach(key => {
      if (preferencesToSave[key] === undefined || preferencesToSave[key] === null) {
        delete preferencesToSave[key]
      }
    })
    
    console.log('Saving preferences data:', preferencesToSave)
    const response = await notificationApi.updateNotificationPreferences(preferencesToSave)
    
    // Handle the [null, data] response format from sendRequest
    const [error, data] = response
    if (error) {
      console.error('Error saving preferences:', error)
      ElMessage.error('Failed to save preferences')
      return
    }
    
    ElMessage.success('Preferences saved successfully')
    showPreferences.value = false
  } catch (error) {
    console.error('Error saving preferences:', error)
    ElMessage.error('Failed to save preferences')
  } finally {
    savingPreferences.value = false
  }
}

const updateUnreadCount = async () => {
  try {
    const response = await notificationApi.getUnreadCount()
    
    // Handle the [null, data] response format from sendRequest
    const [error, data] = response
    if (error) {
      console.error('Error fetching unread count:', error)
      return
    }
    
    unreadCount.value = data?.unread_count || 0
  } catch (error) {
    console.error('Failed to fetch unread count:', error)
  }
}

const markAsRead = async (id) => {
  try {
    markingRead.value = id
    await notificationApi.markAsRead(id)
    await loadNotifications()
  } catch (error) {
    ElMessage.error('Failed to mark notification as read')
  } finally {
    markingRead.value = null
  }
}

const markAllAsRead = async () => {
  try {
    markingAllAsRead.value = true
    await notificationApi.markAllAsRead()
    await loadNotifications()
    ElMessage.success('All notifications marked as read')
  } catch (error) {
    ElMessage.error('Failed to mark all notifications as read')
  } finally {
    markingAllAsRead.value = false
  }
}

const markSelectedAsRead = async () => {
  if (selectedNotifications.value.length === 0) return

  try {
    markingBatch.value = true
    const ids = selectedNotifications.value.map(n => n.id)
    await notificationApi.markBatchAsRead(ids)
    await loadNotifications()
    ElMessage.success('Selected notifications marked as read')
    selectedNotifications.value = []
  } catch (error) {
    ElMessage.error('Failed to mark selected notifications as read')
  } finally {
    markingBatch.value = false
  }
}

const handleSelectionChange = (selection) => {
  selectedNotifications.value = selection
  const checkedCount = selection.length
  const totalCount = notifications.value.length
  selectAll.value = checkedCount === totalCount
  isIndeterminate.value = checkedCount > 0 && checkedCount < totalCount
}

const handleCheckAllChange = (val) => {
  if (notificationTable.value) {
    notificationTable.value.toggleAllSelection()
  }
  isIndeterminate.value = false
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadNotifications()
}

const showAll = () => {
  showUnreadOnly.value = false
  loadNotifications()
}

const showUnread = () => {
  showUnreadOnly.value = true
  loadNotifications()
}

const tableRowClassName = ({row}) => {
  return row.is_read ? 'read' : ''
}

const formatDate = (date) => {
  return formatDistanceToNow(new Date(date), { addSuffix: true })
}

const getNotificationTypeLabel = (type) => {
  const labels = {
    application_status: 'Application Status',
    repayment_upcoming: 'Upcoming Repayment',
    repayment_overdue: 'Overdue Repayment',
    note_reminder: 'Reminder',
    document_uploaded: 'Document Upload',
    signature_required: 'Signature Required',
    system: 'System Notification',
    active_loan_payment: 'Loan Payment Alert',
    active_loan_expiry: 'Loan Expiry Warning',
    active_loan_critical: 'Critical Loan Alert',
    active_loan_manual: 'Loan Alert'
  }
  return labels[type] || type
}

const getNotificationIcon = (type) => {
  const icons = {
    application_status: Bell,
    repayment_upcoming: Calendar,
    repayment_overdue: Warning,
    note_reminder: Bell,
    document_uploaded: Document,
    signature_required: Document,
    system: Bell,
    active_loan_payment: Calendar,
    active_loan_expiry: Warning,
    active_loan_critical: Warning,
    active_loan_manual: Bell
  }
  return icons[type] || Bell
}

const clearAllNotifications = async () => {
  try {
    await notificationApi.markAllAsRead()
    ElMessage.success('All notifications marked as read')
    await loadNotifications()
  } catch (error) {
    console.error('Error clearing notifications:', error)
    ElMessage.error('Failed to clear notifications')
  }
}

// Lifecycle
onMounted(async () => {
  await loadNotifications()
  await loadPreferencesData()
})
</script>

<style scoped>
.notification {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.select_title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.all, .unread {
  padding: 8px 16px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #7A858E;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.all.active, .unread.active {
  color: #384144;
  background-color: rgba(0, 0, 0, 0.05);
}

.unread {
  display: flex;
  align-items: center;
  gap: 8px;
}

.unread-badge :deep(.el-badge__content) {
  background-color: #1F63A9;
}

.list {
  width: 100%;
  padding: 20px;
  border-radius: 8px;
  background: #FFF;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05);
}

.notification-type {
  display: flex;
  align-items: center;
  gap: 12px;
}

.type-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.type-details h1 {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 500;
  color: #384144;
}

.type-details p {
  margin: 0;
  font-size: 0.75rem;
  color: #7A858E;
}

.multiple {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.select {
  display: flex;
  align-items: center;
  gap: 16px;
}

:deep(.el-table) {
  --el-table-border-color: transparent;
  --el-table-header-bg-color: transparent;
}

:deep(.el-table .cell) {
  padding: 16px 8px;
}

:deep(.el-table .read) {
  background-color: #F5F5F5;
}

:deep(.el-checkbox) {
  --el-checkbox-input-border: 1.5px solid #B2B3BD;
  --el-checkbox-checked-input-border-color: #1F63A9;
  --el-checkbox-checked-bg-color: #1F63A9;
  --el-checkbox-input-border-color-hover: #1F63A9;
}

:deep(.el-pagination) {
  --el-pagination-button-bg-color: #FFF;
  --el-pagination-button-disabled-bg-color: #FFF;
}

:deep(.el-pagination button) {
  border: 1.5px solid rgba(64, 64, 64, 0.16);
  border-radius: 4px;
  padding: 0 15px;
}

:deep(.el-pagination button:hover) {
  border-color: #1F63A9;
}

:deep(.el-pagination .btn-prev::after) {
  content: "Previous";
}

:deep(.el-pagination .btn-next::before) {
  content: "Next";
}

:deep(.el-drawer__header) {
  margin-bottom: 32px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-checkbox-group) {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preference-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preference-group .el-checkbox {
  margin-right: 0;
  margin-bottom: 8px;
}

:deep(.el-checkbox__label) {
  font-size: 14px;
  color: #384144;
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #1F63A9;
  border-color: #1F63A9;
}

:deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
  color: #1F63A9;
}
</style>