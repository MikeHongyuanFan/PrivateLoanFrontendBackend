<script setup>
import { ref, onMounted, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/api'
import { ApplicationTable, NotificationTable, UpcomingTable } from './components'
import AddApplication from '@/components/popup/addapplication/index.vue';
import AddBorrower from '@/components/popup/addborrower.vue';

const router = useRouter()
const loadingData = ref(false)
const dashboard = ref({})
const repayment = ref({})
const fee = ref({})
const volume = ref({})
const archivedStats = ref({})
const applicationPopup = ref(false)
const borrowerPopup = ref(false)

onActivated(() => {
  getApplicationStatus()
  getApplicationVolume()
  getRepaymentCompliance()
  getFeeCompliance()
  getArchivedStats()
})

const toPage = (page) => {
  if (page === 'application') {
    router.push('/application')
  } else {
    router.push(`/dashboard/${page}`)
  }
}

async function getApplicationStatus() {
  loadingData.value = true
  let params = {}
  const [err, res] = await api.applicationStatus(params)
  console.log('🚀 ~ getData ~ applicationStatus:', res)
  loadingData.value = false
  dashboard.value = res
}

async function getApplicationVolume() {
  let params = {}
  const [err, res] = await api.applicationVolume(params)
  console.log('🚀 ~ getData2 ~ applicationVolume:', res)
  volume.value = res
}

async function getRepaymentCompliance() {
  let params = {}
  const [err, res] = await api.repaymentCompliance(params)
  console.log('🚀 ~ getData3 ~ repaymentCompliance:', res)
  repayment.value = res
}

async function getFeeCompliance() {
  let params = {}
  const [err, res] = await api.feeCompliance(params)
  console.log('🚀 ~ getData4 ~ feeCompliance:', res)
  fee.value = res
}

async function getArchivedStats() {
  const [err, res] = await api.archivedApplicationsStats()
  if (!err) {
    console.log('🚀 ~ getArchivedStats ~ archivedStats:', res)
    archivedStats.value = res
  } else {
    console.error('Error fetching archived stats:', err)
  }
}

const toAddApplication = () => {
  applicationPopup.value = true
}
const closeApplication = () => {
  applicationPopup.value = false
}
const toAddBorrower = () => {
  borrowerPopup.value = true
}
const closeBorrower = () => {
  borrowerPopup.value = false
}
const toDocument = () => {
  router.push('/document')
}
const toAddNote = () => {

}

const viewArchived = () => {
  router.push('/application/archived')
}
</script>

<template>
  <div class="dashboard" v-loading="loadingData">
    <!-- Main Statistics Cards -->
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card primary">
          <div class="stat-icon">
            <img src="/src/assets/icons/quick_act_1.png" alt="applications" />
          </div>
          <div class="stat-content">
            <h3>Total Applications</h3>
            <div class="stat-value">{{ volume.total_applications || 0 }}</div>
            <p>Applications in the system</p>
          </div>
          <button class="stat-action" @click="toPage('application')">
            View Applications
          </button>
        </div>

        <div class="stat-card success">
          <div class="stat-icon">
            <img src="/src/assets/icons/quick_act_2.png" alt="loans" />
          </div>
          <div class="stat-content">
            <h3>Active Loans</h3>
            <div class="stat-value">{{ dashboard.total_active || 0 }}</div>
            <p>Currently active loans</p>
          </div>
          <button class="stat-action" @click="toPage('application')">
            View Active Loans
          </button>
        </div>

        <div class="stat-card info">
          <div class="stat-icon">
            <img src="/src/assets/icons/quick_act_3.png" alt="value" />
          </div>
          <div class="stat-content">
            <h3>Total Loan Value</h3>
            <div class="stat-value">${{ volume.total_loan_amount || 0 }}</div>
            <p>Combined loan portfolio value</p>
          </div>
          <button class="stat-action" @click="toPage('application')">
            View Portfolio
          </button>
        </div>

        <div class="stat-card warning">
          <div class="stat-icon">
            <img src="/src/assets/icons/quick_act_1.png" alt="repayments" />
          </div>
          <div class="stat-content">
            <h3>Repayments Due</h3>
            <div class="stat-value">${{ repayment.total_amount_due || 0 }}</div>
            <p>Total repayments outstanding</p>
          </div>
          <button class="stat-action" @click="toPage('repayment')">
            View Repayments
          </button>
        </div>

        <div class="stat-card danger">
          <div class="stat-icon">
            <img src="/src/assets/icons/quick_act_2.png" alt="fees" />
          </div>
          <div class="stat-content">
            <h3>Fees Outstanding</h3>
            <div class="stat-value">${{ fee.total_amount_due || 0 }}</div>
            <p>Total fees pending payment</p>
          </div>
          <button class="stat-action" @click="toPage('fee')">
            View Fees
          </button>
        </div>
      </div>
    </div>

    <!-- Secondary Information -->
    <div class="secondary-section">
      <div class="secondary-grid">
        <div class="info-card archived">
          <div class="info-content">
            <h3>Archived Applications</h3>
            <div class="info-value">{{ archivedStats.total_archived || 0 }}</div>
            <p>Applications automatically archived when closed</p>
          </div>
          <button class="info-action" @click="viewArchived">
            View Archived
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Actions Section -->
    <div class="actions-section">
      <div class="actions-container">
        <div class="actions-header">
          <h2>Quick Actions</h2>
          <p>Common tasks and shortcuts</p>
        </div>
        <div class="actions-grid">
          <button class="action-card primary" @click="toAddApplication">
            <div class="action-icon">
              <img src="/src/assets/icons/quick_act_1.png" alt="new application" />
            </div>
            <div class="action-content">
              <h4>New Application</h4>
              <p>Create a new loan application</p>
            </div>
          </button>

          <button class="action-card secondary" @click="toAddBorrower">
            <div class="action-icon">
              <img src="/src/assets/icons/quick_act_2.png" alt="new borrower" />
            </div>
            <div class="action-content">
              <h4>New Borrower</h4>
              <p>Add a new borrower to the system</p>
            </div>
          </button>

          <button class="action-card tertiary" @click="toDocument">
            <div class="action-icon">
              <img src="/src/assets/icons/quick_act_3.png" alt="upload document" />
            </div>
            <div class="action-content">
              <h4>Upload Document</h4>
              <p>Upload and manage documents</p>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Popups -->
    <transition name="slide-right-popup">
      <AddApplication v-if="applicationPopup" 
        action="Add Application" 
        @close="closeApplication" 
        @minimize="minimize"
      ></AddApplication>
    </transition>
    <transition name="slide-right-popup">
      <AddBorrower v-if="borrowerPopup" 
        action="Add Borrower" 
        @close="closeBorrower" 
        @minimize="minimize"
      ></AddBorrower>
    </transition>
  </div>
</template>

<style lang="scss" scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px;
  background: #f8f9fa;
  min-height: 100vh;
}

// Main Statistics Section
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
    flex-direction: column;
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
      margin-bottom: 8px;

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

    .stat-action {
      background: transparent;
      border: 1px solid currentColor;
      color: inherit;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
      margin-top: auto;

      &:hover {
        background: currentColor;
        color: white;
      }
    }

    // Color variants
    &.primary {
      border-left: 4px solid #2984de;
      .stat-icon { background: #2984de; }
      .stat-value { color: #2984de; }
      .stat-action { color: #2984de; }
    }

    &.success {
      border-left: 4px solid #28a745;
      .stat-icon { background: #28a745; }
      .stat-value { color: #28a745; }
      .stat-action { color: #28a745; }
    }

    &.info {
      border-left: 4px solid #17a2b8;
      .stat-icon { background: #17a2b8; }
      .stat-value { color: #17a2b8; }
      .stat-action { color: #17a2b8; }
    }

    &.warning {
      border-left: 4px solid #ffc107;
      .stat-icon { background: #ffc107; }
      .stat-value { color: #ffc107; }
      .stat-action { color: #ffc107; }
    }

    &.danger {
      border-left: 4px solid #dc3545;
      .stat-icon { background: #dc3545; }
      .stat-value { color: #dc3545; }
      .stat-action { color: #dc3545; }
    }
  }
}

// Secondary Information Section
.secondary-section {
  .secondary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }

  .info-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;

    .info-content {
      flex: 1;

      h3 {
        color: #495057;
        font-size: 16px;
        font-weight: 600;
        margin: 0 0 8px 0;
      }

      .info-value {
        font-size: 24px;
        font-weight: 700;
        color: #6c757d;
        margin: 0 0 4px 0;
      }

      p {
        color: #6c757d;
        font-size: 13px;
        margin: 0;
        line-height: 1.4;
      }
    }

    .info-action {
      background: #6c757d;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: background 0.2s ease;

      &:hover {
        background: #5a6268;
      }
    }

    &.archived {
      border-left: 4px solid #6c757d;
    }
  }
}

// Quick Actions Section
.actions-section {
  .actions-container {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid #e9ecef;

    .actions-header {
      margin-bottom: 24px;
      text-align: center;

      h2 {
        color: #495057;
        font-size: 20px;
        font-weight: 600;
        margin: 0 0 8px 0;
      }

      p {
        color: #6c757d;
        font-size: 14px;
        margin: 0;
      }
    }

    .actions-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 16px;
    }

    .action-card {
      background: white;
      border: 1px solid #e9ecef;
      border-radius: 8px;
      padding: 20px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 16px;
      text-align: left;

      &:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .action-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;

        img {
          width: 20px;
          height: 20px;
          filter: brightness(0) invert(1);
        }
      }

      .action-content {
        flex: 1;

        h4 {
          color: #495057;
          font-size: 14px;
          font-weight: 600;
          margin: 0 0 4px 0;
        }

        p {
          color: #6c757d;
          font-size: 12px;
          margin: 0;
          line-height: 1.4;
        }
      }

      &.primary {
        border-color: #2984de;
        .action-icon { background: #2984de; }
        &:hover { border-color: #1f63a9; }
      }

      &.secondary {
        border-color: #28a745;
        .action-icon { background: #28a745; }
        &:hover { border-color: #1e7e34; }
      }

      &.tertiary {
        border-color: #17a2b8;
        .action-icon { background: #17a2b8; }
        &:hover { border-color: #117a8b; }
      }
    }
  }
}

// Responsive Design
@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
    gap: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .info-card {
    flex-direction: column;
    text-align: center;
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

