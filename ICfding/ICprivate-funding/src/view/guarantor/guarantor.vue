<template>
    <div class="guarantor">
        <div class="title">
            <h1>{{ guarantor.name || '-'}}</h1>
            <h2>{{ guarantor.date }}</h2>
            <p style="color: #2984DE">Guarantor ID: {{ guarantorId }}</p>
        </div>
        <el-tabs v-model="activeName" class="tabs" >
            <el-tab-pane name="1">
                <template #label>
                    <div class="label">Personal Information</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Title</p>
                        <p class="text">{{ formatTitle(overview.title) }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Guarantor Name</p>
                        <p class="text">{{ overview.name || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Guarantor Type</p>
                        <p class="text">{{ overview.guarantor_type || 'Individual' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Email Address</p>
                        <p class="text">{{ overview.email || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Home Phone</p>
                        <p class="text">{{ overview.home_phone || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Mobile Phone</p>
                        <p class="text">{{ overview.mobile || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Date of Birth</p>
                        <p class="text">{{ overview.birth || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Driver's License Number</p>
                        <p class="text">{{ overview.drivers_licence_no || '-' }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="2">
                <template #label>
                    <div class="label">Residential Address</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Unit Number</p>
                        <p class="text">{{ overview.address_unit || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Street Number</p>
                        <p class="text">{{ overview.address_street_no || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Street Name</p>
                        <p class="text">{{ overview.address_street_name || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Suburb</p>
                        <p class="text">{{ overview.address_suburb || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">State</p>
                        <p class="text">{{ overview.address_state || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Postcode</p>
                        <p class="text">{{ overview.address_postcode || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Full Address</p>
                        <p class="text">{{ formatFullAddress(overview) }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="3">
                <template #label>
                    <div class="label">Employment Information</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Occupation</p>
                        <p class="text">{{ overview.occupation || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Employment Type</p>
                        <p class="text">{{ formatEmploymentType(overview.status) }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Employer Name</p>
                        <p class="text">{{ overview.employer_name || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Annual Income</p>
                        <p class="text">{{ overview.income || '-' }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="4">
                <template #label>
                    <div class="label">Company Details</div>
                </template>
                <div class="tab" v-if="overview.guarantor_type === 'company'">
                    <div class="info">
                        <p style="color: #7A858E">Company Name</p>
                        <p class="text">{{ overview.company_name || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">ABN</p>
                        <p class="text">{{ overview.company_abn || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">ACN</p>
                        <p class="text">{{ overview.company_acn || '-' }}</p>
                    </div>
                </div>
                <div class="tab" v-else>
                    <div class="info">
                        <p style="color: #7A858E">No Company Details</p>
                        <p class="text">This is an individual guarantor</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="5">
                <template #label>
                    <div class="label">Legacy Information</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Legacy Phone</p>
                        <p class="text">{{ overview.phone || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Address</p>
                        <p class="text">{{ overview.address || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy City</p>
                        <p class="text">{{ overview.city || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Postal Code</p>
                        <p class="text">{{ overview.postal_code || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Years with Employer</p>
                        <p class="text">{{ overview.years_with_employer || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Legacy Credit Score</p>
                        <p class="text">{{ overview.score || '-' }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="6">
                <template #label>
                    <div class="label">Related Borrowers</div>
                </template>
                <div class="applications-section">
                    <div v-if="loadingBorrowers" class="loading">Loading related borrowers...</div>
                    <div v-else-if="!relatedBorrowers || relatedBorrowers.length === 0" class="no-data">No related borrowers found</div>
                    <div v-else>
                        <div class="applications-header">
                            <h3>Related Borrowers ({{ relatedBorrowers.length }})</h3>
                        </div>
                        <el-table 
                            :data="relatedBorrowers" 
                            style="width: 100%" 
                            class="applications-table"
                            v-loading="loadingBorrowers"
                        >
                            <el-table-column prop="id" label="ID" width="80" />
                            <el-table-column prop="name" label="Borrower Name" min-width="200" />
                            <el-table-column prop="relationship" label="Relationship" min-width="150" />
                            <el-table-column prop="email" label="Email" min-width="200" />
                            <el-table-column prop="phone" label="Phone" min-width="150" />
                            <el-table-column label="Actions" width="120">
                                <template #default="scope">
                                    <el-button 
                                        type="primary" 
                                        size="small" 
                                        @click="viewBorrower(scope.row.id)"
                                    >
                                        View
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="7">
                <template #label>
                    <div class="label">Related Applications</div>
                </template>
                <div class="applications-section">
                    <div v-if="loadingApplications" class="loading">Loading related applications...</div>
                    <div v-else-if="!relatedApplications || relatedApplications.length === 0" class="no-data">No related applications found</div>
                    <div v-else>
                        <div class="applications-header">
                            <h3>Related Applications ({{ relatedApplications.length }})</h3>
                        </div>
                        <el-table 
                            :data="relatedApplications" 
                            style="width: 100%" 
                            class="applications-table"
                            v-loading="loadingApplications"
                        >
                            <el-table-column prop="id" label="ID" width="80" />
                            <el-table-column prop="reference_number" label="Reference Number" width="150" />
                            <el-table-column prop="title" label="Application Title" min-width="250" />
                            <el-table-column prop="status" label="Status" min-width="120" />
                            <el-table-column prop="created_at" label="Created Date" min-width="150" />
                            <el-table-column label="Actions" width="120">
                                <template #default="scope">
                                    <el-button 
                                        type="primary" 
                                        size="small" 
                                        @click="viewApplication(scope.row.id)"
                                    >
                                        View
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
    import { onMounted, ref } from 'vue';
    import { ElMessage } from 'element-plus';
    import { User, Document, View } from '@element-plus/icons-vue';
    import { api } from '@/api';
    import { useRoute, useRouter } from 'vue-router';

    const route = useRoute();
    const router = useRouter();

    const guarantor = ref({
        name: "Guarantor Name",
        date: "Date Create: 2025-12-23 10:13:42"
    });
    const activeName = ref('1');
    const guarantorId = route.params.guarantorId;
    const overview = ref({
        title: "",
        name: "Broker One",
        guarantor_type: "individual",
        address: "Address",
        phone: "123456789",
        home_phone: "",
        mobile: "",
        email: "broker@gmail.com",
        relationship: "Branch Name",
        birth: "14.05.1986",
        status: "Full-time",
        income: "$200,000.00",
        score: "85",
        drivers_licence_no: "",
        address_unit: "",
        address_street_no: "",
        address_street_name: "",
        address_suburb: "",
        address_state: "",
        address_postcode: "",
        occupation: "",
        employer_name: "",
        company_name: "",
        company_abn: "",
        company_acn: "",
        city: "",
        postal_code: "",
        years_with_employer: ""
    });
    
    const relatedBorrowers = ref([]);
    const relatedApplications = ref([]);
    const loadingBorrowers = ref(false);
    const loadingApplications = ref(false);

    onMounted(() => {
        getGuarantor();
        getRelatedBorrowers();
        getRelatedApplications();
    });

    const getGuarantor = async () => {
        const [err, res] = await api.getGuarantor(guarantorId);
        if (!err) {
            guarantor.value = {
                name: `${res.first_name} ${res.last_name}`,
                date: new Date(res.created_at).toLocaleString()
            };
            overview.value = {
                title: res.title || "",
                name: `${res.first_name} ${res.last_name}`,
                guarantor_type: res.guarantor_type || "individual",
                address: `${res.address_street_name || ''}, ${res.address_suburb || ''}, ${res.address_state || ''} ${res.address_postcode || ''}`,
                phone: res.phone || res.mobile || res.home_phone || "",
                home_phone: res.home_phone || "",
                mobile: res.mobile || "",
                email: res.email,
                relationship: 'Guarantor',
                birth: res.date_of_birth ? new Date(res.date_of_birth).toLocaleDateString() : 'N/A',
                status: res.employment_type || 'N/A',
                income: res.annual_income ? new Intl.NumberFormat('en-US', { 
                    style: 'currency', 
                    currency: 'USD' 
                }).format(res.annual_income) : 'N/A',
                employer_name: res.employer_name || 'N/A',
                occupation: res.occupation || 'N/A',
                drivers_licence_no: res.drivers_licence_no || "",
                address_unit: res.address_unit || "",
                address_street_no: res.address_street_no || "",
                address_street_name: res.address_street_name || "",
                address_suburb: res.address_suburb || "",
                address_state: res.address_state || "",
                address_postcode: res.address_postcode || "",
                company_name: res.company_name || "",
                company_abn: res.company_abn || "",
                company_acn: res.company_acn || "",
                city: res.city || "",
                postal_code: res.postal_code || "",
                years_with_employer: res.years_with_employer || "",
                score: 'N/A'
            };
        } else {
            ElMessage.error({
                message: err.message || 'Failed to fetch guarantor details',
                type: 'error'
            });
        }
    };
    
    const getRelatedBorrowers = async () => {
        loadingBorrowers.value = true;
        try {
            const [err, res] = await api.getGuarantorBorrowers(guarantorId);
            if (!err && res && res.results) {
                relatedBorrowers.value = res.results.map(borrower => ({
                    id: borrower.id,
                    name: `${borrower.first_name || ''} ${borrower.last_name || ''}`.trim() || 'Unnamed Borrower',
                    relationship: 'Guarantor',
                    email: borrower.email || 'N/A',
                    phone: borrower.mobile || borrower.home_phone || borrower.phone || 'N/A'
                }));
            } else {
                console.error('Error loading related borrowers:', err);
                relatedBorrowers.value = [];
            }
        } catch (error) {
            console.error('Error loading related borrowers:', error);
            relatedBorrowers.value = [];
        } finally {
            loadingBorrowers.value = false;
        }
    };
    
    const getRelatedApplications = async () => {
        loadingApplications.value = true;
        try {
            const [err, res] = await api.getGuarantorApplications(guarantorId);
            if (!err && res && res.results) {
                relatedApplications.value = res.results.map(application => ({
                    id: application.id,
                    reference_number: application.reference_number || `APP-${application.id}`,
                    title: application.purpose || 'No Purpose Specified',
                    status: application.stage || 'Unknown',
                    created_at: application.created_at ? new Date(application.created_at).toLocaleDateString() : 'N/A'
                }));
            } else {
                console.error('Error loading related applications:', err);
                relatedApplications.value = [];
            }
        } catch (error) {
            console.error('Error loading related applications:', error);
            relatedApplications.value = [];
        } finally {
            loadingApplications.value = false;
        }
    };
    
    const viewBorrower = (borrowerId) => {
        router.push(`/borrower/${borrowerId}`);
    };
    
    const viewApplication = (applicationId) => {
        router.push(`/application/${applicationId}`);
    };

    // Formatting functions
    const formatTitle = (title) => {
        if (!title) return '-';
        const titleMap = {
            'mr': 'Mr',
            'mrs': 'Mrs',
            'ms': 'Ms',
            'miss': 'Miss',
            'dr': 'Dr',
            'other': 'Other'
        };
        return titleMap[title] || title;
    };

    const formatEmploymentType = (type) => {
        if (!type) return '-';
        const typeMap = {
            'full_time': 'Full Time',
            'part_time': 'Part Time',
            'casual': 'Casual',
            'self_employed': 'Self Employed',
            'contractor': 'Contractor',
            'unemployed': 'Unemployed',
            'retired': 'Retired'
        };
        return typeMap[type] || type;
    };

    const formatFullAddress = (guarantor) => {
        const parts = [];
        if (guarantor.address_unit) parts.push(guarantor.address_unit);
        if (guarantor.address_street_no) parts.push(guarantor.address_street_no);
        if (guarantor.address_street_name) parts.push(guarantor.address_street_name);
        if (guarantor.address_suburb) parts.push(guarantor.address_suburb);
        if (guarantor.address_state) parts.push(guarantor.address_state);
        if (guarantor.address_postcode) parts.push(guarantor.address_postcode);
        
        return parts.length > 0 ? parts.join(' ') : '-';
    };
</script>

<style scoped>
.guarantor {
    min-height: 70vh;
    padding: 20px;
    border-radius: 6px;
    background: #FFF;
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 20px;
}

.title {
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

.tabs {
    width: 100%;
    --el-color-primary: #384144;
}

.label {
    padding: 0 20px;
    color: #949494;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 400;
    line-height: 12px;
}

.tabs :deep(.el-tabs__item) {
    padding: 0;
}

.tabs :deep(.el-tabs__item.is-active .label) {
    color: #384144;
}

.tab {
    padding: 20px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.info {
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 10px;
}

.text {
    font-family: Inter;
    font-weight: 600;
    font-size: 12px;
    line-height: 100%;
    letter-spacing: 0px;
    color: #000000;
}

.applications-section {
    padding: 20px;
}

.loading {
    text-align: center;
    color: #909399;
    font-size: 0.875rem;
    margin-bottom: 20px;
}

.no-data {
    text-align: center;
    color: #909399;
    font-size: 0.875rem;
    margin-bottom: 20px;
}

.applications-header {
    margin-bottom: 20px;
}

.applications-header h3 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #000;
    margin: 0;
}

.applications-table {
    width: 100%;
}
</style>