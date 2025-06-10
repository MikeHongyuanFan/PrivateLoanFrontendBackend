<template>
    <div class="popup-overlay" @click="closeIfClickOutside">
        <div class="popup-container" @click.stop>
            <div class="popup-header">
                <h2>Email Preview</h2>
                <div class="header-actions">
                    <button @click="printEmail" class="action-btn print-btn" title="Print Email">
                        <i class="icon-print"></i>
                        Print
                    </button>
                    <button @click="copyToClipboard" class="action-btn copy-btn" title="Copy Content">
                        <i class="icon-copy"></i>
                        Copy
                    </button>
                    <button @click="closePopup" class="close-btn">
                        <i class="icon-close"></i>
                    </button>
                </div>
            </div>
            
            <div class="email-preview" ref="emailContent">
                <div class="email-header-section">
                    <div class="email-metadata">
                        <div class="metadata-row">
                            <span class="label">From:</span>
                            <span class="value">{{ email.send_as_user_email || email.created_by_name || 'Unknown Sender' }}</span>
                        </div>
                        <div class="metadata-row">
                            <span class="label">To:</span>
                            <span class="value">{{ email.recipient_email }}</span>
                        </div>
                        <div class="metadata-row">
                            <span class="label">Subject:</span>
                            <span class="value">{{ email.subject }}</span>
                        </div>
                        <div class="metadata-row">
                            <span class="label">Date:</span>
                            <span class="value">{{ formatDateTime(email.created_at) }}</span>
                        </div>
                        <div v-if="email.related_application" class="metadata-row">
                            <span class="label">Application ID:</span>
                            <span class="value application-id">{{ email.related_application }}</span>
                        </div>
                        <div class="metadata-row">
                            <span class="label">Status:</span>
                            <span :class="['value', 'status-badge', email.is_sent ? 'sent' : 'pending']">
                                {{ email.is_sent ? 'Sent' : 'Pending' }}
                            </span>
                        </div>
                        <div v-if="email.sent_at" class="metadata-row">
                            <span class="label">Sent At:</span>
                            <span class="value">{{ formatDateTime(email.sent_at) }}</span>
                        </div>
                        <div v-if="email.error_message" class="metadata-row error">
                            <span class="label">Error:</span>
                            <span class="value error-text">{{ email.error_message }}</span>
                        </div>
                    </div>
                </div>
                
                <div class="email-body-section">
                    <div class="body-header">
                        <h3>Message Content</h3>
                        <div class="body-actions">
                            <button @click="toggleRawView" class="toggle-btn">
                                <i :class="showRaw ? 'icon-formatted' : 'icon-raw'"></i>
                                {{ showRaw ? 'Formatted View' : 'Raw HTML' }}
                            </button>
                        </div>
                    </div>
                    
                    <div class="email-content">
                        <div v-if="!showRaw" class="formatted-content" v-html="email.email_body"></div>
                        <pre v-else class="raw-content">{{ email.email_body }}</pre>
                    </div>
                </div>

                <div v-if="email.related_application" class="related-info-section">
                    <h3>Related Information</h3>
                    <div class="related-content">
                        <div class="info-item">
                            <span class="info-label">Application ID:</span>
                            <span class="info-value">
                                {{ email.related_application }}
                                <button @click="viewApplication" class="link-btn">
                                    <i class="icon-external"></i>
                                    View Application
                                </button>
                            </span>
                        </div>
                        <div v-if="email.related_borrower" class="info-item">
                            <span class="info-label">Borrower ID:</span>
                            <span class="info-value">{{ email.related_borrower }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="popup-footer">
                <div class="footer-info">
                    <span class="email-id">Email ID: {{ email.id }}</span>
                    <span class="created-info">Created by {{ email.created_by_name }} on {{ formatDateTime(email.created_at) }}</span>
                </div>
                <div class="footer-actions">
                    <button @click="downloadAsFile" class="btn-secondary">
                        <i class="icon-download"></i>
                        Download
                    </button>
                    <button @click="closePopup" class="btn-primary">
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'

    // Props and Emits
    const props = defineProps({
        email: {
            type: Object,
            required: true
        }
    })
    
    const emit = defineEmits(['close'])

    // Reactive data
    const emailContent = ref(null)
    const showRaw = ref(false)

    // Methods
    const formatDateTime = (dateString) => {
        return new Date(dateString).toLocaleString()
    }

    const closePopup = () => {
        emit('close')
    }

    const closeIfClickOutside = (event) => {
        if (event.target === event.currentTarget) {
            closePopup()
        }
    }

    const toggleRawView = () => {
        showRaw.value = !showRaw.value
    }

    const printEmail = () => {
        const printWindow = window.open('', '_blank')
        const emailHtml = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>Email: ${props.email.subject}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; color: #333; }
                    .header { border-bottom: 2px solid #eee; padding-bottom: 15px; margin-bottom: 20px; }
                    .metadata { margin-bottom: 10px; }
                    .label { font-weight: bold; margin-right: 10px; }
                    .content { line-height: 1.6; }
                    .status-sent { color: green; }
                    .status-pending { color: orange; }
                    .error { color: red; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>${props.email.subject}</h1>
                    <div class="metadata">
                        <div><span class="label">From:</span> ${props.email.send_as_user_email || props.email.created_by_name}</div>
                        <div><span class="label">To:</span> ${props.email.recipient_email}</div>
                        <div><span class="label">Date:</span> ${formatDateTime(props.email.created_at)}</div>
                        ${props.email.related_application ? `<div><span class="label">Application ID:</span> ${props.email.related_application}</div>` : ''}
                        <div><span class="label">Status:</span> <span class="status-${props.email.is_sent ? 'sent' : 'pending'}">${props.email.is_sent ? 'Sent' : 'Pending'}</span></div>
                    </div>
                </div>
                <div class="content">
                    ${props.email.email_body}
                </div>
            </body>
            </html>
        `
        
        printWindow.document.write(emailHtml)
        printWindow.document.close()
        printWindow.print()
    }

    const copyToClipboard = async () => {
        try {
            const textContent = `
Subject: ${props.email.subject}
From: ${props.email.send_as_user_email || props.email.created_by_name}
To: ${props.email.recipient_email}
Date: ${formatDateTime(props.email.created_at)}
${props.email.related_application ? `Application ID: ${props.email.related_application}` : ''}
Status: ${props.email.is_sent ? 'Sent' : 'Pending'}

${props.email.email_body.replace(/<[^>]*>/g, '')}
            `.trim()

            await navigator.clipboard.writeText(textContent)
            
            // Show temporary success message (you can replace with a proper toast notification)
            alert('Email content copied to clipboard!')
        } catch (err) {
            console.error('Failed to copy to clipboard:', err)
            alert('Failed to copy content. Please try again.')
        }
    }

    const downloadAsFile = () => {
        const textContent = `
Subject: ${props.email.subject}
From: ${props.email.send_as_user_email || props.email.created_by_name}
To: ${props.email.recipient_email}
Date: ${formatDateTime(props.email.created_at)}
${props.email.related_application ? `Application ID: ${props.email.related_application}` : ''}
Status: ${props.email.is_sent ? 'Sent' : 'Pending'}

${props.email.email_body.replace(/<[^>]*>/g, '')}
        `.trim()

        const blob = new Blob([textContent], { type: 'text/plain' })
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `email-${props.email.id}-${props.email.subject.replace(/[^a-zA-Z0-9]/g, '_')}.txt`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)
    }

    const viewApplication = () => {
        if (props.email.related_application) {
            window.open(`/applications/${props.email.related_application}`, '_blank')
        }
    }

    // Lifecycle
    onMounted(() => {
        // Focus on the close button for keyboard accessibility
        const closeBtn = document.querySelector('.close-btn')
        if (closeBtn) {
            closeBtn.focus()
        }
    })
</script>

<style scoped>
    .popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        backdrop-filter: blur(4px);
    }

    .popup-container {
        background: white;
        border-radius: 12px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        width: 90%;
        max-width: 1000px;
        max-height: 90vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }

    .popup-header {
        padding: 20px 24px;
        border-bottom: 1px solid #E8EBEE;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FAFBFC;
    }

    .popup-header h2 {
        margin: 0;
        color: #384144;
        font-size: 1.25rem;
        font-weight: 600;
    }

    .header-actions {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .action-btn {
        background: #F8F9FA;
        border: 1px solid #D1D5DB;
        color: #384144;
        padding: 8px 12px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s;
    }

    .action-btn:hover {
        background: #E8EBEE;
    }

    .print-btn:hover {
        background: #E3F2FD;
        border-color: #1976D2;
        color: #1976D2;
    }

    .copy-btn:hover {
        background: #E8F5E8;
        border-color: #2E7D2E;
        color: #2E7D2E;
    }

    .close-btn {
        background: none;
        border: none;
        color: #7A858E;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        transition: all 0.2s;
    }

    .close-btn:hover {
        background: #F0F2F3;
        color: #384144;
    }

    .email-preview {
        flex: 1;
        overflow-y: auto;
        padding: 24px;
        display: flex;
        flex-direction: column;
        gap: 24px;
    }

    .email-header-section {
        background: #F8F9FA;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #E8EBEE;
    }

    .email-metadata {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .metadata-row {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .metadata-row.error {
        padding: 8px;
        background: #FEF2F2;
        border-radius: 4px;
        border: 1px solid #FCA5A5;
    }

    .label {
        font-weight: 600;
        color: #384144;
        min-width: 120px;
        font-size: 0.875rem;
    }

    .value {
        color: #7A858E;
        font-size: 0.875rem;
        flex: 1;
    }

    .application-id {
        background: #E3F2FD;
        color: #1976D2;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 500;
    }

    .status-badge {
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 500;
        font-size: 0.8125rem;
    }

    .status-badge.sent {
        background: #E8F5E8;
        color: #2E7D2E;
    }

    .status-badge.pending {
        background: #FFF3CD;
        color: #856404;
    }

    .error-text {
        color: #DC2626;
        font-weight: 500;
    }

    .email-body-section {
        border: 1px solid #E8EBEE;
        border-radius: 8px;
        overflow: hidden;
    }

    .body-header {
        background: #FAFBFC;
        padding: 16px 20px;
        border-bottom: 1px solid #E8EBEE;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .body-header h3 {
        margin: 0;
        color: #384144;
        font-size: 1rem;
        font-weight: 600;
    }

    .toggle-btn {
        background: none;
        border: 1px solid #D1D5DB;
        color: #7A858E;
        padding: 6px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s;
    }

    .toggle-btn:hover {
        background: #E8EBEE;
        color: #384144;
    }

    .email-content {
        padding: 20px;
        background: white;
    }

    .formatted-content {
        color: #384144;
        font-size: 0.9375rem;
        line-height: 1.6;
    }

    .formatted-content * {
        max-width: 100%;
    }

    .raw-content {
        color: #374151;
        font-size: 0.8125rem;
        line-height: 1.5;
        white-space: pre-wrap;
        word-break: break-word;
        background: #F9FAFB;
        padding: 16px;
        border-radius: 4px;
        border: 1px solid #E5E7EB;
        margin: 0;
    }

    .related-info-section {
        background: #FFFBEB;
        border: 1px solid #FCD34D;
        border-radius: 8px;
        padding: 20px;
    }

    .related-info-section h3 {
        margin: 0 0 16px 0;
        color: #92400E;
        font-size: 1rem;
        font-weight: 600;
    }

    .related-content {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .info-item {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .info-label {
        font-weight: 600;
        color: #92400E;
        min-width: 120px;
        font-size: 0.875rem;
    }

    .info-value {
        color: #B45309;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .link-btn {
        background: none;
        border: 1px solid #D97706;
        color: #D97706;
        padding: 4px 8px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.75rem;
        display: flex;
        align-items: center;
        gap: 4px;
        transition: all 0.2s;
    }

    .link-btn:hover {
        background: #D97706;
        color: white;
    }

    .popup-footer {
        padding: 20px 24px;
        border-top: 1px solid #E8EBEE;
        background: #FAFBFC;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
    }

    .footer-info {
        display: flex;
        flex-direction: column;
        gap: 4px;
        font-size: 0.8125rem;
        color: #7A858E;
    }

    .email-id {
        font-weight: 500;
        color: #384144;
    }

    .footer-actions {
        display: flex;
        gap: 12px;
    }

    .btn-primary,
    .btn-secondary {
        padding: 10px 16px;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.2s;
        border: none;
    }

    .btn-primary {
        background: #FF754C;
        color: white;
    }

    .btn-primary:hover {
        background: #E5663F;
    }

    .btn-secondary {
        background: #F8F9FA;
        color: #384144;
        border: 1px solid #D1D5DB;
    }

    .btn-secondary:hover {
        background: #E8EBEE;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .popup-container {
            width: 95%;
            max-height: 95vh;
        }

        .header-actions {
            flex-wrap: wrap;
        }

        .metadata-row {
            flex-direction: column;
            align-items: flex-start;
            gap: 4px;
        }

        .label {
            min-width: auto;
        }

        .popup-footer {
            flex-direction: column;
            align-items: stretch;
        }

        .footer-actions {
            justify-content: stretch;
        }

        .btn-primary,
        .btn-secondary {
            flex: 1;
            justify-content: center;
        }
    }

    /* Icon placeholders - replace with actual icons */
    .icon-close::before { content: "✕"; }
    .icon-print::before { content: "🖨"; }
    .icon-copy::before { content: "📋"; }
    .icon-download::before { content: "⬇"; }
    .icon-external::before { content: "🔗"; }
    .icon-formatted::before { content: "📄"; }
    .icon-raw::before { content: "📝"; }
</style> 