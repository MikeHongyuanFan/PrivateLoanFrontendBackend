<template>
  <div class="notification">
    <!-- Notification Preferences Section -->
    <el-drawer
      v-model="showPreferences"
      title="Notification Preferences"
      direction="rtl"
      size="400px"
    >
      <el-form v-loading="loadingPreferences" :model="preferences" label-position="top">
        <el-form-item label="Email Notifications">
          <el-switch v-model="preferences.email_enabled" />
        </el-form-item>
        <el-form-item label="Push Notifications">
          <el-switch v-model="preferences.push_enabled" />
        </el-form-item>
        <el-form-item label="Notification Types">
          <el-checkbox-group v-model="preferences.notification_types">
            <el-checkbox label="application_status">Application Status Changes</el-checkbox>
            <el-checkbox label="repayment_upcoming">Upcoming Repayments</el-checkbox>
            <el-checkbox label="repayment_overdue">Overdue Repayments</el-checkbox>
            <el-checkbox label="note_reminder">Note Reminders</el-checkbox>
            <el-checkbox label="document_uploaded">Document Uploads</el-checkbox>
            <el-checkbox label="signature_required">Signature Required</el-checkbox>
            <el-checkbox label="system">System Notifications</el-checkbox>
          </el-checkbox-group>
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
        <el-button @click="showPreferences = true" type="text">
          <el-icon><Setting /></el-icon>
          Preferences
        </el-button>
        <el-button @click="markAllAsRead" type="primary" plain :loading="markingAllAsRead">
          Mark All as Read
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
        <el-table-column prop="message" label="Message" />
        <el-table-column width="100">
          <template #default="scope">
            <el-button
              v-if="!scope.row.is_read"
              @click="markAsRead(scope.row.id)"
              type="text"
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
import { ref, computed, onMounted } from 'vue'
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
  email_enabled: false,
  push_enabled: false,
  notification_types: []
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
    const response = await notificationApi.getDetailedNotifications(params)
    notifications.value = response.results
    totalNotifications.value = response.count
    await updateUnreadCount()
  } catch (error) {
    ElMessage.error('Failed to load notifications')
  } finally {
    loading.value = false
  }
}

const loadPreferencesData = async () => {
  try {
    loadingPreferences.value = true
    const response = await notificationApi.getNotificationPreferences()
    preferences.value = response
  } catch (error) {
    ElMessage.error('Failed to load notification preferences')
  } finally {
    loadingPreferences.value = false
  }
}

const savePreferences = async () => {
  try {
    savingPreferences.value = true
    await notificationApi.updateNotificationPreferences(preferences.value)
    ElMessage.success('Preferences saved successfully')
    showPreferences.value = false
  } catch (error) {
    ElMessage.error('Failed to save preferences')
  } finally {
    savingPreferences.value = false
  }
}

const updateUnreadCount = async () => {
  try {
    const response = await notificationApi.getUnreadCount()
    unreadCount.value = response.count
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
    system: 'System Notification'
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
    system: Bell
  }
  return icons[type] || Bell
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
</style>