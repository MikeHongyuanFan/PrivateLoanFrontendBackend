<script setup>
import { ref, onMounted, computed } from 'vue';
import { api } from '@/api';
import Calendar from '@/components/icons/calendar.vue';
import Search from '@/components/buttons/search.vue';
import Clear from '@/components/buttons/clear.vue';
import Create from '@/components/buttons/create.vue'
import AddRepayment from '@/components/popup/addrepayment.vue';
import { Pagination } from '@/components'
import { RepaymentTable } from './components'
import { ElMessage } from 'element-plus';
import { Search as SearchIcon, Refresh, Plus } from '@element-plus/icons-vue';

const action = ref("Add Repayment")
const popup = ref(false)
const repayments = ref([])
const repayment = ref({})
const loading = ref(false)
const totalInfo = computed(() =>[
    {
        title: "Total Repayment",
        money: repayment.value.total_amount_due,
        num: repayment.value.total_repayments
    },
    {
        title: "Paid on Time",
        money: repayment.value.total_amount_paid,
        num: repayment.value.paid_on_time
    },
    {
        title: "Paid Late",
        money: "-",
        num: repayment.value.paid_late
    },
    {
        title: "Overdue",
        money: repayment.value.total_amount_due - repayment.value.total_amount_paid,
        num: repayment.value.missed
    }
])
const searchedRepayment = ref("")
// const statuses = ref([
//     { value: "scheduled", label: "Scheduled" },
//     { value: "dueSoon", label: "Due Soon" },
//     { value: "paid", label: "Paid" },
//     { value: "overdue", label: "Overdue" }
// ])
const paginationInfo = ref({
    total: 10,
})
const popupAction = ref("")
const selectedStatus = ref("")
const dateRange = ref("")
const itemClass = (index) => {
    switch (index) {
        case 0: return 'item1'
        case 1: return 'item2'
        case 2: return 'item3'
        case 3: return 'item4'
        default: return ''
    }
}
const selected = ref({
    search: "",
    due_after: "",
    due_before: "",
    page: 1
})

onMounted(() => {
    getRepayments()
    getRepaymentCompliance()
})

const getRepayments = async () => {
    loading.value = true
    selected.value.due_after = dateRange.value[0]
    selected.value.due_before = dateRange.value[1]
    const [err, res] = await api.repayments(selected.value)
    if (!err) {
        console.log(res);
        repayments.value = res?.results || []
        paginationInfo.value.total = res?.count || 0
    } else {
        console.log(err)
    }
    loading.value = false
}

async function getRepaymentCompliance() {
    let params = {}
    const [err, res] = await api.repaymentCompliance(params)
    console.log('🚀 ~ getData3 ~ repaymentCompliance:', res)
    repayment.value = res
}

const handleChange = (currantPage) => {
    selected.value.page = currantPage
    getRepayments()
    console.log(currantPage);
}

const addRepayment = () => {
    popup.value = true
    popupAction.value = "Add Payment"
}

const handleEdit = (id) => {
    popup.value = true
    popupAction.value = `Edit Payment ${id}`
}

const close = () => {
    popup.value = false
    // Refresh the repayments list after adding a new one
    getRepayments()
}

const handleSearch = () => {
    console.log(dateRange.value)
    getRepayments()
}

const handleClear = () => {
    searchedRepayment.value = ""
    selectedStatus.value = ""
    dateRange.value = ""
    getRepayments()
}
</script>

<template>
    <div class="repayment-dashboard">
        <!-- Statistics Cards -->
        <div class="stats-section">
            <div class="stats-grid">
                <div v-for="(info, index) in totalInfo" :key="index" class="stat-card" :class="itemClass(index)">
                    <div class="stat-icon">
                        <img src="/src/assets/icons/quick_act_1.png" alt="stat" />
                    </div>
                    <div class="stat-content">
                        <h3>{{ info.title }}</h3>
                        <div class="stat-value">{{ info.money }}</div>
                        <p>{{ info.num }} repayments</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Filters and Actions -->
        <div class="controls-section">
            <div class="controls-container">
                <div class="filters-group">
                    <el-input 
                        v-model="searchedRepayment" 
                        placeholder="Search repayments..." 
                        class="search-input"
                        clearable
                    >
                        <template #prefix>
                            <el-icon><SearchIcon /></el-icon>
                        </template>
                    </el-input>
                    
                    <div class="date-picker-wrapper">
                        <el-date-picker 
                            v-model="dateRange" 
                            type="daterange" 
                            start-placeholder="Start date" 
                            end-placeholder="End date"
                            format="DD MMM YYYY" 
                            value-format="YYYY-MM-DD" 
                            :prefix-icon="Calendar" 
                            clearable 
                            class="date-picker"
                        />
                    </div>
                    
                    <div class="filter-actions">
                        <el-button type="primary" @click="handleSearch" :icon="SearchIcon">
                            Search
                        </el-button>
                        <el-button @click="handleClear" :icon="Refresh">
                            Clear
                        </el-button>
                    </div>
                </div>
                
                <div class="action-group">
                    <el-button type="success" @click="addRepayment" :icon="Plus">
                        {{ action }}
                    </el-button>
                </div>
            </div>
        </div>

        <!-- Data Table -->
        <div class="table-section">
            <div class="table-container">
                <RepaymentTable :repayments="repayments" @refresh="getRepayments" />
                <div class="pagination-wrapper">
                    <Pagination :="paginationInfo" @change="handleChange" />
                </div>
            </div>
        </div>

        <!-- Popup -->
        <transition name="slide-right-popup">
            <AddRepayment v-if="popup" :action="popupAction" @close="close" />
        </transition>
    </div>
</template>

<style lang="scss" scoped>
.repayment-dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px;
  background: #f8f9fa;
  min-height: 100vh;
}

// Statistics Section
.stats-section {
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
  }

  .stat-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid #e9ecef;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 16px;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    }

    .stat-icon {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;

      img {
        width: 24px;
        height: 24px;
        filter: brightness(0) invert(1);
      }
    }

    .stat-content {
      flex: 1;

      h3 {
        color: #495057;
        font-size: 14px;
        font-weight: 600;
        margin: 0 0 8px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .stat-value {
        font-size: 28px;
        font-weight: 700;
        margin: 0 0 8px 0;
        line-height: 1.2;
      }

      p {
        color: #6c757d;
        font-size: 13px;
        margin: 0;
        line-height: 1.4;
      }
    }

    // Color variants
    &.item1 {
      border-left: 4px solid #384144;
      .stat-icon { background: #384144; }
      .stat-value { color: #384144; }
    }

    &.item2 {
      border-left: 4px solid #28a745;
      .stat-icon { background: #28a745; }
      .stat-value { color: #28a745; }
    }

    &.item3 {
      border-left: 4px solid #ffc107;
      .stat-icon { background: #ffc107; }
      .stat-value { color: #ffc107; }
    }

    &.item4 {
      border-left: 4px solid #dc3545;
      .stat-icon { background: #dc3545; }
      .stat-value { color: #dc3545; }
    }
  }
}

// Controls Section
.controls-section {
  .controls-container {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
  }

  .filters-group {
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;

    .search-input {
      width: 250px;
    }

    .date-picker-wrapper {
      .date-picker {
        width: 220px;
      }
    }

    .filter-actions {
      display: flex;
      gap: 8px;
    }
  }

  .action-group {
    flex-shrink: 0;
  }
}

// Table Section
.table-section {
  .table-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid #e9ecef;
    overflow: hidden;

    .pagination-wrapper {
      padding: 20px;
      display: flex;
      justify-content: center;
      border-top: 1px solid #e9ecef;
      background: #f8f9fa;
    }
  }
}

// Responsive Design
@media (max-width: 768px) {
  .repayment-dashboard {
    padding: 16px;
    gap: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .controls-container {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .filters-group {
    flex-direction: column;
    align-items: stretch;

    .search-input {
      width: 100%;
    }

    .date-picker-wrapper .date-picker {
      width: 100%;
    }

    .filter-actions {
      justify-content: center;
    }
  }
}

// Transition animations
.slide-right-popup-enter-active,
.slide-right-popup-leave-active {
  transition: all 0.3s ease;
}

.slide-right-popup-enter-from,
.slide-right-popup-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>