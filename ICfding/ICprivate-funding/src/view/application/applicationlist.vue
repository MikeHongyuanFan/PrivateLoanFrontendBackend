<template>
    <div class="application">
        <div class="filters">
            <div class="left">
                <div class="filter">
                    <h1>Search</h1>
                    <el-input v-model="selected.search" style="width: 180px" placeholder="Search..." />
                </div>
                <!-- <div class="filter">
                    <h1>Location</h1>
                    <el-select v-model="selectedLocation" placeholder="Select Location" style="width: 180px">
                        <el-option v-for="item in locations" :key="item.value" :label="item.label"
                            :value="item.value" />
                    </el-select>
                </div>
                <div class="filter">
                    <h1>Income Type</h1>
                    <el-select v-model="selectedincome" placeholder="Select Income Type" style="width: 180px">
                        <el-option v-for="item in incomes" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div>
                <div class="date_picker">
                    <el-date-picker v-model="dateRange" type="daterange" start-placeholder="start" end-placeholder="end"
                        format="DD MMM" value-format="YYYY-MM-DD" :prefix-icon="Calendar" clearable
                        style="width: 180px;" />
                </div> -->
                <Search @click="toApplication"></Search>
                <Clear @click="handleClear"></Clear>
            </div>
            <Create :action="action" @click="addApplication"></Create>            
        </div>
        <!-- <div class="create">
            <Create :action="action" @click="addApplication"></Create>
        </div> -->
        <div class="container">
            <div class="tabs-scroll">
                <el-scrollbar>
                    <div class="tab-bar">
                        <div v-for="item in tabs" :key="item.name"
                            :class="['tab-item', { active: activeTab === item.name }]" @click="selectStatus(item.name)">
                            {{ item.label }}
                        </div>
                    </div>
                </el-scrollbar>
            </div>
            <div class="list">
                <ApplicationTable 
                    :selected="selected" 
                    :paginationInfo="paginationInfo"
                    :data="filteredApplications"
                    @getData="getApplications"
                    @edit="handleEdit"
                    @click="handleApplicationClick"
                ></ApplicationTable>
                <div class="flex">
                    <!-- <div class="select">
                        <el-checkbox v-model="selectAll" :indeterminate="isSelected" @change="handleCheckAllChange" />
                        <div class="table-buttons">
                            <DeleteButton @click="deleteSelect"></DeleteButton>
                        </div>
                    </div> -->
                    <Pagination :="paginationInfo" @change="handleChange"></Pagination>
                </div>
            </div>
        </div>
        <transition name="slide-right-popup">
            <div v-if="popup" class="popup-container">
                <AddApplication v-if="!isEditMode" 
                    :action="popupAction" 
                    @close="close" 
                    @minimize="minimize"
                ></AddApplication>
                <EditApplication v-else
                    :applicationId="editApplicationId"
                    @close="close"
                    @saved="handleApplicationSaved"
                ></EditApplication>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, onActivated, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { api } from '@/api';
import AddApplication from '@/components/popup/addapplication/index.vue';
import EditApplication from '@/view/application/edit/EditApplication.vue';
import Calendar from '@/components/icons/calendar.vue';
import Search from '@/components/buttons/search.vue';
import Clear from '@/components/buttons/clear.vue';
import Create from '@/components/buttons/create.vue';
import DeleteButton from '@/components/buttons/delete.vue';

import { Pagination } from '@/components'
import { ApplicationTable } from './components'
import { ElMessage } from 'element-plus';

const route = useRoute()
const popup = ref(false)
const isEditMode = ref(false)
const editApplicationId = ref(null)

const locations = ref([
    { value: "1", label: "1" },
    { value: "2", label: "2" }
])
const incomes = ref([
    { value: "1", label: "1" },
    { value: "2", label: "2" }
])
const tabs = [
    { name: 'all', label: 'All', width: '32px' },
    { name: 'received', label: 'Received', width: '58px' },
    { name: 'sent_to_lender', label: 'Sent to Lender/Investor', width: '86px' },
    { name: 'funding_table_issued', label: 'Funding Table Issued', width: '88px' },
    { name: 'indicative_letter_issued', label: 'Indicative Letter Issued', width: '89px' },
    { name: 'indicative_letter_signed', label: 'Indicative Letter Signed', width: '89px' },
    { name: 'commitment_fee_received', label: 'Commitment Fee Received', width: '73px' },
    { name: 'application_submitted', label: 'Application Submitted', width: '80px' },
    { name: 'valuation_ordered', label: 'Valuation Ordered', width: '69px' },
    { name: 'valuation_received', label: 'Valuation Received', width: '77px' },
    { name: 'more_info_required', label: 'More Info Required', width: '72px' },
    { name: 'formal_approval', label: 'Formal Approval', width: '72px' },
    { name: 'loan_docs_instructed', label: 'Loan Docs Instructed', width: '90px' },
    { name: 'loan_docs_issued', label: 'Loan Docs Issued', width: '59px' },
    { name: 'loan_docs_signed', label: 'Loan Docs Signed', width: '61px' },
    { name: 'settlement_conditions', label: 'Settlement Conditions', width: '82px' },
    { name: 'settled', label: 'Settled', width: '82px' },
    { name: 'closed', label: 'Closed', width: '82px' },
    { name: 'discharged', label: 'Discharged', width: '82px' }
]
const activeTab = ref('all')
const selected = ref({
    search: "",
    page: 1
})
const selectedLocation = ref("")
const selectedincome = ref("")
const dateRange = ref("")
const action = ref("Create Application")
const popupAction = ref("")
const applications = ref([])

const paginationInfo = ref({
    total: 0,
})
const selectAll = ref(false)
const isSelected = ref(false)

const router = useRouter();

onActivated(() => {
    getApplications()
    if (route.query.search) {
        selected.value.search = route.query.search
        getApplications()
    }    
})

const toApplication = () => {
    getApplications()
}
const handleClear = () => {
    selected.value = ({page: 1})
    getApplications()
}
const addApplication = () => {
    popupAction.value = "Add Application";
    isEditMode.value = false;
    popup.value = true;
}
const close = () => {
    popup.value = false;
    
    // Reset the edit mode and application ID when closing the popup
    editApplicationId.value = null;
    isEditMode.value = false;
}
const minimize = () => {

}

const getApplications = async () => {
    const [err, res] = await api.applications(selected.value)
    if (!err) {
        console.log(res);
        paginationInfo.value.total = res.count
        applications.value = res.results.map(item => ({
            ...item,
            create: item.created_at ? item.created_at.split('T')[0] : item.created_at,
            update: item.updated_at ? item.updated_at.split('T')[0] : item.updated_at
        }))
    } else {
        console.log(err)
    }
}

const handleChange = (currantPage) => {
    selected.value.page = currantPage
    console.log(selected.value.page);
}

// const handleCheckAllChange = (row) => {
//     if (row) {
//         applicationListTable.value.toggleAllSelection()
//     } else {
//         applicationListTable.value.clearSelection()
//     }
//     isSelected.value = false
// }

const handleEdit = (id) => {
    console.log("Edit button clicked for application ID:", id);
    editApplicationId.value = id;
    isEditMode.value = true;
    popup.value = true;
}
const selectStatus = (name) => {
    activeTab.value = name
}

const filteredApplications = computed(() => {
    if (activeTab.value === 'all') {
        return applications.value
    }
    return applications.value.filter(app => app.stage_display === activeTab.value)
})

const handleApplicationSaved = (savedData) => {
    console.log("Application saved successfully:", savedData);
    
    // Refresh the applications list to show updated data
    getApplications();
    
    // Optionally, you could update the specific application in the list without refetching all:
    // const appIndex = applications.value.findIndex(app => app.id === savedData.id);
    // if (appIndex !== -1) {
    //     applications.value[appIndex] = { ...applications.value[appIndex], ...savedData.data };
    // }
};

const handleApplicationClick = (id) => {
    console.log("=== APPLICATION CLICK DEBUG ===");
    console.log("Application clicked with ID:", id, "Type:", typeof id);
    console.log("ID value:", JSON.stringify(id));
    console.log("Is ID a number?", typeof id === 'number');
    console.log("Is ID a string?", typeof id === 'string');
    console.log("Is ID an object?", typeof id === 'object');
    
    // Validate that we received a proper ID
    if (!id || typeof id !== 'number' && typeof id !== 'string') {
        console.error("❌ Invalid application ID received:", id);
        console.error("ID type:", typeof id);
        console.error("ID constructor:", id?.constructor?.name);
        return;
    }
    
    // Convert to string if it's a number
    const applicationId = String(id);
    console.log("✅ Valid application ID:", applicationId);
    console.log("Navigating to application:", applicationId);
    
    try {
        console.log("Attempting router.push to:", `/application/${applicationId}`);
        router.push(`/application/${applicationId}`);
        console.log("✅ Router navigation successful");
    } catch (error) {
        console.error("❌ Navigation error:", error);
        // Fallback: try using window.location
        console.log("Attempting fallback navigation");
        window.location.href = `/application/${applicationId}`;
    }
};
</script>

<style lang="scss" scoped>
.application {
    display: flex;
    flex-direction: column;
    gap: 20px;
    height: 100%;
}
.create {
    width: 100%;
    display: flex;
    justify-content: end;
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

.date_picker {
    width: 200px;
}

:deep(.el-date-editor .el-range-input) {
    width: 50px !important;
}

:deep(.el-date-editor .el-range__icon) {
    font-size: 20px;
}

:deep(.el-date-editor .el-range-separator) {
    flex: 0;
}

.container {
    padding: 20px;
    flex: 1;
    border-radius: 3px;
    background: #FFF;
    overflow: hidden;

    .list {
        height: calc(100% - 44px);
        padding: 10px;
    }

    .flex {
        display: flex;
        align-items: center;
        justify-content: end;

        .select {
            margin-top: 20px;
            padding-left: 18px;
            display: flex;
            flex-direction: row;
            gap: 25px;
        }

        .table-buttons {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 10px;
        }
    }

    .left {
        display: flex;
        flex-direction: row;
        justify-content: start;
        align-items: end;
        gap: 20px;
    }

    .tabs-scroll {
        width: 100%;
        height: 48px;
        border-bottom: 1px solid #ccc;
    }

    .tab-bar {
        display: flex;
        width: fit-content;
        height: 44px;
    }

    .tab-item {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #949494;
        padding: 5px 9px;
        cursor: pointer;
        border-radius: 4px 4px 0 0;
        font-size: 12px;
        font-style: normal;
        font-weight: 400;
        transition: background 0.2s;
    }

    .tab-item:hover {
        background: #e0e0e0;
    }

    .tab-item.active {
        background: #2984DE;
        color: white;
        font-weight: 600;
    }
}

.popup-container {
    /* This is just a wrapper that doesn't affect styling */
    display: contents;
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