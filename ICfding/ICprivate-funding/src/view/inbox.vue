<template>
    <div class="inbox">
        <div class="left">
            <div class="title">
                <h1>Inbox</h1>
                <button @click="openComposePopup" class="compose-btn">
                    <i class="icon-compose"></i>
                    Compose
                </button>
            </div>
            <div class="search">
                <img src="@/assets/icons/search.png" alt="search" />
                <input v-model="search" placeholder="Search emails..." @input="filterEmails" />
            </div>
            <div class="filter-tabs">
                <button 
                    v-for="tab in filterTabs" 
                    :key="tab.key"
                    :class="['tab', { active: activeFilter === tab.key }]"
                    @click="setActiveFilter(tab.key)"
                >
                    {{ tab.label }}
                </button>
            </div>
            <div class="email-list">
                <!-- Error state -->
                <div v-if="error" class="error-state">
                    <i class="icon-error"></i>
                    <p>{{ error }}</p>
                    <button @click="loadEmails(true)" class="retry-btn">Retry</button>
                </div>

                <!-- Loading state -->
                <div v-else-if="loading" class="loading-state">
                    <i class="icon-loading"></i>
                    <p>Loading emails...</p>
                </div>

                <!-- Empty state -->
                <div v-else-if="filteredEmails.length === 0" class="empty-state">
                    <i class="icon-inbox-empty"></i>
                    <p>No emails found</p>
                    <p v-if="search || activeFilter !== 'all'" class="empty-hint">
                        Try adjusting your search or filters
                    </p>
                </div>

                <!-- Email list -->
                <div v-else>
                    <div 
                        v-for="(email, index) in filteredEmails" 
                        :key="email.id" 
                        :class="['email-item', { selected: selectedEmail?.id === email.id, unread: !email.is_sent }]"
                        @click="selectEmail(email)"
                    >
                        <div class="email-info">
                            <div class="email-header">
                                <h3>{{ email.created_by_name || email.recipient_email }}</h3>
                                <span class="email-time">{{ formatTime(email.created_at) }}</span>
                            </div>
                            <div class="email-subject">{{ email.subject }}</div>
                            <div class="email-preview">{{ truncateText(email.email_body, 60) }}</div>
                            <div class="email-meta">
                                <span v-if="email.related_application" class="app-id">
                                    App ID: {{ email.related_application }}
                                </span>
                                <span :class="['status', email.is_sent ? 'sent' : 'pending']">
                                    {{ email.is_sent ? 'Sent' : 'Pending' }}
                                </span>
                            </div>
                        </div>
                        <el-badge v-if="!email.is_sent" :value="1" class="unread-badge"></el-badge>
                    </div>

                    <!-- Pagination -->
                    <div v-if="totalCount > pageSize" class="pagination">
                        <div class="pagination-info">
                            Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, totalCount) }} of {{ totalCount }} emails
                        </div>
                        <div class="pagination-controls">
                            <button 
                                @click="previousPage" 
                                :disabled="!hasPreviousPage || loading"
                                class="pagination-btn"
                            >
                                <i class="icon-chevron-left"></i>
                                Previous
                            </button>
                            <span class="page-info">Page {{ currentPage }}</span>
                            <button 
                                @click="nextPage" 
                                :disabled="!hasNextPage || loading"
                                class="pagination-btn"
                            >
                                Next
                                <i class="icon-chevron-right"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="right">
            <div v-if="selectedEmail" class="email-details">
                <div class="email-header-detail">
                    <div class="header-info">
                        <h1>{{ selectedEmail.subject }}</h1>
                        <div class="email-meta-detail">
                            <p><strong>From:</strong> {{ selectedEmail.send_as_user_email || selectedEmail.created_by_name }}</p>
                            <p><strong>To:</strong> {{ selectedEmail.recipient_email }}</p>
                            <p><strong>Date:</strong> {{ formatDateTime(selectedEmail.created_at) }}</p>
                            <p v-if="selectedEmail.related_application">
                                <strong>Application ID:</strong> {{ selectedEmail.related_application }}
                            </p>
                        </div>
                    </div>
                    <div class="email-actions">
                        <button @click="openReplyPopup" class="action-btn reply-btn">
                            <i class="icon-reply"></i>
                            Reply
                        </button>
                        <button @click="openForwardPopup" class="action-btn forward-btn">
                            <i class="icon-forward"></i>
                            Forward
                        </button>
                        <button @click="openPreviewPopup" class="action-btn preview-btn">
                            <i class="icon-preview"></i>
                            Preview
                        </button>
                        <button v-if="selectedEmail.related_application" @click="viewApplication" class="action-btn app-btn">
                            <i class="icon-app"></i>
                            View Application
                        </button>
                    </div>
                </div>
                <div class="email-content">
                    <div v-html="selectedEmail.email_body" class="email-body"></div>
                </div>
            </div>
            <div v-else class="no-selection">
                <div class="no-selection-content">
                    <i class="icon-inbox-large"></i>
                    <h2>Select an email to view</h2>
                    <p>Choose an email from the list to read its contents</p>
                </div>
            </div>
        </div>

        <!-- Email Compose Popup -->
        <EmailCompose 
            v-if="showComposePopup"
            @close="closeComposePopup"
            @send="handleEmailSent"
        />

        <!-- Email Reply Popup -->
        <EmailReply 
            v-if="showReplyPopup"
            :original-email="selectedEmail"
            @close="closeReplyPopup"
            @send="handleEmailSent"
        />

        <!-- Email Forward Popup -->
        <EmailForward 
            v-if="showForwardPopup"
            :original-email="selectedEmail"
            @close="closeForwardPopup"
            @send="handleEmailSent"
        />

        <!-- Email Preview Popup -->
        <EmailPreview 
            v-if="showPreviewPopup"
            :email="selectedEmail"
            @close="closePreviewPopup"
        />
    </div>
</template>

<script setup>
    import { onMounted, ref, computed } from "vue";
    import EmailCompose from "@/components/popup/EmailCompose.vue";
    import EmailReply from "@/components/popup/EmailReply.vue";
    import EmailForward from "@/components/popup/EmailForward.vue";
    import EmailPreview from "@/components/popup/EmailPreview.vue";
    import { useEmailApi } from "@/composables/useEmailApi";

    // Reactive data
    const search = ref("")
    const emails = ref([])
    const selectedEmail = ref(null)
    const activeFilter = ref('all')
    const loading = ref(false)
    const error = ref(null)
    
    // Pagination
    const currentPage = ref(1)
    const pageSize = ref(20)
    const totalCount = ref(0)
    const hasNextPage = ref(false)
    const hasPreviousPage = ref(false)

    // Popup states
    const showComposePopup = ref(false)
    const showReplyPopup = ref(false)
    const showForwardPopup = ref(false)
    const showPreviewPopup = ref(false)

    // Filter tabs
    const filterTabs = [
        { key: 'all', label: 'All' },
        { key: 'sent', label: 'Sent' },
        { key: 'pending', label: 'Pending' },
        { key: 'applications', label: 'Applications' }
    ]

    // Use email API composable
    const { fetchReminders, createReminder } = useEmailApi()

    // Computed properties
    const filteredEmails = computed(() => {
        return emails.value.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    })

    // Build API query parameters
    const buildQueryParams = () => {
        const params = {
            page: currentPage.value,
            page_size: pageSize.value
        }

        // Add search parameter
        if (search.value.trim()) {
            params.search = search.value.trim()
        }

        // Add filter parameters
        switch (activeFilter.value) {
            case 'sent':
                params.is_sent = true
                break
            case 'pending':
                params.is_sent = false
                break
            case 'applications':
                // Filter for emails with related applications
                // This will be handled by the backend
                break
            default:
                // 'all' - no additional filtering
                break
        }

        return params
    }

    // Methods
    const loadEmails = async (resetPage = false) => {
        try {
            loading.value = true
            error.value = null
            
            if (resetPage) {
                currentPage.value = 1
            }
            
            const params = buildQueryParams()
            const response = await fetchReminders(params)
            
            emails.value = response.results || []
            totalCount.value = response.count || 0
            hasNextPage.value = !!response.next
            hasPreviousPage.value = !!response.previous
            
            // Select first email if none selected and emails exist
            if (emails.value.length > 0 && !selectedEmail.value) {
                selectedEmail.value = emails.value[0]
            }
        } catch (err) {
            console.error('Error loading emails:', err)
            error.value = 'Failed to load emails. Please try again.'
            emails.value = []
            totalCount.value = 0
        } finally {
            loading.value = false
        }
    }

    const selectEmail = (email) => {
        selectedEmail.value = email
    }

    const setActiveFilter = (filterKey) => {
        activeFilter.value = filterKey
        loadEmails(true) // Reset to first page when changing filters
    }

    const filterEmails = () => {
        // Debounce search to avoid too many API calls
        clearTimeout(searchTimeout.value)
        searchTimeout.value = setTimeout(() => {
            loadEmails(true)
        }, 300)
    }

    // Search debouncing
    const searchTimeout = ref(null)

    // Pagination methods
    const nextPage = () => {
        if (hasNextPage.value) {
            currentPage.value++
            loadEmails()
        }
    }

    const previousPage = () => {
        if (hasPreviousPage.value && currentPage.value > 1) {
            currentPage.value--
            loadEmails()
        }
    }

    const goToPage = (page) => {
        currentPage.value = page
        loadEmails()
    }

    // Popup methods
    const openComposePopup = () => {
        showComposePopup.value = true
    }

    const closeComposePopup = () => {
        showComposePopup.value = false
    }

    const openReplyPopup = () => {
        if (selectedEmail.value) {
            showReplyPopup.value = true
        }
    }

    const closeReplyPopup = () => {
        showReplyPopup.value = false
    }

    const openForwardPopup = () => {
        if (selectedEmail.value) {
            showForwardPopup.value = true
        }
    }

    const closeForwardPopup = () => {
        showForwardPopup.value = false
    }

    const openPreviewPopup = () => {
        if (selectedEmail.value) {
            showPreviewPopup.value = true
        }
    }

    const closePreviewPopup = () => {
        showPreviewPopup.value = false
    }

    const handleEmailSent = () => {
        // Refresh emails list after sending
        loadEmails()
        // Close all popups
        showComposePopup.value = false
        showReplyPopup.value = false
        showForwardPopup.value = false
    }

    const viewApplication = () => {
        if (selectedEmail.value?.related_application) {
            // Navigate to application view using the correct path format
            window.location.href = `/#/application/${selectedEmail.value.related_application}`
        }
    }

    // Utility functions
    const formatTime = (dateString) => {
        const date = new Date(dateString)
        const now = new Date()
        const diff = now - date
        const minutes = Math.floor(diff / 60000)
        const hours = Math.floor(diff / 3600000)
        const days = Math.floor(diff / 86400000)

        if (minutes < 1) return 'Just now'
        if (minutes < 60) return `${minutes} min ago`
        if (hours < 24) return `${hours}h ago`
        if (days < 7) return `${days}d ago`
        return date.toLocaleDateString()
    }

    const formatDateTime = (dateString) => {
        return new Date(dateString).toLocaleString()
    }

    const truncateText = (text, maxLength) => {
        if (!text) return ''
        const cleanText = text.replace(/<[^>]*>/g, '') // Remove HTML tags
        return cleanText.length > maxLength 
            ? cleanText.substring(0, maxLength) + '...'
            : cleanText
    }

    // Lifecycle
    onMounted(() => {
        loadEmails()
    })
</script>

<style scoped>
    .inbox {
        width: 100%;
        min-height: 610px;
        border-radius: 8px;
        background: #FFF;
        display: flex;
        flex-direction: row;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .left {
        width: 35%;
        display: flex;
        flex-direction: column;
        border-right: 1px solid #E8EBEE;
        background: #FAFBFC;
    }

    .right {
        width: 65%;
        display: flex;
        flex-direction: column;
        background: #FFF;
    }

    .title {
        width: 100%;
        height: 64px;
        padding: 0 20px;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #E8EBEE;
        background: #FFF;
    }

    .compose-btn {
        background: #FF754C;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.875rem;
        transition: background 0.2s;
    }

    .compose-btn:hover {
        background: #E5663F;
    }

    .search {
        width: 100%;
        padding: 16px 20px;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid #E8EBEE;
        background: #FFF;
    }

    .search img {
        width: 18px;
        height: 18px;
        opacity: 0.6;
    }

    .search input {
        border: none;
        outline: none;
        flex: 1;
        color: #384144;
        font-size: 0.875rem;
        background: transparent;
    }

    .search input::placeholder {
        color: #7A858E;
    }

    .filter-tabs {
        display: flex;
        padding: 0 20px;
        border-bottom: 1px solid #E8EBEE;
        background: #FFF;
    }

    .tab {
        padding: 12px 16px;
        border: none;
        background: transparent;
        color: #7A858E;
        font-size: 0.875rem;
        cursor: pointer;
        border-bottom: 2px solid transparent;
        transition: all 0.2s;
    }

    .tab.active {
        color: #FF754C;
        border-bottom-color: #FF754C;
    }

    .tab:hover:not(.active) {
        color: #384144;
    }

    .email-list {
        flex: 1;
        overflow-y: auto;
    }

    .email-item {
        padding: 16px 20px;
        border-bottom: 1px solid #F0F2F3;
        cursor: pointer;
        transition: background 0.2s;
        position: relative;
    }

    .email-item:hover {
        background: #F8F9FA;
    }

    .email-item.selected {
        background: #FFF4F1;
        border-left: 3px solid #FF754C;
    }

    .email-item.unread {
        background: #FFFCFB;
        font-weight: 600;
    }

    .email-info {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .email-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .email-header h3 {
        color: #384144;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0;
    }

    .email-time {
        color: #7A858E;
        font-size: 0.75rem;
        font-weight: 400;
    }

    .email-subject {
        color: #384144;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 4px;
    }

    .email-preview {
        color: #7A858E;
        font-size: 0.8125rem;
        line-height: 1.4;
    }

    .email-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 4px;
    }

    .app-id {
        color: #7A858E;
        font-size: 0.75rem;
        background: #F0F2F3;
        padding: 2px 6px;
        border-radius: 4px;
    }

    .status {
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 500;
    }

    .status.sent {
        background: #E8F5E8;
        color: #2E7D2E;
    }

    .status.pending {
        background: #FFF3CD;
        color: #856404;
    }

    .unread-badge {
        position: absolute;
        top: 16px;
        right: 16px;
    }

    .email-details {
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .email-header-detail {
        padding: 24px;
        border-bottom: 1px solid #E8EBEE;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 20px;
    }

    .header-info {
        flex: 1;
    }

    .header-info h1 {
        color: #384144;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0 0 12px 0;
        line-height: 1.3;
    }

    .email-meta-detail p {
        margin: 4px 0;
        color: #7A858E;
        font-size: 0.875rem;
    }

    .email-meta-detail strong {
        color: #384144;
        font-weight: 600;
    }

    .email-actions {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }

    .action-btn {
        padding: 8px 12px;
        border: 1px solid #E8EBEE;
        border-radius: 6px;
        background: #FFF;
        color: #384144;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s;
    }

    .action-btn:hover {
        background: #F8F9FA;
        border-color: #D1D5DB;
    }

    .reply-btn:hover {
        background: #E8F5E8;
        border-color: #2E7D2E;
        color: #2E7D2E;
    }

    .forward-btn:hover {
        background: #E3F2FD;
        border-color: #1976D2;
        color: #1976D2;
    }

    .preview-btn:hover {
        background: #FFF3E0;
        border-color: #F57C00;
        color: #F57C00;
    }

    .app-btn:hover {
        background: #FFF4F1;
        border-color: #FF754C;
        color: #FF754C;
    }

    .email-content {
        flex: 1;
        padding: 24px;
        overflow-y: auto;
    }

    .email-body {
        color: #384144;
        font-size: 0.9375rem;
        line-height: 1.6;
    }

    .no-selection {
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .no-selection-content {
        text-align: center;
        color: #7A858E;
    }

    .no-selection-content h2 {
        color: #384144;
        font-size: 1.125rem;
        margin: 16px 0 8px 0;
    }

    .no-selection-content p {
        font-size: 0.875rem;
        margin: 0;
    }

    h1 {
        color: #384144;
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
    }

    /* Icon placeholders - replace with actual icons */
    .icon-compose::before { content: "✉"; }
    .icon-reply::before { content: "↩"; }
    .icon-forward::before { content: "↪"; }
    .icon-preview::before { content: "👁"; }
    .icon-app::before { content: "📄"; }
    .icon-inbox-large::before { content: "📥"; font-size: 3rem; }
    .icon-error::before { content: "⚠"; color: #DC3545; font-size: 2rem; }
    .icon-loading::before { content: "⏳"; color: #007BFF; font-size: 2rem; animation: spin 1s linear infinite; }
    .icon-inbox-empty::before { content: "📭"; font-size: 3rem; color: #7A858E; }
    .icon-chevron-left::before { content: "‹"; }
    .icon-chevron-right::before { content: "›"; }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Error, Loading, and Empty States */
    .error-state,
    .loading-state,
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 20px;
        text-align: center;
        color: #7A858E;
    }

    .error-state i,
    .loading-state i,
    .empty-state i {
        margin-bottom: 16px;
    }

    .error-state p,
    .loading-state p,
    .empty-state p {
        margin: 8px 0;
        font-size: 0.875rem;
    }

    .empty-hint {
        font-size: 0.75rem !important;
        color: #9CA3AF !important;
    }

    .retry-btn {
        margin-top: 16px;
        padding: 8px 16px;
        background: #007BFF;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .retry-btn:hover {
        background: #0056B3;
    }

    /* Pagination */
    .pagination {
        padding: 16px 20px;
        border-top: 1px solid #E8EBEE;
        background: #FAFBFC;
    }

    .pagination-info {
        text-align: center;
        color: #7A858E;
        font-size: 0.75rem;
        margin-bottom: 12px;
    }

    .pagination-controls {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 16px;
    }

    .pagination-btn {
        padding: 6px 12px;
        border: 1px solid #E8EBEE;
        border-radius: 4px;
        background: #FFF;
        color: #384144;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 4px;
        transition: all 0.2s;
    }

    .pagination-btn:hover:not(:disabled) {
        background: #F8F9FA;
        border-color: #D1D5DB;
    }

    .pagination-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .page-info {
        color: #7A858E;
        font-size: 0.875rem;
        font-weight: 500;
        min-width: 60px;
        text-align: center;
    }
</style>
