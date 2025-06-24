<template>
    <div class="application">
        <div class="overview">
            <div class="title">
                <div class="title_info">
                    <h1>{{ application.reference_number }}</h1>
                    <h2>Created at: {{ application.created_at?.split('T')[0] }}</h2>
                    <p style="color: #2984DE">Application ID: {{ validApplicationId }}</p>
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
            
            <!-- Broker, BDM & Branch Assignment Section -->
            <div class="assignment-section">
                <div class="assignment-header">
                    <h3>📋 Assignment Information</h3>
                </div>
                <div class="assignment-grid">
                    <div class="assignment-item">
                        <span class="assignment-label">Broker:</span>
                        <span class="assignment-value">
                            {{ application.broker?.name || 'Not Assigned' }}
                            <span v-if="application.broker?.company" class="company">({{ application.broker.company }})</span>
                        </span>
                    </div>
                    <div class="assignment-item">
                        <span class="assignment-label">BDM:</span>
                        <span class="assignment-value">{{ application.bd?.name || 'Not Assigned' }}</span>
                    </div>
                    <div class="assignment-item">
                        <span class="assignment-label">Branch:</span>
                        <span class="assignment-value">{{ application.branch?.name || 'Not Assigned' }}</span>
                    </div>
                    <div class="assignment-item" v-if="application.broker?.email">
                        <span class="assignment-label">Broker Email:</span>
                        <span class="assignment-value">
                            <a :href="`mailto:${application.broker.email}`" class="email-link">
                                {{ application.broker.email }}
                            </a>
                        </span>
                    </div>
                    <div class="assignment-item" v-if="application.broker?.phone">
                        <span class="assignment-label">Broker Phone:</span>
                        <span class="assignment-value">
                            <a :href="`tel:${application.broker.phone}`" class="phone-link">
                                {{ application.broker.phone }}
                            </a>
                        </span>
                    </div>
                    <div class="assignment-item" v-if="application.branch?.address">
                        <span class="assignment-label">Branch Address:</span>
                        <span class="assignment-value">{{ application.branch.address }}</span>
                    </div>
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
                
                <!-- Stage History Section -->
                <div class="stage-history" v-if="stageHistory.length > 0">
                    <h4>Stage History</h4>
                    <el-timeline>
                        <el-timeline-item
                            v-for="(change, index) in stageHistory"
                            :key="index"
                            :timestamp="change.timestamp"
                            :type="getTimelineItemType(change)"
                        >
                            <div class="history-item">
                                <div class="stage-change">
                                    <span class="from-stage">{{ change.from }}</span>
                                    <el-icon><ArrowRight /></el-icon>
                                    <span class="to-stage">{{ change.to }}</span>
                                </div>
                                <div class="change-details">
                                    <span class="user">By: {{ change.user }}</span>
                                    <p v-if="change.notes" class="notes">{{ change.notes }}</p>
                                </div>
                            </div>
                        </el-timeline-item>
                    </el-timeline>
                </div>
            </div>
            
            <!-- Add Active Loan Details section when stage is settled -->
            <div v-if="application.stage === 'settled'" class="active-loan-section">
                <ActiveLoanDetails :detail="application" />
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
        
        <!-- Enhanced component rendering with additional data access -->
        <Company v-if="activeInfo === 0" :detail="application" :summary="borrowerSummary"></Company>
        <CompanyAsset v-if="activeInfo === 1" 
            :detail="application" 
            :summary="combinedBorrowerGuarantorSummary"></CompanyAsset>
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
                :id="validApplicationId"
            ></Calculator>
        </transition>
        <transition name="slide-right-popup">
            <Note
                v-if="note"
                :id="validApplicationId"
                :applicationId="validApplicationId"
                @close="closeNote"
                @minimize="minimize"
            ></Note>
        </transition>
        <transition name="slide-right-popup">
            <Fee
                v-if="fee"
                :id="validApplicationId"
                :applicationId="validApplicationId"
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
    import ActiveLoanDetails from '@/components/application/activeloandetails.vue';
    import { SuccessFilled, ArrowRight } from '@element-plus/icons-vue';

    const route = useRoute()

    const application = ref({})
    const applicationId = route.params.applicationId

    // Add immediate debugging when the component is created
    console.log("=== COMPONENT CREATION DEBUG ===");
    console.log("Component created at:", new Date().toISOString());
    console.log("Route object at creation:", route);
    console.log("Route params at creation:", route.params);
    console.log("Route path at creation:", route.path);
    console.log("Route fullPath at creation:", route.fullPath);
    console.log("ApplicationId from route at creation:", applicationId);
    console.log("ApplicationId type at creation:", typeof applicationId);
    console.log("ApplicationId constructor at creation:", applicationId?.constructor?.name);

    // Create a computed property that always extracts the ID from the route path
    const validApplicationId = computed(() => {
        console.log("=== COMPUTED APPLICATION ID DEBUG ===");
        console.log("Computed property called at:", new Date().toISOString());
        console.log("Route path:", route.path);
        console.log("Route params:", route.params);
        console.log("Route params keys:", Object.keys(route.params));
        console.log("Route fullPath:", route.fullPath);
        console.log("Route query:", route.query);
        
        // ALWAYS extract from path first, ignore route params if they're invalid
        const pathParts = route.path.split('/');
        const idFromPath = pathParts[pathParts.length - 1];
        console.log("Path parts:", pathParts);
        console.log("ID from path:", idFromPath);
        
        if (idFromPath && !isNaN(idFromPath)) {
            console.log("✅ Using ID from path:", idFromPath);
            return idFromPath;
        }
        
        // Fallback to route params only if path extraction fails
        let id = route.params.applicationId;
        console.log("ID from route params:", id, "Type:", typeof id);
        console.log("ID constructor:", id?.constructor?.name);
        
        // If route params is invalid, return null
        if (!id || id === '[object PointerEvent]' || typeof id === 'object') {
            console.log("❌ Route params invalid");
            console.log("Invalid ID details:", {
                value: id,
                type: typeof id,
                constructor: id?.constructor?.name,
                isObject: typeof id === 'object',
                isPointerEvent: id?.constructor?.name === 'PointerEvent'
            });
            console.error("❌ Could not extract valid ID from path or route params");
            return null;
        } else {
            console.log("✅ Route params valid, using:", id);
        }
        
        console.log("✅ Final valid application ID:", id);
        return id;
    });

    // Add comprehensive debugging and validation for applicationId
    console.log("=== ROUTE DEBUG ===");
    console.log("Route object:", route);
    console.log("Route params:", route.params);
    console.log("Route path:", route.path);
    console.log("Route fullPath:", route.fullPath);
    console.log("Route query:", route.query);
    console.log("ApplicationId from route:", applicationId, "Type:", typeof applicationId);
    console.log("ApplicationId constructor:", applicationId?.constructor?.name);

    // Check if applicationId is an event object
    if (applicationId && typeof applicationId === 'object') {
        console.error("❌ CRITICAL: applicationId is an object!");
        console.error("Object keys:", Object.keys(applicationId));
        console.error("Object constructor:", applicationId.constructor.name);
        if (applicationId.constructor.name === 'PointerEvent') {
            console.error("❌ This is a PointerEvent object!");
        }
    }

    // Validate applicationId
    if (!applicationId || applicationId === '[object PointerEvent]' || typeof applicationId === 'object') {
        console.error("❌ Invalid applicationId detected:", applicationId);
        // Try to get it from the current route path
        const pathParts = route.path.split('/');
        const idFromPath = pathParts[pathParts.length - 1];
        console.log("Trying to get ID from path:", idFromPath);
        if (idFromPath && !isNaN(idFromPath)) {
            console.log("✅ Using ID from path:", idFromPath);
            // We can't reassign const, so we'll handle this in the functions
        }
    }

    // Enhanced data access with computed properties for cascade data
    const cascadeMetadata = ref({})
    const financialSummary = ref({})
    const borrowerSummary = ref([])
    const guarantorSummary = ref([])
    
    const stages = ref([
        {name: "Received", value: "received", status: "complete"},
        {name: "Sent to Lender/Investor", value: "sent_to_lender", status: "complete"},
        {name: "Funding Table Issued", value: "funding_table_issued", status: "complete"},
        {name: "Indicative Letter Issued", value: "indicative_letter_issued", status: "complete"},
        {name: "Indicative Letter Signed", value: "indicative_letter_signed", status: "processing"},
        {name: "Commitment Fee Received", value: "commitment_fee_received", status: "incomplete"},
        {name: "Application Submitted", value: "application_submitted", status: "incomplete"},
        {name: "Valuation Ordered", value: "valuation_ordered", status: "incomplete"},
        {name: "Valuation Received", value: "valuation_received", status: "incomplete"},
        {name: "More Information Required", value: "more_info_required", status: "incomplete"},
        {name: "Formal Approval", value: "formal_approval", status: "incomplete"},
        {name: "Loan Documents Instructed", value: "loan_docs_instructed", status: "incomplete"},
        {name: "Loan Documents Issued", value: "loan_docs_issued", status: "incomplete"},
        {name: "Loan Documents Signed", value: "loan_docs_signed", status: "incomplete"},
        {name: "Settlement Conditions", value: "settlement_conditions", status: "incomplete"},
        {name: "Settled", value: "settled", status: "incomplete"},
        {name: "Closed", value: "closed", status: "incomplete"},
        {name: "Discharged", value: "discharged", status: "incomplete"}
    ])
    const infos = ref([
        {name: "Company/Individual Borrower Detail", count: 0},
        {name: "Assets & Liabilities", count: 0},
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

    // Add stage history display
    const stageHistory = computed(() => {
        if (!application.value?.stage_history) return []
        return application.value.stage_history.map(change => ({
            from: stages.value.find(s => s.value === change.from_stage)?.name || change.from_stage,
            to: stages.value.find(s => s.value === change.to_stage)?.name || change.to_stage,
            timestamp: new Date(change.timestamp).toLocaleString(),
            user: change.user,
            notes: change.notes
        }))
    })

    // Combined borrower and guarantor data for assets/liabilities display
    const combinedBorrowerGuarantorSummary = computed(() => {
        const borrowers = borrowerSummary.value || []
        const guarantors = guarantorSummary.value || []
        
        // Filter to only include entities that have assets or liabilities
        const borrowersWithAssets = borrowers.filter(borrower => 
            (borrower.assets && borrower.assets.length > 0) || 
            (borrower.liabilities && borrower.liabilities.length > 0)
        )
        
        const guarantorsWithAssets = guarantors.filter(guarantor => 
            (guarantor.assets && guarantor.assets.length > 0) || 
            (guarantor.liabilities && guarantor.liabilities.length > 0)
        )
        
        // Combine all borrowers and guarantors for unified display
        return [...borrowersWithAssets, ...guarantorsWithAssets]
    })

    onMounted(() => {
        console.log("=== ON MOUNTED DEBUG ===");
        console.log("Route at mounted:", route);
        console.log("Route params at mounted:", route.params);
        console.log("Route path at mounted:", route.path);
        console.log("validApplicationId.value at mounted:", validApplicationId.value);
        getApplicationWithCascade()
        getBd()
    })

    onActivated(() => {
        // Refresh data when the route becomes active (e.g., navigating from list view after edit)
        console.log("=== ON ACTIVATED DEBUG ===");
        console.log("Route at activated:", route);
        console.log("Route params at activated:", route.params);
        console.log("Route path at activated:", route.path);
        console.log("validApplicationId.value at activated:", validApplicationId.value);
        console.log("Application detail view activated, refreshing data...");
        getApplicationWithCascade()
    })

    const updateInfoCounts = () => {
        // Update the info tabs with actual counts from the data
        infos.value[0].count = totalBorrowers.value // Company Borrower Details (both individual and company)
        
        // Calculate total assets and liabilities from both individual and company borrowers
        // Only count entities that actually have assets or liabilities
        const individualAssets = application.value.borrowers?.reduce((sum, b) => {
            const hasAssets = (b.assets && b.assets.length > 0) || (b.liabilities && b.liabilities.length > 0)
            return hasAssets ? sum + (b.assets?.length || 0) + (b.liabilities?.length || 0) : sum
        }, 0) || 0
        
        const companyAssets = application.value.company_borrowers?.reduce((sum, c) => {
            const hasAssets = (c.assets && c.assets.length > 0) || (c.liabilities && c.liabilities.length > 0)
            return hasAssets ? sum + (c.assets?.length || 0) + (c.liabilities?.length || 0) : sum
        }, 0) || 0
        
        const guarantorAssets = application.value.guarantors?.reduce((sum, g) => {
            const hasAssets = (g.assets && g.assets.length > 0) || (g.liabilities && g.liabilities.length > 0)
            return hasAssets ? sum + (g.assets?.length || 0) + (g.liabilities?.length || 0) : sum
        }, 0) || 0
        
        infos.value[1].count = individualAssets + companyAssets + guarantorAssets // Assets & Liabilities
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
        // Handle invalid applicationId
        let validId = validApplicationId.value;
        console.log("=== GET APPLICATION WITH CASCADE DEBUG ===");
        console.log("validApplicationId.value:", validId);
        console.log("validApplicationId.value type:", typeof validId);
        console.log("validApplicationId.value constructor:", validId?.constructor?.name);
        
        if (!validId || validId === '[object PointerEvent]' || typeof validId === 'object') {
            console.log("Invalid applicationId, extracting from route path");
            const pathParts = route.path.split('/');
            const idFromPath = pathParts[pathParts.length - 1];
            console.log("Trying to get ID from path:", idFromPath);
            if (idFromPath && !isNaN(idFromPath)) {
                validId = idFromPath;
                console.log("Using ID from path:", validId);
            } else {
                console.error("Could not extract valid ID from route");
                ElMessage.error({
                    message: 'Invalid application ID',
                    type: 'error',
                });
                return;
            }
        }
        
        console.log("Calling applicationWithCascade with ID:", validId);
        console.log("ID type:", typeof validId);
        const [err, res] = await api.applicationWithCascade(validId)
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
        // Handle invalid applicationId
        let validId = validApplicationId.value;
        console.log("=== GET APPLICATION DEBUG ===");
        console.log("validApplicationId.value:", validId);
        console.log("validApplicationId.value type:", typeof validId);
        console.log("validApplicationId.value constructor:", validId?.constructor?.name);
        
        if (!validId || validId === '[object PointerEvent]' || typeof validId === 'object') {
            console.log("Invalid applicationId, extracting from route path");
            const pathParts = route.path.split('/');
            const idFromPath = pathParts[pathParts.length - 1];
            console.log("Trying to get ID from path:", idFromPath);
            if (idFromPath && !isNaN(idFromPath)) {
                validId = idFromPath;
                console.log("Using ID from path:", validId);
            } else {
                console.error("Could not extract valid ID from route");
                ElMessage.error({
                    message: 'Invalid application ID',
                    type: 'error',
                });
                return;
            }
        }
        
        console.log("Calling application with ID:", validId);
        console.log("ID type:", typeof validId);
        const [err, res] = await api.application(validId)
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
        // Handle invalid applicationId
        let validId = validApplicationId.value;
        if (!validId || validId === '[object PointerEvent]' || typeof validId === 'object') {
            console.log("Invalid applicationId, extracting from route path");
            const pathParts = route.path.split('/');
            const idFromPath = pathParts[pathParts.length - 1];
            if (idFromPath && !isNaN(idFromPath)) {
                validId = idFromPath;
                console.log("Using ID from path:", validId);
            } else {
                console.error("Could not extract valid ID from route");
                ElMessage.error({
                    message: 'Invalid application ID',
                    type: 'error',
                });
                return;
            }
        }
        
        const [err, blob] = await api.generatePdf(validId)
        if (!err) {
            const url = window.URL.createObjectURL(blob)
            const link = document.createElement('a')
            link.href = url
            link.download = `application_${validId}.pdf`
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
        // Handle invalid applicationId
        let validId = validApplicationId.value;
        if (!validId || validId === '[object PointerEvent]' || typeof validId === 'object') {
            console.log("Invalid applicationId, extracting from route path");
            const pathParts = route.path.split('/');
            const idFromPath = pathParts[pathParts.length - 1];
            if (idFromPath && !isNaN(idFromPath)) {
                validId = idFromPath;
                console.log("Using ID from path:", validId);
            } else {
                console.error("Could not extract valid ID from route");
                ElMessage.error({
                    message: 'Invalid application ID',
                    type: 'error',
                });
                return;
            }
        }
        
        const data = {
            bd_id: bdm.value
        }
        const [err, res] = await api.assignBd(validId, data)
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
        const [err, res] = await api.updateStage(validApplicationId.value, data)
        if (!err) {
            console.log(res)
            ElMessage.success(`Application moved to ${stages.value[i + 1].name} stage successfully`)
            getApplication()
        } else {
            console.log(err)
            ElMessage.error('Failed to update stage')
        }
    }
    const prevStage = async () => {
        const i = currentIndex.value
        const data = {
            stage: stages.value[i - 1].value
        }
        const [err, res] = await api.updateStage(validApplicationId.value, data)
        if (!err) {
            console.log(res)
            ElMessage.success(`Application moved to ${stages.value[i - 1].name} stage successfully`)
            getApplication()
        } else {
            console.log(err)
            ElMessage.error('Failed to update stage')
        }
    }
    const selectInfo = (index) => {
        activeInfo.value = index
    }

    // Add stage history section to template
    const getTimelineItemType = (change) => {
        if (change.from === 'received' && change.to === 'sent_to_lender') return 'primary'
        if (change.from === 'sent_to_lender' && change.to === 'funding_table_issued') return 'primary'
        if (change.from === 'funding_table_issued' && change.to === 'indicative_letter_issued') return 'primary'
        if (change.from === 'indicative_letter_issued' && change.to === 'indicative_letter_signed') return 'primary'
        if (change.from === 'indicative_letter_signed' && change.to === 'commitment_fee_received') return 'primary'
        if (change.from === 'commitment_fee_received' && change.to === 'application_submitted') return 'primary'
        if (change.from === 'application_submitted' && change.to === 'valuation_ordered') return 'primary'
        if (change.from === 'valuation_ordered' && change.to === 'valuation_received') return 'primary'
        if (change.from === 'valuation_received' && change.to === 'more_info_required') return 'primary'
        if (change.from === 'more_info_required' && change.to === 'formal_approval') return 'primary'
        if (change.from === 'formal_approval' && change.to === 'loan_docs_instructed') return 'primary'
        if (change.from === 'loan_docs_instructed' && change.to === 'loan_docs_issued') return 'primary'
        if (change.from === 'loan_docs_issued' && change.to === 'loan_docs_signed') return 'primary'
        if (change.from === 'loan_docs_signed' && change.to === 'settlement_conditions') return 'primary'
        if (change.from === 'settlement_conditions' && change.to === 'settled') return 'primary'
        if (change.from === 'settled' && change.to === 'closed') return 'primary'
        if (change.from === 'closed' && change.to === 'discharged') return 'primary'
        return 'success'
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
    
    /* Assignment section styles */
    .assignment-section {
        background: #FFF;
        border: 1px solid #E8EBEE;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .assignment-header h3 {
        color: #384144;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 15px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .assignment-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
    }
    
    .assignment-item {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        padding: 12px 15px;
        background: #F8F9FA;
        border-radius: 6px;
        border: 1px solid #E8EBEE;
        transition: all 0.2s ease;
    }
    
    .assignment-item:hover {
        background: #F0F4F8;
        border-color: #2984DE;
    }
    
    .assignment-label {
        font-size: 0.75rem;
        color: #666;
        font-weight: 600;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .assignment-value {
        font-size: 0.9rem;
        color: #384144;
        font-weight: 500;
        line-height: 1.4;
    }
    
    .assignment-value .company {
        font-size: 0.8rem;
        color: #666;
        font-weight: 400;
        margin-left: 4px;
    }
    
    .email-link, .phone-link {
        color: #2984DE;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    
    .email-link:hover, .phone-link:hover {
        color: #1F63A9;
        text-decoration: underline;
    }
    
    /* Responsive adjustments for assignment section */
    @media (max-width: 1200px) {
        .assignment-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media (max-width: 768px) {
        .assignment-grid {
            grid-template-columns: 1fr;
        }
        
        .assignment-section {
            padding: 15px;
        }
        
        .assignment-header h3 {
            font-size: 1rem;
        }
        
        .assignment-item {
            padding: 10px 12px;
        }
    }

    .stage-history {
        margin-top: 20px;
        padding: 15px;
        border-top: 1px solid #E8EBEE;
    }

    .stage-history h4 {
        color: #384144;
        font-size: 1rem;
        margin-bottom: 15px;
    }

    .history-item {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .stage-change {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #2984DE;
        font-weight: 500;
    }

    .change-details {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .user {
        color: #666;
        font-size: 0.9rem;
    }

    .notes {
        color: #384144;
        font-size: 0.9rem;
        margin: 0;
        white-space: pre-wrap;
    }

    .active-loan-section {
        margin-top: 20px;
        padding: 20px;
        border-radius: 6px;
        background: #FFF;
        border: 1px solid #E8EBEE;
    }
</style>