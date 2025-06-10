<template>
    <div class="broker">
        <div class="filters">
            <div class="left">
                <div class="filter">
                    <h1>Search</h1>
                    <el-input v-model="selected.search" style="width: 200px" placeholder="Search..." clearable />
                </div>
                <div class="filter">
                    <h1>Branch</h1>
                    <el-select v-model="selected.branch" placeholder="Select Branch" clearable style="width: 200px"
                        @change="handleSelect">
                        <el-option v-for="item in branchesList" :key="item.id" :label="item.name" :value="item.id" />
                    </el-select>
                </div>
                <!-- <div class="filter">
                    <h1>Income Type</h1>
                    <el-select v-model="selectedincome" placeholder="Select Income Type" style="width: 200px">
                        <el-option v-for="item in incomes" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div> -->
                <Search @click="getBrokers"></Search>
                <Clear @click="handleClear"></Clear>
            </div>
            <Create :action="action" @click="addBroker"></Create>
        </div>
        <div class="container">
            <el-table ref="brokerListTable" :data="brokers" style="width: 100%"
                :default-sort="{ prop: 'createDate', order: 'ascending' }" :cell-style="{ padding: '10px 0' }"
                @selection-change="handleSelectionChange">
                <el-table-column type="selection" align="center" width="50" fixed />
                <el-table-column prop="id" label="Broker ID" sortable width="120" />
                <el-table-column prop="name" label="Name" min-width="139" />
                <el-table-column prop="company" label="Company" width="130" />
                <el-table-column prop="phone" label="Phone" width="130" />
                <el-table-column prop="application_count" label="Applications" min-width="120" />
                <el-table-column prop="email" label="Email Address" min-width="225" />
                <el-table-column prop="branch_name" label="Branch" width="160" />
                <el-table-column label="Action" align="center" width="60" fixed="right">
                    <template #default="{ row }">
                        <el-popover placement="bottom" trigger="hover" width="160" popper-class="user-popover">
                            <div class="actions">
                                <div class="action_user">Action</div>
                                <div class="action" @click="handleView(row)">
                                    <el-icon>
                                        <View />
                                    </el-icon>
                                    View
                                </div>
                                <div class="action" @click="handleEdit(row)">
                                    <el-icon>
                                        <Edit />
                                    </el-icon>
                                    Edit
                                </div>
                                <div class="action" @click="handleDelete(row)">
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
            <div class="multiple">
                <div class="select">
                    <!-- <el-checkbox v-model="selectAll" :indeterminate="isSelected" @change="handleCheckAllChange" />
                    <div class="table_buttons">
                        <DeleteButton @click="deleteSelect"></DeleteButton>
                        <Active></Active>
                        <Inactive></Inactive>
                    </div> -->
                </div>
                <el-pagination layout="prev, pager, next" background :total="total" :page-size="pageSize"
                    :current-page="selected.page" @current-change="handlePageChange" />
            </div>
        </div>
        <transition name="slide-right-popup">
            <AddBroker v-if="popup" :action="popupAction" :editId="editId" @close="close" @minimize="minimize">
            </AddBroker>
        </transition>
    </div>
</template>

<script setup>
import { onMounted, ref, onActivated, computed } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '@/api'
import AddBroker from '@/components/popup/addbroker.vue';
import Search from '@/components/buttons/search.vue';
import Clear from '@/components/buttons/clear.vue';
import Create from '@/components/buttons/create.vue';
import DeleteButton from '@/components/buttons/delete.vue';
import Active from '@/components/buttons/active.vue';
import Inactive from '@/components/buttons/inactive.vue';
import { ElMessageBox } from 'element-plus'

import useBranches from '@/hooks/useBranches'

const { branchesList } = useBranches()

const router = useRouter()
const popup = ref(false)

const incomes = ref([
    { value: "1", label: "1" },
    { value: "2", label: "2" }
])
const selected = ref({
    branch: "",
    search: "",
    page: 1,
})
const selectedincome = ref("")
const action = ref("Create Broker")
const popupAction = ref("")
const brokers = ref([])
const pageSize = 10
const total = ref(0)
const brokerListTable = ref()
const selectedItem = ref([])
const selectAll = ref(false)
const isSelected = ref(false)
const editId = ref("")

onMounted(() => {
    // getBrokers()
})

onActivated(() => {
    getBrokers()
})

// const paginatedData = computed(() => {
//     const start = (selected.value.page - 1) * pageSize
//     return brokers.value.slice(start, start + pageSize)
// })

const getBrokers = async () => {
    const [err, res] = await api.brokers(selected.value)
    if (!err) {
        console.log(res);
        total.value = res?.count || 0
        brokers.value = res.results
    } else {
        console.log(err)
    }
}
const handleClear = () => {
    selected.value.search = ''
    selected.value.branch = ''
    getBrokers()
}

const handleSelect = () => {
    getBrokers()
}

const addBroker = () => {
    popupAction.value = "Add Broker"
    popup.value = true
    editId.value = ""
}
const close = () => {
    popup.value = false
    getBrokers()
}
const minimize = () => {

}
const handleSelectionChange = (row) => {
    selectedItem.value = row
    selectAll.value = row.length === brokers.value.length
    isSelected.value = row.length > 0 && row.length < brokers.value.length
}
const handleCheckAllChange = (row) => {
    if (row) {
        brokerListTable.value.toggleAllSelection()
    } else {
        brokerListTable.value.clearSelection()
    }
    isSelected.value = false
}
const handleView = (row) => {
    router.push(`/broker/${row.id}`)
}
const handleEdit = (row) => {
    const id = row.name
    popupAction.value = `Edit ${id}`
    popup.value = true
    editId.value = row.id
}
const handleDelete = async (row) => {
    ElMessageBox.confirm('Confirm to delete data?')
        .then(async () => {
            const [err, res] = await api.deleteBrokers(row.id)
            if (!err) {
                getBrokers()
            } else {
                console.log(err)
            }
        })
        .catch(() => {
            // catch error
        })
    // brokers.value = brokers.value.filter(item => item !== row)

}
const deleteSelect = () => {
    console.log("selected", selectedItem)
    brokers.value = brokers.value.filter(
        item => !selectedItem.value.includes(item)
    )
    selectedItem.value = []
}
const handlePageChange = (page) => {
    selected.value.page = page
    getBrokers
}
</script>

<style scoped>
.broker {
    display: flex;
    flex-direction: column;
    gap: 20px;
    height: 100%;
}

.filters {
    padding: 20px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: end;
    border-radius: 6px;
    background: #FFF;
}

.left {
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: end;
    gap: 20px;
}

.filter {
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 10px;
}

h1 {
    color: #272727;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 600;
    line-height: 19px;
    margin: 0;
}

.container {
    flex: 1;
    padding: 20px;
    border-radius: 3px;
    background: #FFF;
    display: flex;
    flex-direction: column;
    gap: 20px;
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

.multiple {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.select {
    padding-left: 18px;
    display: flex;
    flex-direction: row;
    gap: 25px;
}

.table_buttons {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
}

:deep(.el-table .el-table__cell) {
    padding: 0;
}

:deep(.el-table tbody .cell) {
    height: auto;
    padding: 0 5px;
    color: #272727;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.75rem;
    font-style: normal;
    font-weight: 400;
    line-height: 140%;
}

:deep(.el-table th.el-table__cell) {
    background: #F8F8F8;
}

:deep(.el-table thead .cell) {
    padding: 10px 5px;
    color: #272727;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.75rem;
    font-style: normal;
    font-weight: 600;
    line-height: 140%;
}

:deep(.el-checkbox) {
    --el-checkbox-input-border: 1.5px solid #B2B3BD;
    --el-checkbox-checked-input-border-color: #2984DE;
    --el-checkbox-checked-bg-color: #2984DE;
    --el-checkbox-input-border-color-hover: #2984DE;
}

:deep(.el-pagination) {
    --el-pagination-button-bg-color: #FFF;
    --el-pagination-button-disabled-bg-color: #FFF;
}

:deep(.el-pager li) {
    background: #FFF;
    color: rgba(0, 0, 0, 0.20);
    border-radius: 4px;
    border: 1.5px solid rgba(64, 64, 64, 0.16);
    font-weight: 500;
}

:deep(.el-pager li):hover {
    border: 1.5px solid #2984DE;
}

:deep(.el-pagination button) {
    height: 32px;
    padding: 0 15px;
    gap: 5px;
    border-radius: 4px;
    color: #1F1F1F;
    border: 1.5px solid rgba(64, 64, 64, 0.16);
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 500;
    line-height: 140%;
}

:deep(.el-pagination button):hover {
    border: 1.5px solid #2984DE;
}

:deep(.el-pagination .btn-prev::after) {
    content: "Previous";
}

:deep(.el-pagination .btn-next::before) {
    content: "Next";
}

:deep(.el-pagination.is-background .btn-prev:disabled) {
    background: #FFF;
}

:deep(.el-pagination.is-background .btn-next:disabled) {
    background: #FFF;
}

:deep(.el-pagination.is-background .el-pager li.is-active) {
    background: rgba(114, 114, 114, 0.08);
    color: #625E5E;
    font-weight: 500;
}

.slide-right-popup-enter-active,
.slide-right-popup-leave-active {
    transition: all 0.3s ease;
}

.slide-right-popup-enter-from,
.slide-right-popup-leave-to {
    opacity: 0;
    transform: translateX(100%);
}

.slide-right-popup-enter-to,
.slide-right-popup-leave-from {
    opacity: 1;
    transform: translateX(0);
}
</style>