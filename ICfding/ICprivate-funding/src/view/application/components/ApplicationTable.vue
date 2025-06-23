<script setup>
    import { ref, onMounted, computed } from 'vue'
    import { CircleCheck, View, Upload, InfoFilled } from '@element-plus/icons-vue'
    import { useRouter } from 'vue-router'
    import { api } from '@/api'
    import { ElMessageBox } from 'element-plus'

    const router = useRouter()

    const { selected, paginationInfo, data } = defineProps({
        selected: Object,
        paginationInfo: Object,
        data: Array
    })
    const emit = defineEmits(['getData', 'edit'])

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
    const handleDelete = (row) => {
        ElMessageBox.confirm('Confirm to delete data?')
            .then(async () => {
                const [err, res] = await api.deleteApplication(row.id)
                if (!err) {
                    console.log(res)
                    emit('getData')
                } else {
                    console.log(err)
                }
            })
            .catch(() => {
                // catch error
            })
        // borrowers.value = borrowers.value.filter(item => item !== row)
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

    const formatStageChange = (change) => {
        if (!change) return ''
        const timestamp = new Date(change.timestamp).toLocaleString()
        return `Changed from ${change.from_stage} to ${change.to_stage}\nBy: ${change.user}\nAt: ${timestamp}\n${change.notes ? `Notes: ${change.notes}` : ''}`
    }
</script>

<template>
    <el-table :data="paginatedData" class="table" :header-cell-style="{ background: '#f8f8f8', color: '#272727' }">
        <el-table-column type="selection" width="50" align="center" fixed />
        <el-table-column prop="reference_number" label="Reference Number" sortable width="200" />
        <el-table-column prop="borrower_name" label="Borrower" width="150" />
        <el-table-column prop="stage" label="Status" width="150">
            <template #default="scope">
                <div class="stage-info">
                    <el-tag :type="getStageTagType(scope.row.stage)" size="small">
                        {{ scope.row.stage_display || scope.row.stage }}
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
        <el-table-column prop="broker_name" label="Broker" width="120" />
        <el-table-column prop="bdm_name" label="BDM" width="100" />
        <el-table-column prop="branch_name" label="Branch/Subsidiary" width="120" />
        <el-table-column prop="guarantor_name" label="Guarantor" width="120" />
        <el-table-column prop="purpose" label="Case Purpose" width="150" />
        <el-table-column prop="product_name" label="Product" />
        <el-table-column prop="security_address" label="Security Address" width="200" />
        <el-table-column prop="loan_amount" label="Loan Amount" width="150">
            <template #default="scope">
                <el-statistic class="number" :value="Number(scope.row.approvedAmount)" v-if="scope.row.approvedAmount"
                    :precision="2" :formatter="(value) => `$ ${value.toFixed(2)}`" />
            </template>
        </el-table-column>
        <el-table-column prop="estimated_settlement_date" label="Settlement Date" width="150" />
        <el-table-column prop="update" label="Updated Date" width="150" />
        <el-table-column prop="create" label="Create Date" width="150" />
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
</style>
