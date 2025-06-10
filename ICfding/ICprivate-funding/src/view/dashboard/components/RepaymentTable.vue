<script setup>
import { ref, onMounted } from 'vue'
import { CircleCheck, View, Upload, Delete } from '@element-plus/icons-vue'
import { api } from '@/api'
import { ElMessageBox, ElMessage } from 'element-plus'

const emit = defineEmits(['refresh'])

const { repayments } = defineProps({
  repayments: Array
})

const viewDialogVisible = ref(false)
const currentRepayment = ref(null)
const loading = ref({
  markPaid: false,
  delete: false,
  upload: false
})

onMounted(() => {
})

const upload = async (id, file) => {
  loading.value.upload = true
  const [err, res] = await api.updateRepayments(id, file)
  if (!err) {
    ElMessage.success('Repayment updated successfully')
    emit('refresh')
  } else {
    ElMessage.error('Failed to update repayment')
    console.error(err)
  }
  loading.value.upload = false
}

const handleUpload = (row) => {
  const input = document.createElement('input')
  input.type = 'file'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) {
      row.file = file
      upload(row.id, row.file)
    }
  }
  input.click()  
}

const handleView = (row) => {
  currentRepayment.value = row
  viewDialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    'Are you sure you want to delete this repayment?',
    'Warning',
    {
      confirmButtonText: 'Delete',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  ).then(async () => {
    loading.value.delete = true
    try {
      const [err, res] = await api.deleteRepayment(row.id)
      if (!err) {
        ElMessage.success('Repayment deleted successfully')
        emit('refresh')
      } else {
        ElMessage.error('Failed to delete repayment')
        console.error(err)
      }
    } catch (error) {
      ElMessage.error('An error occurred')
      console.error(error)
    } finally {
      loading.value.delete = false
    }
  }).catch(() => {
    // User cancelled the action
  })
}

const markAsPaid = async (row) => {
  loading.value.markPaid = row.id
  try {
    const [err, res] = await api.markRepaymentAsPaid(row.id)
    if (!err) {
      ElMessage.success('Repayment marked as paid')
      emit('refresh')
    } else {
      ElMessage.error('Failed to mark repayment as paid')
      console.error(err)
    }
  } catch (error) {
    ElMessage.error('An error occurred')
    console.error(error)
  } finally {
    loading.value.markPaid = null
  }
}
</script>

<template>
  <el-table :data="repayments" class="table" :header-cell-style="{ background: '#f8f8f8', color: '#272727' }">
    <el-table-column type="selection" width="50" align="center" />
    <el-table-column prop="id" label="ID" />
    <el-table-column prop="application" label="Application" />
    <el-table-column prop="amount" label="Amount" />
    <el-table-column prop="status" label="Status" />
    <el-table-column prop="due_date" label="Due Date" />
    <el-table-column prop="paid_date" label="Paid Date" />
    <el-table-column prop="created_by_name" label="Created By" />
    <el-table-column label="Action" width="300" align="center">
      <template #default="scope">
        <el-button-group>
          <el-button class="view" :icon="View" @click="handleView(scope.row)" />
          <el-button class="record" v-if="!scope.row.paid_date" @click="markAsPaid(scope.row)" :loading="loading.markPaid === scope.row.id">
            <el-icon class="icon">
              <CircleCheck />
            </el-icon>
            Mark as Paid
          </el-button>
          <el-button @click="handleUpload(scope.row)" :loading="loading.upload">
            <el-icon class="icon">
              <Upload />
            </el-icon>
            Upload
          </el-button>
          <el-button class="delete" @click="handleDelete(scope.row)" :loading="loading.delete">
            <el-icon class="icon">
              <Delete />
            </el-icon>
          </el-button>
        </el-button-group>
      </template>
    </el-table-column>
  </el-table>

  <!-- Repayment Detail Dialog -->
  <el-dialog
    v-model="viewDialogVisible"
    title="Repayment Details"
    width="50%"
  >
    <div v-if="currentRepayment" class="repayment-detail">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="ID">{{ currentRepayment.id }}</el-descriptions-item>
        <el-descriptions-item label="Application">{{ currentRepayment.application }}</el-descriptions-item>
        <el-descriptions-item label="Amount">{{ currentRepayment.amount }}</el-descriptions-item>
        <el-descriptions-item label="Status">{{ currentRepayment.status }}</el-descriptions-item>
        <el-descriptions-item label="Due Date">{{ currentRepayment.due_date }}</el-descriptions-item>
        <el-descriptions-item label="Paid Date">{{ currentRepayment.paid_date || 'Not paid yet' }}</el-descriptions-item>
        <el-descriptions-item label="Created By">{{ currentRepayment.created_by_name }}</el-descriptions-item>
        <el-descriptions-item label="Created At">{{ currentRepayment.created_at }}</el-descriptions-item>
        <el-descriptions-item label="Updated At">{{ currentRepayment.updated_at }}</el-descriptions-item>
        <el-descriptions-item label="Invoice" v-if="currentRepayment.invoice_url">
          <el-link type="primary" :href="currentRepayment.invoice_url" target="_blank">View Invoice</el-link>
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="viewDialogVisible = false">Close</el-button>
        <el-button type="primary" v-if="currentRepayment && !currentRepayment.paid_date" @click="markAsPaid(currentRepayment); viewDialogVisible = false">
          Mark as Paid
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style lang="scss" scoped>
.table {
  height: 90%;

  .number {
    font-weight: 400;
    font-size: 12px;

    ::v-deep(.el-statistic__content) {
      font-size: 12px;
    }
  }

  .view {
    border: 1px solid #2984DE;
    color: #2984DE;
  }

  .record {
    border-top: 1px solid #1AAD0A;
    border-bottom: 1px solid #1AAD0A;
    border-right: 1px solid #1AAD0A;
    color: #1AAD0A;
  }

  .upload {
    border-top: 1px solid #B3BFCA;
    border-bottom: 1px solid #B3BFCA;
    border-right: 1px solid #B3BFCA;
    color: #B3BFCA;
  }

  .delete {
    border: 1px solid #F56C6C;
    color: #F56C6C;
  }

  .icon {
    margin-right: 6px;
  }

  ::v-deep(.el-button-group>.el-button:not(:last-child)) {
    margin-right: 0;
  }
}

.repayment-detail {
  margin: 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
