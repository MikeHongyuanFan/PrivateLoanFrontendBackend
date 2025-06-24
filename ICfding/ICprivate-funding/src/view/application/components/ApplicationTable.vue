<script setup>
    import { ref, onMounted, computed } from 'vue'
    import { CircleCheck, View, Upload, InfoFilled } from '@element-plus/icons-vue'
    import { useRouter } from 'vue-router'
    import { api } from '@/api'
    import { ElMessageBox, ElMessage } from 'element-plus'

    const router = useRouter()

    const { selected, paginationInfo, data } = defineProps({
        selected: Object,
        paginationInfo: Object,
        data: Array
    })
    const emit = defineEmits(['getData', 'edit', 'click'])

    onMounted(() => {
    })

    const paginatedData = computed(() => {
        const start = (selected.page - 1) * 10
        return data.slice(start, start + 10)
    })

    const handleView = (row) => {
        router.push(`/application/${row.id}`)
    }
    const handleEdit = (row) => {
        emit('edit', row.id)
    }
    const handleDelete = async (row) => {
        try {
            await ElMessageBox.confirm(
                'Are you sure you want to delete this application?',
                'Warning',
                {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning',
                }
            )
            const [err, res] = await api.deleteApplication(row.id)
            if (!err) {
                ElMessage.success('Application deleted successfully')
                emit('refresh')
            } else {
                ElMessage.error('Failed to delete application')
            }
        } catch (error) {
            if (error !== 'cancel') {
                ElMessage.error('Failed to delete application')
            }
        }
    }

    const formatStageChange = (change) => {
        if (!change) return ''
        const timestamp = new Date(change.timestamp).toLocaleString()
        return `Changed from ${change.from_stage} to ${change.to_stage}\nBy: ${change.user}\nAt: ${timestamp}\n${change.notes ? `Notes: ${change.notes}` : ''}`
    }

    const getStageTagType = (stage) => {
        // Define tag types based on stage
        const stageTypes = {
            'received': 'info',
            'sent_to_lender': 'primary',
            'funding_table_issued': 'primary',
            'indicative_letter_issued': 'warning',
            'indicative_letter_signed': 'warning',
            'commitment_fee_received': 'success',
            'application_submitted': 'primary',
            'valuation_ordered': 'warning',
            'valuation_received': 'warning',
            'more_info_required': 'danger',
            'formal_approval': 'success',
            'loan_docs_instructed': 'primary',
            'loan_docs_issued': 'primary',
            'loan_docs_signed': 'success',
            'settlement_conditions': 'warning',
            'settled': 'success',
            'closed': 'info',
            'discharged': 'info'
        }
        return stageTypes[stage] || 'info'
    }
</script>

<template>
    <el-table :data="paginatedData" class="table" :header-cell-style="{ background: '#f8f8f8', color: '#272727' }">
        <el-table-column type="selection" width="50" align="center" fixed />
        <el-table-column prop="reference_number" label="Reference Number" width="150">
            <template #default="scope">
                <span>{{ scope.row.reference_number }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="borrower_name" label="Borrower" width="150">
            <template #default="scope">
                <span>{{ scope.row.borrower_name }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="stage" label="Status" width="150">
            <template #default="scope">
                <div class="stage-info">
                    <el-tag :type="getStageTagType(scope.row.stage)" size="small">
                        {{ scope.row.stage_display || scope.row.stage }}
                    </el-tag>
                    <!-- Archived indicator -->
                    <el-tag v-if="scope.row.is_archived" type="warning" size="small" style="margin-left: 5px;">
                        Archived
                    </el-tag>
                    <el-tooltip
                        v-if="scope.row.last_stage_change"
                        :content="formatStageChange(scope.row.last_stage_change)"
                        placement="right"
                        effect="light"
                    >
                        <el-icon class="history-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                </div>
            </template>
        </el-table-column>
        <el-table-column prop="broker_name" label="Broker" width="120">
            <template #default="scope">
                <span>{{ scope.row.broker_name }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="bdm_name" label="BDM" width="100">
            <template #default="scope">
                <span>{{ scope.row.bdm_name }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="branch_name" label="Branch/Subsidiary" width="120">
            <template #default="scope">
                <span>{{ scope.row.branch_name }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="guarantor_name" label="Guarantor" width="120">
            <template #default="scope">
                <span>{{ scope.row.guarantor_name }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="purpose" label="Case Purpose" width="150">
            <template #default="scope">
                <span>{{ scope.row.purpose }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="product_name" label="Product">
            <template #default="scope">
                <span>{{ scope.row.product_name }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="security_address" label="Security Address" width="200">
            <template #default="scope">
                <span>{{ scope.row.security_address }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="loan_amount" label="Loan Amount" width="150">
            <template #default="scope">
                <el-statistic class="number" :value="Number(scope.row.approvedAmount)" v-if="scope.row.approvedAmount"
                    :precision="2" :formatter="(value) => `$ ${value.toFixed(2)}`" />
            </template>
        </el-table-column>
        <el-table-column prop="estimated_settlement_date" label="Settlement Date" width="150">
            <template #default="scope">
                <span>{{ scope.row.estimated_settlement_date }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="update" label="Updated Date" width="150">
            <template #default="scope">
                <span>{{ scope.row.update }}</span>
            </template>
        </el-table-column>
        <el-table-column prop="create" label="Create Date" width="150">
            <template #default="scope">
                <span>{{ scope.row.create }}</span>
            </template>
        </el-table-column>
        <el-table-column label="Action" align="center" width="80" fixed="right">
            <template #default="scope">
                <el-popover placement="bottom" trigger="hover" width="160" popper-class="user-popover">
                    <div class="actions">
                        <div class="action_user">Action</div>
                        <div class="action" @click="handleView(scope.row)">
                            <el-icon>
                                <View />
                            </el-icon>
                            View
                        </div>
                        <div class="action" @click="handleEdit(scope.row)">
                            <el-icon>
                                <Edit />
                            </el-icon>
                            Edit
                        </div>
                        <div class="action" @click="handleDelete(scope.row)">
                            <el-icon>
                                <Delete />
                            </el-icon>
                            Delete
                        </div>
                    </div>
                    <template #reference>
                        <p class="show_action">···</p>
                    </template>
                </el-popover>
            </template>
        </el-table-column>
    </el-table>
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
}

.stage-info {
    display: flex;
    align-items: center;
    gap: 5px;
    flex-wrap: wrap;
}

.history-icon {
    margin-left: 5px;
    cursor: pointer;
    color: #666;
}
.actions {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.action_user {
    width: 100%;
    padding: 0 10px 10px 10px;
    border-bottom: 1.5px solid #E1E1E1;
    color: #272727;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 500;
    line-height: 19px;
}

.action {
    padding: 0 10px;
    display: flex;
    flex-direction: row;
    justify-content: start;
    gap: 10px;
    margin-bottom: 10px;
    align-items: center;
    cursor: pointer;
    color: #949494;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.8rem;
    font-style: normal;
    font-weight: 500;
    line-height: 19px;
}

.action:hover {
    color: #2984DE;
}

.action p:hover {
    color: #2984DE;
}

.show_action {
    width: 100%;
    font-size: 1.5rem;
    color: #969696;
    text-align: center;
    cursor: pointer;
    margin: 0;
}

.stage-info {
    display: flex;
    align-items: center;
    gap: 8px;
}

.history-icon {
    color: #909399;
    cursor: pointer;
    font-size: 16px;
}

.history-icon:hover {
    color: #2984DE;
}

.reference-link {
    color: #2984DE;
    text-decoration: none;
    cursor: pointer;
}

.reference-link:hover {
    text-decoration: underline;
}
</style>
