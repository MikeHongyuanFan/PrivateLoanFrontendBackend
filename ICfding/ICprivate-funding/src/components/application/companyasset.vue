<template>
    <div class="content">
        <el-table v-loading="loading" :data="assets" style="width: 100%">
            <el-table-column prop="asset_type" label="Asset Type" min-width="120">
                <template #default="{ row }">{{ row.asset_type || '-' }}</template>
            </el-table-column>
            <el-table-column prop="description" label="Description" min-width="200">
                <template #default="{ row }">{{ row.description || '-' }}</template>
            </el-table-column>
            <el-table-column prop="value" label="Value" min-width="120">
                <template #default="{ row }">{{ formatCurrency(row.value) }}</template>
            </el-table-column>
            <el-table-column prop="amount_owing" label="Amount Owing" min-width="120">
                <template #default="{ row }">{{ formatCurrency(row.amount_owing) }}</template>
            </el-table-column>
            <el-table-column prop="to_be_refinanced" label="To Be Refinanced" min-width="120">
                <template #default="{ row }">{{ row.to_be_refinanced ? 'Yes' : 'No' }}</template>
            </el-table-column>
            <el-table-column prop="address" label="Address" min-width="200">
                <template #default="{ row }">{{ row.address || '-' }}</template>
            </el-table-column>
        </el-table>
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="!loading && (!assets || assets.length === 0)" class="empty-state">No assets found</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/api'

const props = defineProps({
    borrowerId: { type: Number, required: true }
})

const assets = ref([])
const loading = ref(false)
const error = ref(null)

const formatCurrency = (value) => {
    if (!value) return '-'
    return new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD' }).format(value)
}

const fetchAssets = async () => {
    loading.value = true
    error.value = null
    try {
        const [err, data] = await api.getBorrowerAssets(props.borrowerId)
        if (err) {
            throw new Error('Failed to fetch assets')
        }
        assets.value = data.results || []
    } catch (err) {
        error.value = 'Error loading assets. Please try again.'
        ElMessage.error('Failed to load company assets')
        console.error('Error fetching assets:', err)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    if (props.borrowerId) fetchAssets()
})
</script>

<style scoped>
.content {
    padding: 20px;
    border-radius: 6px;
    background: #FFF;
}
.error-message {
    color: #f56c6c;
    font-size: 14px;
    margin-top: 10px;
    text-align: center;
}
.empty-state {
    color: #909399;
    font-size: 14px;
    text-align: center;
    padding: 20px;
}
:deep(.el-table) {
    --el-table-border-color: #E8EBEE;
    --el-table-header-bg-color: #F8F9FA;
    --el-table-row-hover-bg-color: #F8F9FA;
}
:deep(.el-table th) {
    background-color: #F8F9FA;
    color: #7A858E;
    font-weight: 600;
    font-size: 12px;
}
:deep(.el-table td) {
    color: #384144;
    font-size: 12px;
}
</style>