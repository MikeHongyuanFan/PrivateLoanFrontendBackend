<template>
    <div class="application">
        <div class="overview">
            <div class="title">
                <div class="title_info">
                    <h1>{{ application.reference_number }}</h1>
                    <h2>Created at: {{ application.created_at?.split('T')[0] }}</h2>
                    <p style="color: #2984DE">Application ID: {{ applicationId }}</p>
                </div>
                <div class="buttons">
                    <button class="calculator" @click="showCalculator">
                        <img src="/src/assets/icons/calculator.png" alt="action" />
                        Calculator
                    </button>
                    <button class="pdf" @click="generatePdf">
                        <img src="/src/assets/icons/pdf.png" alt="action" />
                        Generate PDF
                    </button>
                    <button class="note" @click="showNote">
                        <img src="/src/assets/icons/note.png" alt="action" />
                        Note
                    </button>
                    <button class="list" @click="showFee">
                        <img src="/src/assets/icons/list.png" alt="action" />
                        Fee List
                    </button>
                </div>
            </div>
            <div class="stages">
                <div class="title">
                    <h3>Stages</h3>
                    <div class="buttons">
                        <el-select v-model="bdm" style="width: 160px;" placeholder="Assign to BD">
                            <el-option v-for="item in bdms" :key="item.id" :label="item.first_name"
                                :value="item.id" />
                        </el-select>
                        <button class="move" @click="assignBd">Assign</button>
                        <button class="move" @click="prevStage" :disabled="!hasPrev">Move to Previous Stage</button>
                        <button class="move" @click="nextStage" :disabled="!hasNext">Move to Next Stage</button>
                    </div>
                </div>
                <el-scrollbar>
                    <div class="stage_line">
                        <div v-for="(s,index) in stages" :key="index" class="stage">
                            <div class="stage_info">
                                <el-icon v-if="s.status === 'complete'" :size="16" color="#1F63A9"><SuccessFilled /></el-icon>
                                <img src="@/assets/icons/application_processing.png" alt="process" v-if="s.status === 'processing'" />
                                <p :class="s.status === 'complete' ? 'active' : 'inactive'">{{ s.name }}</p>
                            </div>
                            <div class="bottom_line" :class="s.status === 'incomplete' ? 'active_line' : ''"></div>
                        </div>
                    </div>
                </el-scrollbar>
            </div>
        </div>
        <div class="tabs">
            <div class="tabs_header">
                <h3>Application Details</h3>
            </div>
            <el-scrollbar>
                <div class="tabs_line">
                    <div v-for="(i, index) in infos" 
                        :key="index" 
                        class="tab_item"
                        :class="{ active_tab_item: index === activeInfo }"
                        @click="selectInfo(index)"
                    >
                        <div class="tab_info">
                            <p :class="index === activeInfo ? 'active' : 'inactive'">{{ i.name }}</p>
                            <span v-if="i.count > 0" class="tab_count">({{ i.count }})</span>
                        </div>
                        <div class="bottom_line" :class="index !== activeInfo ? 'active_line' : ''"></div>
                    </div>
                </div>
            </el-scrollbar>
        </div>
        
        <!-- Enhanced data display sections with cascade information -->
        <div v-if="cascadeMetadata.retrieval_method" class="cascade_info">
            <div class="cascade_summary">
                <h4>📊 Data Summary (Retrieved via {{ cascadeMetadata.retrieval_method }})</h4>
                <div class="summary_grid">
                    <div class="summary_item">
                        <span class="label">Borrowers:</span>
                        <span class="value">{{ totalBorrowers }}</span>
                    </div>
                    <div class="summary_item">
                        <span class="label">Guarantors:</span>
                        <span class="value">{{ totalGuarantors }}</span>
                    </div>
                    <div class="summary_item">
                        <span class="label">Security Properties:</span>
                        <span class="value">{{ totalSecurityProperties }}</span>
                    </div>
                    <div class="summary_item">
                        <span class="label">Loan Requirements:</span>
                        <span class="value">{{ totalLoanRequirements }}</span>
                    </div>
                    <div class="summary_item">
                        <span class="label">Documents:</span>
                        <span class="value">{{ totalDocuments }}</span>
                    </div>
                    <div class="summary_item">
                        <span class="label">Notes:</span>
                        <span class="value">{{ totalNotes }}</span>
                    </div>
                    <div class="summary_item">
                        <span class="label">Total Loan Amount:</span>
                        <span class="value">${{ totalLoanAmount.toLocaleString() }}</span>
                    </div>
                    <div class="summary_item">
                        <span class="label">Total Security Value:</span>
                        <span class="value">${{ totalSecurityValue.toLocaleString() }}</span>
                    </div>
                </div>
                <small class="cascade_timestamp">Last retrieved: {{ new Date(cascadeMetadata.retrieved_at).toLocaleString() }}</small>
            </div>
        </div>
        
        <!-- Financial Summary -->
        <div v-if="financialSummary.total_fees !== undefined" class="financial_summary">
            <h4>💰 Financial Overview</h4>
            <div class="financial_grid">
                <div class="financial_item">
                    <span class="label">Total Fees:</span>
                    <span class="value">${{ financialSummary.total_fees?.toLocaleString() || 0 }}</span>
                </div>
                <div class="financial_item">
                    <span class="label">Total Repayments:</span>
                    <span class="value">${{ financialSummary.total_repayments?.toLocaleString() || 0 }}</span>
                </div>
                <div class="financial_item">
                    <span class="label">Borrower Assets:</span>
                    <span class="value">${{ financialSummary.total_borrower_assets?.toLocaleString() || 0 }}</span>
                </div>
                <div class="financial_item">
                    <span class="label">Borrower Liabilities:</span>
                    <span class="value">${{ financialSummary.total_borrower_liabilities?.toLocaleString() || 0 }}</span>
                </div>
                <div class="financial_item">
                    <span class="label">Guarantor Assets:</span>
                    <span class="value">${{ financialSummary.total_guarantor_assets?.toLocaleString() || 0 }}</span>
                </div>
                <div class="financial_item">
                    <span class="label">Guarantor Liabilities:</span>
                    <span class="value">${{ financialSummary.total_guarantor_liabilities?.toLocaleString() || 0 }}</span>
                </div>
            </div>
        </div>
        
        <!-- Enhanced component rendering with additional data access -->
        <Company v-if="activeInfo === 0" :detail="application" :summary="borrowerSummary"></Company>
        <CompanyAsset v-if="activeInfo === 1" 
            :detail="application" 
            :summary="borrowerSummary"></CompanyAsset>
        <Enquiries v-if="activeInfo === 2" :detail="application"></Enquiries>
        <Individual v-if="activeInfo === 3" :detail="application" :summary="guarantorSummary"></Individual>
        <GuarantorAsset v-if="activeInfo === 4" :detail="application" :summary="guarantorSummary"></GuarantorAsset>
        <Security v-if="activeInfo === 5" :detail="application" :total_value="totalSecurityValue"></Security>
        <LoanDetail v-if="activeInfo === 6" :detail="application" :total_amount="totalLoanAmount"></LoanDetail>
        <LoanRequirement v-if="activeInfo === 7" :detail="application" :total_amount="totalLoanAmount"></LoanRequirement>
        <Exit v-if="activeInfo === 8" :detail="application"></Exit>
        <transition name="slide-right-popup">
            <Calculator
                v-if="calculator"
                @close="closeCalculator"
                @minimize="minimize"
            ></Calculator>
        </transition>
        <transition name="slide-right-popup">
            <Note
                v-if="note"
                :id="applicationId"
                @close="closeNote"
                @minimize="minimize"
            ></Note>
        </transition>
        <transition name="slide-right-popup">
            <Fee
                v-if="fee"
                :id="applicationId"
                :applicationId="applicationId"
                @close="closeFee"
                @minimize="minimize"
            ></Fee>
        </transition>
    </div>
</template>

<script setup>
    import { ref, computed, onActivated, onMounted } from 'vue';
    import { useRoute } from 'vue-router';
    import { api } from '@/api';
    import { ElMessage } from 'element-plus';
    import Company from '@/components/application/company.vue';
    import CompanyAsset from '@/components/application/companyasset.vue';
    import Enquiries from '@/components/application/enquiries.vue';
    import Individual from '@/components/application/individual.vue';
    import GuarantorAsset from '@/components/application/guarantorasset.vue';
    import Security from '@/components/application/security.vue';
    import LoanDetail from '@/components/application/loandetail.vue';
    import LoanRequirement from '@/components/application/loanrequirement.vue';
    import Exit from '@/components/application/exit.vue';
    import Calculator from '@/components/popup/calculator.vue';
    import Note from '@/components/popup/note.vue';
    import Fee from '@/components/popup/fee.vue';
    import { SuccessFilled } from '@element-plus/icons-vue';

    const route = useRoute()

    const application = ref({})
    const applicationId = route.params.applicationId
    // Enhanced data access with computed properties for cascade data
    const cascadeMetadata = ref({})
    const financialSummary = ref({})
    const borrowerSummary = ref([])
    const guarantorSummary = ref([])
    
    const stages = ref([
        {name: "Inquiry", value: "inquiry", status: "complete"},
        {name: "Send to Lender", value: "sent_to_lender", status: "complete"},
        {name: "Funding Table lssued", value: "funding_table_issued", status: "complete"},
        {name: "ILOO lssued", value: "iloo_issued", status: "complete"},
        {name: "ILOO Signed", value: "iloo_signed", status: "processing"},
        {name: "Commitment Fee Paid", value: "commitment_fee_paid", status: "incomplete"},
        {name: "App Submitted", value: "app_submitted", status: "incomplete"},
        {name: "Valuation Ordered", value: "valuation_ordered", status: "incomplete"},
        {name: "Valuation Received", value: "valuation_received", status: "incomplete"},
        {name: "More Info Required", value: "more_info_required", status: "incomplete"},
        {name: "Formal Approval", value: "formal_approval", status: "incomplete"},
        {name: "Loan Docs instructed", value: "loan_docs_instructed", status: "incomplete"},
        {name: "Loan Docs lssued", value: "loan_docs_issued", status: "incomplete"},
        {name: "Loan Docs Signed", value: "loan_docs_signed", status: "incomplete"},
        {name: "Settlement Conditions", value: "settlement_conditions", status: "incomplete"},
        {name: "Settled", value: "settled", status: "incomplete"},
        {name: "Closed", value: "closed", status: "incomplete"},
        {name: "Declined", value: "declined", status: "incomplete"},
        {name: "Withdrawn", value: "withdrawn", status: "incomplete"},
    ])
    const infos = ref([
        {name: "Company Borrower Details", count: 0},
        {name: "Company Assets & Liabilities", count: 0},
        {name: "General Solvency Enquires", count: 0},
        {name: "Guarantor Details", count: 0},
        {name: "Guarantor Assets & Liability", count: 0},
        {name: "Proposed Security Details", count: 0},
        {name: "Loan Details & Purpose", count: 0},
        {name: "Loan Requirements", count: 0},
        {name: "Proposed Exit Strategy", count: 0}
    ])
    const activeInfo = ref(0)
    const calculator = ref(false)
    const note = ref(false)
    const fee = ref(false)
    const bdm = ref("")
    const bdms = ref([])

    const currentIndex = computed(() =>
        stages.value.findIndex(s => s.status === 'processing')
    )
    const hasPrev = computed(() => currentIndex.value > 0)
    const hasNext = computed(() => currentIndex.value < stages.value.length - 1)

    // Computed properties for enhanced data access
    const totalBorrowers = computed(() => 
        (application.value.borrowers?.length || 0) + (application.value.company_borrowers?.length || 0)
    )
    const totalIndividualBorrowers = computed(() => application.value.borrowers?.length || 0)
    const totalCompanyBorrowers = computed(() => application.value.company_borrowers?.length || 0)
    const totalGuarantors = computed(() => application.value.guarantors?.length || 0)
    const totalSecurityProperties = computed(() => application.value.security_properties?.length || 0)
    const totalLoanRequirements = computed(() => application.value.loan_requirements?.length || 0)
    const totalDocuments = computed(() => application.value.documents?.length || 0)
    const totalNotes = computed(() => application.value.notes?.length || 0)
    const totalFees = computed(() => application.value.fees?.length || 0)
    const totalRepayments = computed(() => application.value.repayments?.length || 0)

    // Financial totals
    const totalLoanAmount = computed(() => {
        return application.value.loan_requirements?.reduce((sum, req) => 
            sum + (parseFloat(req.amount) || 0), 0) || 0
    })
    
    const totalSecurityValue = computed(() => {
        return application.value.security_properties?.reduce((sum, prop) => 
            sum + (parseFloat(prop.estimated_value) || 0), 0) || 0
    })

    onMounted(() => {
        getApplicationWithCascade()
        getBd()
    })

    const updateInfoCounts = () => {
        // Update the info tabs with actual counts from the data
        infos.value[0].count = totalBorrowers.value // Company Borrower Details (both individual and company)
        
        // Calculate total assets and liabilities from both individual and company borrowers
        const individualAssets = application.value.borrowers?.reduce((sum, b) => 
            sum + (b.assets?.length || 0) + (b.liabilities?.length || 0), 0) || 0
        const companyAssets = application.value.company_borrowers?.reduce((sum, c) => 
            sum + (c.assets?.length || 0) + (c.liabilities?.length || 0), 0) || 0
        
        infos.value[1].count = individualAssets + companyAssets // Company Assets & Liabilities
        infos.value[2].count = 1 // General Solvency Enquires (always 1 set)
        infos.value[3].count = totalGuarantors.value // Guarantor Details
        infos.value[4].count = application.value.guarantors?.reduce((sum, g) => 
            sum + (g.assets?.length || 0) + (g.liabilities?.length || 0), 0) || 0 // Guarantor Assets & Liability
        infos.value[5].count = totalSecurityProperties.value // Proposed Security Details
        infos.value[6].count = 1 // Loan Details & Purpose (always 1 set)
        infos.value[7].count = totalLoanRequirements.value // Loan Requirements
        infos.value[8].count = 1 // Proposed Exit Strategy (always 1 set)
    }

    const updateStages = (currentStageName) => {
        const idx = stages.value.findIndex(s => s.value === currentStageName)
        if (idx === -1) {
            console.warn(`Stage "${currentStageName}" is not valid`)
            return
        }
        stages.value.forEach((s, i) => {
            if (i < idx)      s.status = 'complete'
            else if (i === idx) s.status = 'processing'
            else               s.status = 'incomplete'
        })
    }
    
    const getApplicationWithCascade = async () => {
        const [err, res] = await api.applicationWithCascade(applicationId)
        if (!err) {
            console.log("Application cascade data received:", res);
            application.value = res
            updateStages(res.stage)
            
            // Store cascade metadata if available
            if (res.cascade_info) {
                cascadeMetadata.value = res.cascade_info
            }
            
            // Store financial summary if available
            if (res.financial_summary) {
                financialSummary.value = res.financial_summary
            }
            
            // Store enhanced borrower and guarantor summaries
            // Combine individual and company borrowers for summary
            const individualBorrowers = res.borrowers?.map(borrower => ({
                ...borrower,
                total_assets: borrower.total_assets || 0,
                total_liabilities: borrower.total_liabilities || 0,
                net_worth: borrower.net_worth || 0,
                is_company: false
            })) || []
            
            const companyBorrowers = res.company_borrowers?.map(company => ({
                ...company,
                total_assets: company.total_assets || 0,
                total_liabilities: company.total_liabilities || 0,
                net_worth: company.net_worth || 0,
                is_company: true
            })) || []
            
            borrowerSummary.value = [...individualBorrowers, ...companyBorrowers]
            
            guarantorSummary.value = res.guarantors?.map(guarantor => ({
                ...guarantor,
                total_assets: guarantor.total_assets || 0,
                total_liabilities: guarantor.total_liabilities || 0,
                net_worth: guarantor.net_worth || 0
            })) || []
            
            // Update tab counts with actual data
            updateInfoCounts()
            
        } else {
            console.error("Error fetching application with cascade:", err)
            ElMessage.error({
                message: 'Failed to load application details',
                type: 'error',
            });
            
            // Fallback to regular application call
            getApplication()
        }
    }
    
    const getApplication = async () => {
        const [err, res] = await api.application(applicationId)
        if (!err) {
            console.log("Application data received:", res);
            application.value = res
            updateStages(res.stage)
            updateInfoCounts()
        } else {
            console.error("Error fetching application:", err)
            ElMessage.error({
                message: 'Failed to load application details',
                type: 'error',
            });
        }
    }
    const generatePdf = async () => {
        const [err, blob] = await api.generatePdf(applicationId)
        if (!err) {
            const url = window.URL.createObjectURL(blob)
            const link = document.createElement('a')
            link.href = url
            link.download = `application_${applicationId}.pdf`
            document.body.appendChild(link)
            link.click()
            link.remove()
            window.URL.revokeObjectURL(url)
        } else {
            console.error(err)
            ElMessage.error({
                message: 'Failed to generate PDF',
                type: 'error',
            });
        }
    }
    const getBd = async () => {
        const [err, res] = await api.users()
        if (!err) {
            console.log(res)
            bdms.value = res.results.filter(item =>
                item.role === 'bd'
            )
        } else {
            console.error(err)
        }
    }
    const assignBd = async () => {
        const data = {
            bd_id: bdm.value
        }
        const [err, res] = await api.assignBd(applicationId, data)
        if (!err) {
            console.log(res);
        } else {
            console.error(err)
            ElMessage.error({
                message: 'Failed to assign',
                type: 'error',
            });
        }
    }
    const showCalculator = () => {
        calculator.value = true
    }
    const showNote = () => {
        note.value = true
    }
    const showFee = () => {
        fee.value = true
    }
    const closeCalculator = () => {
        calculator.value = false
    }
    const closeNote = () => {
        note.value = false
    }
    const closeFee = () => {
        fee.value = false
    }
    const nextStage = async () => {
        const i = currentIndex.value
        const data = {
            stage: stages.value[i + 1].value
        }
        const [err, res] = await api.updateStage(applicationId, data)
        if (!err) {
            console.log(res)
            getApplication()
        } else {
            console.log(err)
        }
    }
    const prevStage = async () => {
        const i = currentIndex.value
        const data = {
            stage: stages.value[i - 1].value
        }
        const [err, res] = await api.updateStage(applicationId, data)
        if (!err) {
            console.log(res)
            getApplication()
        } else {
            console.log(err)
        }
    }
    const selectInfo = (index) => {
        activeInfo.value = index
    }
</script>

<style scoped>
    .application {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .overview {
        padding: 20px;
        border-radius: 6px;
        background: #FFF;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .title {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    .title_info {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    h1 {
        color: #000;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 1.5rem;
        font-style: normal;
        font-weight: 700;
        line-height: 12px;
    }
    h2 {
        color: #939393;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 400;
        line-height: 12px;
        margin: 0;
    }
    p {
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 140%;
        margin: 0;
    }
    .buttons {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
    }
    button {
        padding: 7px 10px;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 5px;
        border-radius: 5px;
        border: 1.5px solid #E8EBEE;
    }
    button img {
        width: 20px;
        height: 20px;
    }
    .calculator {
        background: #14A105;
        color: #FFF;
    }
    .calculator:hover {
        background: #108104;
    }
    .pdf {
        background: #384144;
        color: #FFF;
    }
    .pdf:hover {
        background: #000;
    }
    .note {
        background: #2984DE;
        color: #FFF;
    }
    .note:hover {
        background: #1F63A9;
    }
    .list {
        background: #F5F7FB;
        color: #384144;
    }
    .list:hover {
        background: #C4C6C9;
    }
    .stages {
        padding: 20px;
        padding-bottom: 0;
        display: flex;
        flex-direction: column;
        gap: 20px;
        border-radius: 8px;
        border: 1.5px solid #E8EBEE;
    }
    h3 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 1.1rem;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
        margin: 0;
    }
    .move {
        background: #FFF;
        color: #2984DE;
    }
    .move:hover {
        background: #F5F7FB;
    }
    .stage_line {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: end;
        gap: 5px;
        margin-bottom: 20px;
    }
    .stage {
        width: auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
        align-items: center;
    }
    .stage_info {
        width: auto;
        padding: 0 5px;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 5px;
    }
    .stage img {
        width: 16px;
        height: 16px;
    }
    .active {
        color: #2984DE
    }
    .inactive {
        color: #384144;
        font-weight: 400;
    }
    .bottom_line {
        width: 100%;
        height: 3px;
        border-radius: 7px;
        background: #2984DE;
    }
    .active_line {
        background: #E8EBEE;
    }
    .tabs {
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 20px;
        border-radius: 8px;
        border: 1.5px solid #E8EBEE;
        background: #FFF;
    }
    .tabs_header h3 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 1.1rem;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
        margin: 0;
    }
    .tabs_line {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: end;
        gap: 20px;
        margin-bottom: 20px;
        overflow-x: auto;
        padding-bottom: 0;
    }
    .tab_item {
        width: auto;
        min-width: 120px;
        padding: 0 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        align-items: center;
        cursor: pointer;
        flex-shrink: 0;
    }
    .tab_info {
        width: auto;
        padding: 0 5px;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 5px;
        flex-wrap: wrap;
        justify-content: center;
    }
    .tab_info p {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 140%;
        margin: 0;
        text-align: center;
        white-space: nowrap;
    }
    .tab_count {
        font-size: 0.6rem;
        color: #666;
        font-weight: 500;
        margin-left: 3px;
    }
    .active {
        color: #2984DE
    }
    .inactive {
        color: #384144;
        font-weight: 400;
    }
    .bottom_line {
        width: 100%;
        height: 3px;
        border-radius: 7px;
        background: #2984DE;
    }
    .active_line {
        background: #E8EBEE;
    }
    
    /* New cascade info styles */
    .cascade_info {
        background: #F8F9FA;
        border: 1px solid #E8EBEE;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .cascade_summary h4 {
        color: #384144;
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 12px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .summary_grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-bottom: 10px;
    }
    .summary_item {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        padding: 8px 12px;
        background: #FFF;
        border-radius: 4px;
        border: 1px solid #E8EBEE;
    }
    .summary_item .label {
        font-size: 0.7rem;
        color: #666;
        font-weight: 500;
        margin-bottom: 2px;
    }
    .summary_item .value {
        font-size: 0.85rem;
        color: #384144;
        font-weight: 600;
    }
    .cascade_timestamp {
        color: #666;
        font-size: 0.65rem;
        font-style: italic;
        display: block;
        text-align: right;
    }
    
    /* Financial summary styles */
    .financial_summary {
        background: #FFF;
        border: 1px solid #E8EBEE;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .financial_summary h4 {
        color: #384144;
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 12px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .financial_grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
    }
    .financial_item {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        padding: 10px 14px;
        background: #F8F9FA;
        border-radius: 4px;
        border: 1px solid #E8EBEE;
    }
    .financial_item .label {
        font-size: 0.7rem;
        color: #666;
        font-weight: 500;
        margin-bottom: 3px;
    }
    .financial_item .value {
        font-size: 0.9rem;
        color: #2984DE;
        font-weight: 700;
    }
    
    /* Responsive adjustments */
    @media (max-width: 1200px) {
        .summary_grid {
            grid-template-columns: repeat(3, 1fr);
        }
        .financial_grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .tabs_line {
            gap: 15px;
        }
        .tab_item {
            min-width: 100px;
        }
    }
    @media (max-width: 768px) {
        .summary_grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .financial_grid {
            grid-template-columns: 1fr;
        }
        .tabs_line {
            gap: 10px;
        }
        .tab_item {
            min-width: 80px;
        }
        .tab_info p {
            font-size: 0.7rem;
        }
    }
    .slide-right-popup-enter-active, .slide-right-popup-leave-active {
        transition: all 0.3s ease;
    }
    .slide-right-popup-enter-from, .slide-right-popup-leave-to {
        opacity: 0;
        transform: translateX(100%);
    }
    .slide-right-popup-enter-to, .slide-right-popup-leave-from {
        opacity: 1;
        transform: translateX(0);
    }
</style>