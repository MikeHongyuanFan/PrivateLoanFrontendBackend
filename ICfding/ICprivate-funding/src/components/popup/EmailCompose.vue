<template>
    <div class="popup-overlay" @click="closeIfClickOutside">
        <div class="popup-container" @click.stop>
            <div class="popup-header">
                <h2>Compose Email</h2>
                <button @click="closePopup" class="close-btn">
                    <i class="icon-close"></i>
                </button>
            </div>
            
            <form @submit.prevent="sendEmail" class="email-form">
                <div class="form-section">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="recipient_type">Recipient Type</label>
                            <select v-model="emailData.recipient_type" id="recipient_type" required>
                                <option value="client">Client</option>
                                <option value="bdm">Business Development Manager</option>
                                <option value="broker">Broker</option>
                                <option value="custom">Custom Email</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="recipient_email">To</label>
                            <input 
                                v-model="emailData.recipient_email" 
                                type="email" 
                                id="recipient_email" 
                                placeholder="recipient@example.com"
                                required
                            />
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="related_application">Application ID (Optional)</label>
                            <input 
                                v-model="emailData.related_application" 
                                type="number" 
                                id="related_application" 
                                placeholder="Enter application ID"
                            />
                        </div>
                        <div class="form-group">
                            <label for="send_datetime">Send Date & Time</label>
                            <input 
                                v-model="emailData.send_datetime" 
                                type="datetime-local" 
                                id="send_datetime"
                                :min="minDateTime"
                            />
                        </div>
                    </div>

                    <div class="form-group full-width">
                        <label for="subject">Subject</label>
                        <input 
                            v-model="emailData.subject" 
                            type="text" 
                            id="subject" 
                            placeholder="Enter email subject"
                            required
                        />
                    </div>
                </div>

                <div class="form-section">
                    <div class="editor-toolbar">
                        <button type="button" @click="formatText('bold')" class="toolbar-btn" title="Bold">
                            <i class="icon-bold"></i>
                        </button>
                        <button type="button" @click="formatText('italic')" class="toolbar-btn" title="Italic">
                            <i class="icon-italic"></i>
                        </button>
                        <button type="button" @click="formatText('underline')" class="toolbar-btn" title="Underline">
                            <i class="icon-underline"></i>
                        </button>
                        <div class="toolbar-divider"></div>
                        <button type="button" @click="insertTemplate" class="toolbar-btn" title="Insert Template">
                            <i class="icon-template"></i>
                        </button>
                        <button type="button" @click="insertSignature" class="toolbar-btn" title="Insert Signature">
                            <i class="icon-signature"></i>
                        </button>
                    </div>
                    
                    <div class="form-group">
                        <label for="email_body">Message</label>
                        <div 
                            ref="emailBodyEditor"
                            class="email-editor"
                            contenteditable="true"
                            @input="updateEmailBody"
                            @paste="handlePaste"
                            placeholder="Type your message here..."
                        ></div>
                        <div class="editor-footer">
                            <span class="character-count">{{ characterCount }} characters</span>
                        </div>
                    </div>
                </div>

                <div class="popup-actions">
                    <button type="button" @click="saveDraft" class="btn-secondary" :disabled="loading">
                        <i class="icon-save"></i>
                        Save Draft
                    </button>
                    <div class="action-group">
                        <button type="button" @click="closePopup" class="btn-cancel">
                            Cancel
                        </button>
                        <button type="submit" class="btn-primary" :disabled="loading || !isFormValid">
                            <i v-if="loading" class="icon-loading"></i>
                            <i v-else class="icon-send"></i>
                            {{ loading ? 'Sending...' : 'Send Email' }}
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted, nextTick } from 'vue'
    import { useEmailApi } from '@/composables/useEmailApi'

    // Props and Emits
    const emit = defineEmits(['close', 'send'])

    // Reactive data
    const emailBodyEditor = ref(null)
    const loading = ref(false)
    const emailData = ref({
        recipient_type: 'custom',
        recipient_email: '',
        subject: '',
        email_body: '',
        send_datetime: '',
        related_application: null,
        related_borrower: null,
        send_as_user: null,
        reply_to_user: null
    })

    // Email API composable
    const { sendEmail: apiSendEmail, error } = useEmailApi()

    // Computed properties
    const minDateTime = computed(() => {
        const now = new Date()
        return now.toISOString().slice(0, 16)
    })

    const characterCount = computed(() => {
        return emailData.value.email_body.length
    })

    const isFormValid = computed(() => {
        return emailData.value.recipient_email && 
               emailData.value.subject && 
               emailData.value.email_body.trim()
    })

    // Methods
    const updateEmailBody = () => {
        if (emailBodyEditor.value) {
            emailData.value.email_body = emailBodyEditor.value.innerHTML
        }
    }

    const handlePaste = (event) => {
        event.preventDefault()
        const text = event.clipboardData.getData('text/plain')
        document.execCommand('insertText', false, text)
    }

    const formatText = (command) => {
        document.execCommand(command, false, null)
        emailBodyEditor.value?.focus()
    }

    const insertTemplate = () => {
        const template = `
            <p>Dear [Recipient Name],</p>
            <p>I hope this email finds you well.</p>
            <p>[Your message here]</p>
            <p>Best regards,<br/>
            [Your Name]</p>
        `
        document.execCommand('insertHTML', false, template)
        emailBodyEditor.value?.focus()
    }

    const insertSignature = () => {
        const signature = `
            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #e0e0e0;">
                <p><strong>[Your Name]</strong><br/>
                [Your Title]<br/>
                [Company Name]<br/>
                Email: [your.email@company.com]<br/>
                Phone: [Your Phone Number]</p>
            </div>
        `
        document.execCommand('insertHTML', false, signature)
        emailBodyEditor.value?.focus()
    }

    const closePopup = () => {
        emit('close')
    }

    const closeIfClickOutside = (event) => {
        if (event.target === event.currentTarget) {
            closePopup()
        }
    }

    const saveDraft = () => {
        // Save to localStorage as draft
        const draft = {
            ...emailData.value,
            savedAt: new Date().toISOString()
        }
        localStorage.setItem('emailDraft', JSON.stringify(draft))
        
        // Show confirmation (you can add a toast notification here)
        alert('Draft saved successfully!')
    }

    const loadDraft = () => {
        const draft = localStorage.getItem('emailDraft')
        if (draft) {
            const draftData = JSON.parse(draft)
            Object.assign(emailData.value, draftData)
            
            // Update editor content
            nextTick(() => {
                if (emailBodyEditor.value) {
                    emailBodyEditor.value.innerHTML = draftData.email_body || ''
                }
            })
        }
    }

    const sendEmail = async () => {
        if (!isFormValid.value) return

        try {
            loading.value = true
            
            // Prepare email data
            const emailPayload = {
                ...emailData.value,
                send_datetime: emailData.value.send_datetime || new Date().toISOString()
            }

            // Send email
            await apiSendEmail(emailPayload)
            
            // Clear draft
            localStorage.removeItem('emailDraft')
            
            // Emit success event
            emit('send')
            
            // Close popup
            closePopup()
        } catch (err) {
            console.error('Failed to send email:', err)
            // You can add error notification here
            alert('Failed to send email. Please try again.')
        } finally {
            loading.value = false
        }
    }

    // Lifecycle
    onMounted(() => {
        // Set default send time to now
        emailData.value.send_datetime = minDateTime.value
        
        // Load any existing draft
        loadDraft()
        
        // Focus on recipient email field
        nextTick(() => {
            const recipientInput = document.getElementById('recipient_email')
            if (recipientInput) {
                recipientInput.focus()
            }
        })
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
        max-width: 800px;
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

    .email-form {
        flex: 1;
        overflow-y: auto;
        padding: 24px;
        display: flex;
        flex-direction: column;
        gap: 24px;
    }

    .form-section {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }

    .form-group {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .form-group.full-width {
        grid-column: 1 / -1;
    }

    .form-group label {
        color: #384144;
        font-size: 0.875rem;
        font-weight: 500;
    }

    .form-group input,
    .form-group select {
        padding: 10px 12px;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
        font-size: 0.875rem;
        color: #384144;
        background: white;
        transition: all 0.2s;
    }

    .form-group input:focus,
    .form-group select:focus {
        outline: none;
        border-color: #FF754C;
        box-shadow: 0 0 0 3px rgba(255, 117, 76, 0.1);
    }

    .editor-toolbar {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border: 1px solid #D1D5DB;
        border-bottom: none;
        border-radius: 6px 6px 0 0;
        background: #FAFBFC;
    }

    .toolbar-btn {
        background: none;
        border: none;
        color: #7A858E;
        padding: 6px 8px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.875rem;
        transition: all 0.2s;
    }

    .toolbar-btn:hover {
        background: #E8EBEE;
        color: #384144;
    }

    .toolbar-divider {
        width: 1px;
        height: 20px;
        background: #D1D5DB;
        margin: 0 4px;
    }

    .email-editor {
        min-height: 200px;
        padding: 12px;
        border: 1px solid #D1D5DB;
        border-radius: 0 0 6px 6px;
        font-size: 0.875rem;
        line-height: 1.5;
        color: #384144;
        background: white;
        outline: none;
        overflow-y: auto;
    }

    .email-editor:focus {
        border-color: #FF754C;
        box-shadow: 0 0 0 3px rgba(255, 117, 76, 0.1);
    }

    .email-editor:empty::before {
        content: attr(placeholder);
        color: #9CA3AF;
        pointer-events: none;
    }

    .editor-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        font-size: 0.75rem;
        color: #7A858E;
    }

    .character-count {
        margin-left: auto;
    }

    .popup-actions {
        padding: 20px 24px;
        border-top: 1px solid #E8EBEE;
        background: #FAFBFC;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
    }

    .action-group {
        display: flex;
        gap: 12px;
    }

    .btn-primary,
    .btn-secondary,
    .btn-cancel {
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

    .btn-primary:hover:not(:disabled) {
        background: #E5663F;
    }

    .btn-primary:disabled {
        background: #D1D5DB;
        color: #9CA3AF;
        cursor: not-allowed;
    }

    .btn-secondary {
        background: #F8F9FA;
        color: #384144;
        border: 1px solid #D1D5DB;
    }

    .btn-secondary:hover:not(:disabled) {
        background: #E8EBEE;
    }

    .btn-cancel {
        background: #F8F9FA;
        color: #7A858E;
        border: 1px solid #D1D5DB;
    }

    .btn-cancel:hover {
        background: #E8EBEE;
        color: #384144;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .popup-container {
            width: 95%;
            max-height: 95vh;
        }

        .form-row {
            grid-template-columns: 1fr;
        }

        .popup-actions {
            flex-direction: column;
            align-items: stretch;
        }

        .action-group {
            justify-content: stretch;
        }

        .btn-primary,
        .btn-secondary,
        .btn-cancel {
            flex: 1;
            justify-content: center;
        }
    }

    /* Icon placeholders - replace with actual icons */
    .icon-close::before { content: "✕"; }
    .icon-bold::before { content: "B"; font-weight: bold; }
    .icon-italic::before { content: "I"; font-style: italic; }
    .icon-underline::before { content: "U"; text-decoration: underline; }
    .icon-template::before { content: "📝"; }
    .icon-signature::before { content: "✍"; }
    .icon-save::before { content: "💾"; }
    .icon-send::before { content: "📤"; }
    .icon-loading::before { content: "⏳"; }
</style> 