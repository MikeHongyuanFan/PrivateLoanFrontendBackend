import { ref } from 'vue'
import axios from 'axios'

export function useEmailApi() {
    const loading = ref(false)
    const error = ref(null)

    // Get the API base URL from environment or default
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

    // Create axios instance with default config
    const apiClient = axios.create({
        baseURL: API_BASE_URL,
        headers: {
            'Content-Type': 'application/json',
        }
    })

    // Add auth token to requests if available
    apiClient.interceptors.request.use((config) => {
        // Get user info from localStorage
        let userInfo = localStorage.getItem('userInfo')
        if (userInfo) {
            userInfo = JSON.parse(userInfo)
            config.headers.Authorization = `Bearer ${userInfo.access}`
        }
        return config
    })

    // Handle API responses and errors
    apiClient.interceptors.response.use(
        (response) => response,
        (error) => {
            console.error('API Error:', error)
            // If unauthorized, redirect to login
            if (error.response?.status === 401) {
                console.log('Unauthorized access, redirecting to login')
                // Import router dynamically to avoid circular dependency
                import('@/router').then(({ default: router }) => {
                    router.push('/login')
                })
            }
            throw error
        }
    )

    /**
     * Fetch reminders/emails from the API
     * @param {Object} params - Query parameters for filtering
     * @returns {Promise} API response with emails/reminders
     */
    const fetchReminders = async (params = {}) => {
        try {
            loading.value = true
            error.value = null
            
            const response = await apiClient.get('/api/reminders/', { params })
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Failed to fetch emails'
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * Create a new reminder/email
     * @param {Object} reminderData - Email/reminder data
     * @returns {Promise} API response
     */
    const createReminder = async (reminderData) => {
        try {
            loading.value = true
            error.value = null
            
            const response = await apiClient.post('/api/reminders/', reminderData)
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Failed to send email'
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * Get a specific reminder/email by ID
     * @param {number} id - Reminder ID
     * @returns {Promise} API response
     */
    const getReminder = async (id) => {
        try {
            loading.value = true
            error.value = null
            
            const response = await apiClient.get(`/api/reminders/${id}/`)
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Failed to fetch email'
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * Update a reminder/email
     * @param {number} id - Reminder ID
     * @param {Object} reminderData - Updated email data
     * @returns {Promise} API response
     */
    const updateReminder = async (id, reminderData) => {
        try {
            loading.value = true
            error.value = null
            
            const response = await apiClient.patch(`/api/reminders/${id}/`, reminderData)
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Failed to update email'
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * Delete a reminder/email
     * @param {number} id - Reminder ID
     * @returns {Promise} API response
     */
    const deleteReminder = async (id) => {
        try {
            loading.value = true
            error.value = null
            
            const response = await apiClient.delete(`/api/reminders/${id}/`)
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Failed to delete email'
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * Preview email template
     * @returns {Promise} API response with email preview
     */
    const previewEmail = async () => {
        try {
            loading.value = true
            error.value = null
            
            const response = await apiClient.get('/api/users/email-preview/')
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Failed to preview email'
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * Download email logs
     * @returns {Promise} API response with download data
     */
    const downloadEmailLogs = async () => {
        try {
            loading.value = true
            error.value = null
            
            const response = await apiClient.get('/api/users/download-email-logs/')
            return response.data
        } catch (err) {
            error.value = err.response?.data?.detail || 'Failed to download email logs'
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * Send email with specific recipient type and data
     * @param {Object} emailData - Email configuration
     * @returns {Promise} API response
     */
    const sendEmail = async (emailData) => {
        const reminderPayload = {
            recipient_type: emailData.recipient_type || 'custom',
            recipient_email: emailData.recipient_email,
            subject: emailData.subject,
            email_body: emailData.email_body,
            send_datetime: emailData.send_datetime || new Date().toISOString(),
            related_application: emailData.related_application || null,
            related_borrower: emailData.related_borrower || null,
            send_as_user: emailData.send_as_user || null,
            reply_to_user: emailData.reply_to_user || null
        }

        return await createReminder(reminderPayload)
    }

    return {
        // State
        loading,
        error,

        // Methods
        fetchReminders,
        createReminder,
        getReminder,
        updateReminder,
        deleteReminder,
        previewEmail,
        downloadEmailLogs,
        sendEmail
    }
} 