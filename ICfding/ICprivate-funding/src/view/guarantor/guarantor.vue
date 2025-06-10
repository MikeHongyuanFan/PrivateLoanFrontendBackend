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
                    <div class="label">Overview</div>
                </template>
                <div class="tab">
                    <div class="info">
                        <p style="color: #7A858E">Guarantor Name</p>
                        <p>{{ overview.name || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Guarantor Address</p>
                        <p>{{ overview.address || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Phone Number</p>
                        <p>{{ overview.phone || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Email Address</p>
                        <p>{{ overview.email || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Relationship to Borrower</p>
                        <p>{{ overview.relationship || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Date of Birth</p>
                        <p>{{ overview.birth || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Employment Status</p>
                        <p>{{ overview.status || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Annual Income</p>
                        <p>{{ overview.income || '-' }}</p>
                    </div>
                    <div class="info">
                        <p style="color: #7A858E">Credit Score</p>
                        <p>{{ overview.score || '-' }}</p>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane name="2">
                <template #label>
                    <div class="label">Related Borrowers</div>
                </template>
                <div class="tab">
                    <el-table 
                        v-loading="loadingBorrowers"
                        :data="relatedBorrowers"
                        style="width: 100%"
                        empty-text="No related borrowers found"
                    >
                        <el-table-column prop="id" label="ID" width="80" />
                        <el-table-column prop="name" label="Borrower Name" />
                        <el-table-column prop="relationship" label="Relationship" />
                        <el-table-column prop="email" label="Email" />
                        <el-table-column prop="phone" label="Phone" />
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
            </el-tab-pane>
            <el-tab-pane name="3">
                <template #label>
                    <div class="label">Related Applications</div>
                </template>
                <div class="tab">
                    <el-table 
                        v-loading="loadingApplications"
                        :data="relatedApplications"
                        style="width: 100%"
                        empty-text="No related applications found"
                    >
                        <el-table-column prop="id" label="ID" width="80" />
                        <el-table-column prop="title" label="Application Title" />
                        <el-table-column prop="status" label="Status" />
                        <el-table-column prop="created_at" label="Created Date" />
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
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
    import { onMounted, ref } from 'vue';
    import { ElMessage } from 'element-plus';
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
        name: "Broker One",
        address: "Address",
        phone: "123456789",
        email: "broker@gmail.com",
        relationship: "Branch Name",
        birth: "14.05.1986",
        status: "Full-time",
        income: "$200,000.00",
        score: "85"
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
                name: `${res.first_name} ${res.last_name}`,
                address: `${res.address_street_name || ''}, ${res.address_suburb || ''}, ${res.address_state || ''} ${res.address_postcode || ''}`,
                phone: res.mobile || res.phone,
                email: res.email,
                relationship: res.relationship === 'other' ? res.relationship_other : res.relationship,
                birth: new Date(res.date_of_birth).toLocaleDateString(),
                status: res.employment_type,
                income: new Intl.NumberFormat('en-US', { 
                    style: 'currency', 
                    currency: 'USD' 
                }).format(res.annual_income),
                employer: res.employer_name || 'N/A',
                years_employed: res.years_with_employer ? `${res.years_with_employer} years` : 'N/A',
                score: res.credit_score || 'N/A'
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
            if (!err && res.results) {
                relatedBorrowers.value = res.results.map(borrower => ({
                    id: borrower.id,
                    name: `${borrower.first_name} ${borrower.last_name}`,
                    relationship: borrower.relationship === 'other' ? borrower.relationship_other : borrower.relationship,
                    email: borrower.email,
                    phone: borrower.mobile || borrower.phone
                }));
            } else if (err) {
                console.error('Error fetching related borrowers:', err);
            }
        } catch (error) {
            console.error('Error fetching related borrowers:', error);
        } finally {
            loadingBorrowers.value = false;
        }
    };
    
    const getRelatedApplications = async () => {
        loadingApplications.value = true;
        try {
            const [err, res] = await api.getGuarantorApplications(guarantorId);
            if (!err && res.results) {
                relatedApplications.value = res.results.map(app => ({
                    id: app.id,
                    title: app.title || `Application #${app.id}`,
                    status: app.status,
                    created_at: new Date(app.created_at).toLocaleDateString()
                }));
            } else if (err) {
                console.error('Error fetching related applications:', err);
            }
        } catch (error) {
            console.error('Error fetching related applications:', error);
        } finally {
            loadingApplications.value = false;
        }
    };
    
    const viewBorrower = (borrowerId) => {
        router.push(`/borrowers/${borrowerId}`);
    };
    
    const viewApplication = (applicationId) => {
        router.push(`/applications/${applicationId}`);
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
        color: #000;
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
</style>