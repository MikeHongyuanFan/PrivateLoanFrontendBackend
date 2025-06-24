<template>
    <div class="archived-applications">
        <div class="header">
            <h1>Archived Applications</h1>
            <p>Applications automatically archived when status changes to "Closed"</p>
            <el-button @click="goBack" type="primary">
                <el-icon><ArrowLeft /></el-icon>
                Back to Applications
            </el-button>
        </div>
        
        <div class="filters">
            <div class="left">
                <div class="filter">
                    <h1>Search</h1>
                    <el-input v-model="selected.search" style="width: 180px" placeholder="Search archived..." />
                </div>
                <Search @click="searchArchived"></Search>
                <Clear @click="handleClear"></Clear>
            </div>
        </div>
        
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
                <div class="stats-bar">
                    <el-alert
                        title="Archived Applications"
                        :description="`Showing ${archivedApplications.length} archived applications. These were automatically archived when their status changed to 'Closed'.`"
                        type="info"
                        :closable="false"
                        show-icon>
                    </el-alert>
                </div>
                
                <ApplicationTable 
                    :selected="selected" 
                    :paginationInfo="paginationInfo"
                    :data="filteredArchivedApplications"
                    @getData="getArchivedApplications"
                    @edit="handleEdit"
                    @click="handleApplicationClick"
                ></ApplicationTable>
                
                <div class="flex">
                    <Pagination :="paginationInfo" @change="handleChange"></Pagination>
                </div>
            </div>
        </div>
        
        <transition name="slide-right-popup">
            <div v-if="popup" class="popup-container">
                <EditApplication
                    :applicationId="editApplicationId"
                    @close="close"
                    @saved="handleApplicationSaved"
                ></EditApplication>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, onActivated, computed } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '@/api';
import EditApplication from '@/view/application/edit/EditApplication.vue';
import Search from '@/components/buttons/search.vue';
import Clear from '@/components/buttons/clear.vue';
import { ArrowLeft } from '@element-plus/icons-vue';

import { Pagination } from '@/components'
import { ApplicationTable } from './components'
import { ElMessage } from 'element-plus';

const router = useRouter();
const popup = ref(false)
const editApplicationId = ref(null)

const tabs = [
    { name: 'all', label: 'All Archived', width: '32px' },
    { name: 'closed', label: 'Closed', width: '82px' },
]

const activeTab = ref('all')
const selected = ref({
    search: "",
    page: 1
})

const archivedApplications = ref([])
const paginationInfo = ref({
    total: 0,
})

onActivated(() => {
    getArchivedApplications()
})

const searchArchived = () => {
    getArchivedApplications()
}

const handleClear = () => {
    selected.value = ({page: 1})
    getArchivedApplications()
}

const close = () => {
    popup.value = false;
    editApplicationId.value = null;
}

const getArchivedApplications = async () => {
    const [err, res] = await api.archivedApplications(selected.value)
    if (!err) {
        console.log('Archived applications:', res);
        paginationInfo.value.total = res.count || 0
        archivedApplications.value = (res.results || []).map(item => ({
            ...item,
            create: item.created_at ? item.created_at.split('T')[0] : item.created_at,
            update: item.updated_at ? item.updated_at.split('T')[0] : item.updated_at
        }))
    } else {
        console.error('Error fetching archived applications:', err)
        ElMessage.error('Failed to load archived applications')
    }
}

const handleChange = (currentPage) => {
    selected.value.page = currentPage
    getArchivedApplications()
}

const handleEdit = (id) => {
    console.log("Edit button clicked for archived application ID:", id);
    editApplicationId.value = id;
    popup.value = true;
}

const handleApplicationClick = (application) => {
    router.push(`/application/${application.id}`)
}

const handleApplicationSaved = () => {
    getArchivedApplications()
    close()
}

const selectStatus = (name) => {
    activeTab.value = name
}

const filteredArchivedApplications = computed(() => {
    if (activeTab.value === 'all') {
        return archivedApplications.value
    }
    return archivedApplications.value.filter(app => app.stage === activeTab.value)
})

const goBack = () => {
    router.push('/application')
}
</script>

<style lang="scss" scoped>
.archived-applications {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.header {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #dee2e6;
    
    h1 {
        color: #495057;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
    }
    
    p {
        color: #6c757d;
        margin: 0;
        font-size: 1rem;
    }
}

.filters {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    
    .left {
        display: flex;
        align-items: center;
        gap: 15px;
        
        .filter {
            display: flex;
            flex-direction: column;
            gap: 5px;
            
            h1 {
                color: #384144;
                font-size: 0.9rem;
                font-weight: 500;
                margin: 0;
            }
        }
    }
}

.container {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.tabs-scroll {
    width: 100%;
    border-bottom: 1px solid #e8ebee;
}

.tab-bar {
    display: flex;
    gap: 10px;
    padding: 0 0 10px 0;
    white-space: nowrap;
}

.tab-item {
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    color: #7a858e;
    font-size: 0.9rem;
    font-weight: 400;
    transition: all 0.3s ease;
    
    &:hover {
        background: #f8f9fa;
        color: #495057;
    }
    
    &.active {
        background: #2984de;
        color: white;
    }
}

.list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.stats-bar {
    margin-bottom: 15px;
}

.flex {
    display: flex;
    justify-content: flex-end;
    padding: 15px 0;
}

.popup-container {
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    z-index: 1000;
}

.slide-right-popup-enter-active,
.slide-right-popup-leave-active {
    transition: transform 0.3s ease-in-out;
}

.slide-right-popup-enter-from,
.slide-right-popup-leave-to {
    transform: translateX(100%);
}

.slide-right-popup-enter-to,
.slide-right-popup-leave-from {
    transform: translateX(0);
}
</style> 