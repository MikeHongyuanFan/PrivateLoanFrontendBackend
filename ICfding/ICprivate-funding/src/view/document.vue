<template>
    <div class="doc">
        <div class="filters">
            <div class="left">
                <div class="filter">
                    <h1>Search Documents</h1>
                    <el-input v-model="searchQuery" style="width: 200px" placeholder="Search documents..." />
                </div>
                <div class="filter">
                    <h1>Application Search</h1>
                    <el-input 
                        v-model="applicationSearch" 
                        style="width: 200px" 
                        placeholder="Search by App ID/Reference" 
                    />
                </div>
                <div class="filter">
                    <h1>Borrower Search</h1>
                    <el-input 
                        v-model="borrowerSearch" 
                        style="width: 200px" 
                        placeholder="Search by name/address" 
                    />
                </div>
                <div class="filter">
                    <h1>Document Type</h1>
                    <el-select v-model="selectedDoc" placeholder="Select Document Type" style="width: 200px">
                        <el-option
                            v-for="item in docTypes"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </div>
            </div>
            <el-button type="primary" @click="uploadDialogVisible = true">Upload Document</el-button>
        </div>

        <div class="container">
            <el-table
                ref="docListTable"
                :data="paginatedData"
                style="width: 100%"
                @selection-change="handleSelectionChange"
                v-loading="loading"
            >
                <el-table-column type="selection" width="55" />
                <el-table-column prop="title" label="Title" />
                <el-table-column prop="description" label="Description" />
                <el-table-column prop="document_type" label="Type" />
                <el-table-column prop="created_at" label="Created At" />
                <el-table-column label="Actions" width="200">
                    <template #default="scope">
                        <div class="actions">
                            <div class="view" @click="handleView(scope.row)">
                                <el-icon><View /></el-icon>
                            </div>
                            <div class="download" @click="handleDownload(scope.row)">
                                <el-icon><Download /></el-icon>
                            </div>
                            <div class="upload" @click="handleUpload(scope.row)">
                                <el-icon><Upload /></el-icon>
                            </div>
                            <div class="edit" @click="openEditDialog(scope.row)">
                                <el-icon><Edit /></el-icon>
                            </div>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
            <div class="multiple">
                <div class="select">
                    <el-checkbox
                        v-model="selectAll"
                        :indeterminate="isSelected"
                        @change="handleCheckAllChange"
                    />
                    <div class="table_buttons">
                        <el-button type="danger" @click="deleteSelect" :disabled="!selectedItem.length">
                            Delete Selected
                        </el-button>
                    </div>
                </div>
                <el-pagination
                    layout="prev, pager, next"
                    background
                    :total="docs.length"
                    :page-size="pageSize"
                    :current-page="currentPage"
                    @current-change="handlePageChange"
                />
            </div>
        </div>

        <!-- Upload Dialog -->
        <el-dialog
            v-model="uploadDialogVisible"
            title="Upload Document"
            width="500px"
        >
            <el-form
                ref="uploadFormRef"
                :model="documentForm"
                :rules="rules"
                label-width="120px"
            >
                <el-form-item label="Title" prop="title">
                    <el-input v-model="documentForm.title" />
                </el-form-item>
                <el-form-item label="Description" prop="description">
                    <el-input v-model="documentForm.description" type="textarea" />
                </el-form-item>
                <el-form-item label="Document Type" prop="document_type">
                    <el-select v-model="documentForm.document_type" placeholder="Select type">
                        <el-option
                            v-for="item in docTypes"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="File" prop="file">
                    <el-upload
                        class="upload-demo"
                        action="#"
                        :auto-upload="false"
                        :limit="1"
                        :on-change="handleFileChange"
                        :on-exceed="() => ElMessage.warning('Only one file can be uploaded')"
                    >
                        <template #trigger>
                            <el-button type="primary">Select File</el-button>
                        </template>
                        <template #tip>
                            <div style="color: #606266; font-size: 12px; margin-top: 7px;">
                                Please select a file to upload
                            </div>
                        </template>
                    </el-upload>
                </el-form-item>
                <el-form-item label="Application" prop="application">
                    <el-select 
                        v-model="documentForm.application" 
                        placeholder="Select application"
                        filterable
                        clearable
                    >
                        <el-option
                            v-for="app in applications"
                            :key="app.id"
                            :label="'App #' + app.id + (app.reference ? ' - ' + app.reference : '')"
                            :value="app.id"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="Borrower" prop="borrower">
                    <el-select 
                        v-model="documentForm.borrower" 
                        placeholder="Select borrower"
                        filterable
                        clearable
                    >
                        <el-option
                            v-for="borrower in borrowers"
                            :key="borrower.id"
                            :label="borrower.first_name + ' ' + borrower.last_name"
                            :value="borrower.id"
                        />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="uploadDialogVisible = false">Cancel</el-button>
                    <el-button type="primary" @click="handleCreate(uploadFormRef)">Upload</el-button>
                </span>
            </template>
        </el-dialog>

        <!-- Edit Dialog -->
        <el-dialog
            v-model="editDialogVisible"
            title="Edit Document"
            width="500px"
        >
            <el-form
                ref="editFormRef"
                :model="documentForm"
                :rules="rules"
                label-width="120px"
            >
                <el-form-item label="Title" prop="title">
                    <el-input v-model="documentForm.title" />
                </el-form-item>
                <el-form-item label="Description" prop="description">
                    <el-input v-model="documentForm.description" type="textarea" />
                </el-form-item>
                <el-form-item label="Document Type" prop="document_type">
                    <el-select v-model="documentForm.document_type" placeholder="Select type">
                        <el-option
                            v-for="item in docTypes"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="File" prop="file">
                    <el-upload
                        class="upload-demo"
                        action="#"
                        :auto-upload="false"
                        :limit="1"
                        :on-change="handleFileChange"
                        :on-exceed="() => ElMessage.warning('Only one file can be uploaded')"
                    >
                        <template #trigger>
                            <el-button type="primary">Select File</el-button>
                        </template>
                        <template #tip>
                            <div style="color: #606266; font-size: 12px; margin-top: 7px;">
                                Please select a file to upload
                            </div>
                        </template>
                    </el-upload>
                </el-form-item>
                <el-form-item label="Application" prop="application">
                    <el-select 
                        v-model="documentForm.application" 
                        placeholder="Select application"
                        filterable
                        clearable
                    >
                        <el-option
                            v-for="app in applications"
                            :key="app.id"
                            :label="'App #' + app.id + (app.reference ? ' - ' + app.reference : '')"
                            :value="app.id"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="Borrower" prop="borrower">
                    <el-select 
                        v-model="documentForm.borrower" 
                        placeholder="Select borrower"
                        filterable
                        clearable
                    >
                        <el-option
                            v-for="borrower in borrowers"
                            :key="borrower.id"
                            :label="borrower.first_name + ' ' + borrower.last_name"
                            :value="borrower.id"
                        />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="editDialogVisible = false">Cancel</el-button>
                    <el-button type="primary" @click="handleEdit(editFormRef)">Update</el-button>
                </span>
            </template>
        </el-dialog>

        <!-- Document Preview Dialog -->
        <el-dialog
            v-model="previewDialogVisible"
            title="Document Preview"
            width="80%"
            :fullscreen="isFullscreen"
            class="document-preview-dialog"
            @close="closePreviewDialog"
        >
            <div class="preview-header">
                <div class="document-info">
                    <h3>{{ previewDocument?.title || previewDocument?.file_name }}</h3>
                    <p v-if="previewDocument?.description">{{ previewDocument.description }}</p>
                    <p class="file-meta">
                        Type: {{ previewDocument?.document_type_display }} | 
                        Size: {{ formatFileSize(previewDocument?.file_size) }} | 
                        Uploaded: {{ formatDate(previewDocument?.created_at) }}
                    </p>
                </div>
                <div class="preview-actions">
                    <el-button @click="toggleFullscreen" :icon="isFullscreen ? 'Close' : 'FullScreen'">
                        {{ isFullscreen ? 'Exit Fullscreen' : 'Fullscreen' }}
                    </el-button>
                    <el-button type="primary" @click="downloadPreviewDocument" :icon="'Download'">
                        Download
                    </el-button>
                </div>
            </div>
            
            <div class="preview-content" v-loading="previewLoading">
                <!-- PDF Preview -->
                <iframe 
                    v-if="previewUrl && isPdfFile" 
                    :src="previewUrl" 
                    class="pdf-preview"
                    frameborder="0"
                ></iframe>
                
                <!-- Image Preview -->
                <img 
                    v-else-if="previewUrl && isImageFile" 
                    :src="previewUrl" 
                    class="image-preview"
                    alt="Document preview"
                />
                
                <!-- Unsupported File Type -->
                <div v-else-if="!previewLoading" class="unsupported-file">
                    <i class="el-icon-document"></i>
                    <h4>Preview Not Available</h4>
                    <p>This file type cannot be previewed in the browser.</p>
                    <p>File type: {{ getFileExtension(previewDocument?.file_name) }}</p>
                    <el-button type="primary" @click="downloadPreviewDocument">
                        Download File
                    </el-button>
                </div>
            </div>
        </el-dialog>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted, watch } from 'vue';
    import { useRouter } from 'vue-router';
    import { ElMessage, ElMessageBox } from 'element-plus';
    import { View, Download, Upload, Edit, InfoFilled } from '@element-plus/icons-vue';
    import { documentsApi } from '@/api/documents';

    const router = useRouter()

    const docTypes = ref([
        { value: 'application_form', label: 'Application Form' },
        { value: 'indicative_letter', label: 'Indicative Letter' },
        { value: 'formal_approval', label: 'Formal Approval' },
        { value: 'valuation_report', label: 'Valuation Report' },
        { value: 'qs_report', label: 'Quantity Surveyor Report' },
        { value: 'id_verification', label: 'ID Verification' },
        { value: 'bank_statement', label: 'Bank Statement' },
        { value: 'payslip', label: 'Payslip' },
        { value: 'tax_return', label: 'Tax Return' },
        { value: 'contract', label: 'Contract' },
        { value: 'other', label: 'Other' }
    ])
    
    const searchQuery = ref("")
    const applicationSearch = ref("")
    const borrowerSearch = ref("")
    const selectedDoc = ref("")
    const loading = ref(false)
    const uploadDialogVisible = ref(false)
    const editDialogVisible = ref(false)
    const currentDocument = ref(null)
    const docs = ref([])
    const applications = ref([])
    const borrowers = ref([])
    
    // Form data for document upload/edit
    const documentForm = ref({
        title: '',
        description: '',
        document_type: '',
        file: null,
        application: null,
        borrower: null
    })
    
    // Rules for form validation
    const rules = {
        title: [{ required: true, message: 'Please input title', trigger: 'blur' }],
        document_type: [{ required: true, message: 'Please select document type', trigger: 'change' }],
        file: [{ required: true, message: 'Please upload a file', trigger: 'change' }]
    }
    
    // Error handling
    const handleError = (error) => {
        console.error('API Error:', error);
        if (error.response) {
            ElMessage.error(error.response.data?.message || error.response.data?.detail || 'An error occurred');
        } else {
            ElMessage.error('An error occurred while communicating with the server');
        }
    }
    
    // Load documents from API
    const loadDocuments = async () => {
        try {
            loading.value = true
            
            // Build query parameters object
            const params = {};
            
            // Only add parameters if they have values
            if (searchQuery.value) {
                params.search = searchQuery.value;
            }
            
            if (applicationSearch.value) {
                params.application_search = applicationSearch.value;
            }
            
            if (borrowerSearch.value) {
                params.borrower_search = borrowerSearch.value;
            }
            
            if (selectedDoc.value) {
                params.document_type = selectedDoc.value;
            }
            
            const [error, data] = await documentsApi.getDocuments(params);
            
            if (error) {
                ElMessage.error('Failed to fetch documents');
                console.error('Error fetching documents:', error);
                return;
            }
            
            if (data && data.results) {
                docs.value = data.results;
                console.log('Documents loaded:', docs.value);
            } else {
                docs.value = [];
                console.warn('No documents found or invalid response format');
            }
        } catch (error) {
            handleError(error)
        } finally {
            loading.value = false
        }
    }

    // Load applications and borrowers
    const loadApplications = async () => {
        try {
            const [error, data] = await documentsApi.getApplications();
            if (error) {
                ElMessage.error('Failed to fetch applications');
                console.error('Error fetching applications:', error);
                return;
            }
            if (data && data.results) {
                applications.value = data.results;
            }
        } catch (error) {
            handleError(error);
        }
    }

    const loadBorrowers = async () => {
        try {
            const [error, data] = await documentsApi.getBorrowers();
            if (error) {
                ElMessage.error('Failed to fetch borrowers');
                console.error('Error fetching borrowers:', error);
                return;
            }
            if (data && data.results) {
                borrowers.value = data.results;
            }
        } catch (error) {
            handleError(error);
        }
    }

    // Load data when dialog opens
    watch(uploadDialogVisible, (newVal) => {
        if (newVal) {
            loadApplications();
            loadBorrowers();
        }
    });

    watch(editDialogVisible, (newVal) => {
        if (newVal) {
            loadApplications();
            loadBorrowers();
        }
    });
    
    // Watch for filter changes
    watch([searchQuery, applicationSearch, borrowerSearch, selectedDoc], () => {
        loadDocuments()
    })

    const pageSize = 10
    const currentPage = ref(1)
    const uploadFormRef = ref(null);
    const editFormRef = ref(null);
    const docListTable = ref(null);

    const selectedItem = ref([]);
    const selectAll = ref(false);
    const isSelected = ref(false);

    // Preview-related reactive data
    const previewDialogVisible = ref(false);
    const previewDocument = ref(null);
    const previewUrl = ref(null);
    const previewLoading = ref(false);
    const isFullscreen = ref(false);

    // Computed properties for preview
    const isPdfFile = computed(() => {
        if (!previewDocument.value?.file_name) return false;
        const extension = getFileExtension(previewDocument.value.file_name);
        return extension === 'pdf';
    });

    const isImageFile = computed(() => {
        if (!previewDocument.value?.file_name) return false;
        const extension = getFileExtension(previewDocument.value.file_name);
        return ['jpg', 'jpeg', 'png', 'gif'].includes(extension);
    });

    // Utility functions
    const getFileExtension = (filename) => {
        if (!filename) return '';
        return filename.split('.').pop().toLowerCase();
    };

    const formatFileSize = (bytes) => {
        if (!bytes) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const formatDate = (dateString) => {
        if (!dateString) return '';
        return new Date(dateString).toLocaleDateString();
    };

    const paginatedData = computed(() => {
        const start = (currentPage.value - 1) * pageSize;
        return docs.value.slice(start, start + pageSize);
    });

    const handleSelectionChange = (row) => {
        selectedItem.value = row;
        selectAll.value = row.length === docs.value.length;
        isSelected.value = row.length > 0 && row.length < docs.value.length;
    };

    const handleCheckAllChange = (row) => {
        if (row) {
            docListTable.value.toggleAllSelection();
        } else {
            docListTable.value.clearSelection();
        }
        isSelected.value = false;
    };
    
    // View document
    const handleView = async (row) => {
        try {
            previewLoading.value = true;
            previewDocument.value = row;
            previewDialogVisible.value = true;
            
            // Get file extension to determine if preview is supported
            const fileExtension = getFileExtension(row.file_name);
            const previewableTypes = ['pdf', 'jpg', 'jpeg', 'png', 'gif'];
            
            if (previewableTypes.includes(fileExtension)) {
                // Use preview endpoint for supported file types
                const [error, data] = await documentsApi.previewDocument(row.id);
                
                if (error) {
                    ElMessage.error('Failed to preview document');
                    console.error('Error previewing document:', error);
                    return;
                }
                
                // Create blob URL for preview
                const blob = new Blob([data], { 
                    type: fileExtension === 'pdf' ? 'application/pdf' : `image/${fileExtension}` 
                });
                previewUrl.value = window.URL.createObjectURL(blob);
            } else {
                // For unsupported file types, clear the URL
                previewUrl.value = null;
            }
        } catch (error) {
            console.error('Error viewing document:', error);
            ElMessage.error('Failed to view document');
        } finally {
            previewLoading.value = false;
        }
    };

    // Download document
    const handleDownload = async (row) => {
        try {
            loading.value = true
            const [error, data] = await documentsApi.downloadDocument(row.id);
            
            if (error) {
                ElMessage.error('Failed to download document');
                console.error('Error downloading document:', error);
                return;
            }
            
            // Create download link
            const url = window.URL.createObjectURL(new Blob([data]))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', row.file_name)
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            window.URL.revokeObjectURL(url)
        } catch (error) {
            handleError(error)
        } finally {
            loading.value = false
        }
    }

    // Preview dialog methods
    const toggleFullscreen = () => {
        isFullscreen.value = !isFullscreen.value;
    };

    const downloadPreviewDocument = async () => {
        if (previewDocument.value) {
            await handleDownload(previewDocument.value);
        }
    };

    const closePreviewDialog = () => {
        previewDialogVisible.value = false;
        previewDocument.value = null;
        if (previewUrl.value) {
            window.URL.revokeObjectURL(previewUrl.value);
            previewUrl.value = null;
        }
        isFullscreen.value = false;
    };

    // Upload new version
    const handleUpload = async (row) => {
        try {
            const input = document.createElement('input');
            input.type = 'file';
            input.onchange = async (e) => {
                const file = e.target.files[0];
                if (file) {
                    loading.value = true;
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('document_type', row.document_type);
                    formData.append('title', row.title);
                    if (row.description) formData.append('description', row.description);
                    if (row.application) formData.append('application', row.application);
                    if (row.borrower) formData.append('borrower', row.borrower);

                    try {
                        const [error] = await documentsApi.createDocumentVersion(row.id, formData);
                        
                        if (error) {
                            ElMessage.error('Failed to upload new version');
                            console.error('Error uploading new version:', error);
                            return;
                        }
                        
                        ElMessage.success('New version uploaded successfully');
                        loadDocuments();
                    } catch (error) {
                        handleError(error);
                    } finally {
                        loading.value = false;
                    }
                }
            };
            input.click();
        } catch (error) {
            handleError(error);
        }
    }

    // Delete selected documents
    const deleteSelect = async () => {
        try {
            if (!selectedItem.value.length) {
                ElMessage.warning('Please select documents to delete')
                return
            }

            await ElMessageBox.confirm(
                'Are you sure you want to delete the selected documents?',
                'Warning',
                {
                    confirmButtonText: 'OK',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }
            )

            loading.value = true
            const deletePromises = selectedItem.value.map(item => 
                documentsApi.deleteDocument(item.id)
            )
            await Promise.all(deletePromises)
            
            ElMessage.success('Documents deleted successfully')
            selectedItem.value = []
            loadDocuments()
        } catch (error) {
            if (error !== 'cancel') {
                handleError(error)
            }
        } finally {
            loading.value = false
        }
    }

    // Handle page change
    const handlePageChange = (page) => {
        currentPage.value = page
    }

    // Create new document
    const handleCreate = async (formEl) => {
        if (!formEl) return;
        
        try {
            await formEl.validate();
            
            if (!documentForm.value.file) {
                ElMessage.error('Please select a file to upload');
                return;
            }
            
            loading.value = true;
            
            const formData = new FormData();
            Object.keys(documentForm.value).forEach(key => {
                if (documentForm.value[key] !== null) {
                    formData.append(key, documentForm.value[key]);
                }
            });

            const [error] = await documentsApi.createDocument(formData);
            
            if (error) {
                ElMessage.error('Failed to create document');
                console.error('Error creating document:', error);
                return;
            }
            
            ElMessage.success('Document created successfully');
            uploadDialogVisible.value = false;
            loadDocuments();
            documentForm.value = {
                title: '',
                description: '',
                document_type: '',
                file: null,
                application: null,
                borrower: null
            };
        } catch (error) {
            handleError(error);
        } finally {
            loading.value = false;
        }
    }

    // Edit document
    const handleEdit = async (formEl) => {
        if (!formEl) return;
        
        try {
            await formEl.validate();
            loading.value = true;
            
            const formData = new FormData();
            Object.keys(documentForm.value).forEach(key => {
                if (documentForm.value[key] !== null && key !== 'file') {
                    formData.append(key, documentForm.value[key]);
                }
            });
            
            // Only append file if it's been changed
            if (documentForm.value.file) {
                formData.append('file', documentForm.value.file);
            }

            const [error] = await documentsApi.updateDocument(currentDocument.value.id, formData);
            
            if (error) {
                ElMessage.error('Failed to update document');
                console.error('Error updating document:', error);
                return;
            }
            
            ElMessage.success('Document updated successfully');
            editDialogVisible.value = false;
            loadDocuments();
        } catch (error) {
            handleError(error);
        } finally {
            loading.value = false;
        }
    }

    // Open edit dialog
    const openEditDialog = (row) => {
        currentDocument.value = row;
        documentForm.value = {
            title: row.title,
            description: row.description,
            document_type: row.document_type,
            file: null, // Don't set the file here, only if user uploads a new one
            application: row.application,
            borrower: row.borrower
        };
        editDialogVisible.value = true;
    }

    // Handle file change
    const handleFileChange = (file) => {
        if (file && file.raw) {
            documentForm.value.file = file.raw;
        }
    }

    // Load initial data
    onMounted(() => {
        loadDocuments()
    })
</script>

<style scoped>
    .doc {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .filters {
        padding: 20px;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: end;
        border-radius: 6px;
        background: #FFF;
    }
    .left {
        display: flex;
        flex-direction: row;
        justify-content: start;
        align-items: end;
        gap: 20px;
    }
    .filter {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    h1 {
        color: #272727;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 600;
        line-height: 19px;
        margin: 0;
    }
    .container {
        padding: 20px;
        border-radius: 3px;
        background: #FFF;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .actions {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        gap: 5px;
    }
    .view, .download, .upload, .edit {
        padding: 5px;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .view {
        border: 1.5px solid #2984DE;
    }
    .download {
        border: 1.5px solid #7A858E;
    }
    .upload {
        border: 1.5px solid #1AAD0A;
    }
    .edit {
        border: 1.5px solid #E6A23C;
    }
    .view:hover, .download:hover, .upload:hover, .edit:hover {
        opacity: 0.8;
        transform: scale(1.05);
    }
    .multiple {
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .select {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
    }
    .table_buttons {
        display: flex;
        flex-direction: row;
        gap: 10px;
    }

    /* Document Preview Dialog Styles */
    .document-preview-dialog {
        .preview-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #E8EBEE;
        }

        .document-info {
            flex: 1;
            margin-right: 20px;

            h3 {
                margin: 0 0 8px 0;
                color: #384144;
                font-size: 1.25rem;
                font-weight: 600;
            }

            p {
                margin: 4px 0;
                color: #7A858E;
                font-size: 0.875rem;
            }

            .file-meta {
                font-size: 0.75rem;
                color: #9CA3AF;
                margin-top: 8px;
            }
        }

        .preview-actions {
            display: flex;
            gap: 10px;
            flex-shrink: 0;
        }

        .preview-content {
            min-height: 400px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #FAFBFC;
            border-radius: 6px;
            overflow: hidden;
        }

        .pdf-preview {
            width: 100%;
            height: 600px;
            border: none;
        }

        .image-preview {
            max-width: 100%;
            max-height: 600px;
            object-fit: contain;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .unsupported-file {
            text-align: center;
            padding: 40px;
            color: #7A858E;

            i {
                font-size: 3rem;
                margin-bottom: 16px;
                display: block;
            }

            h4 {
                margin: 16px 0 8px 0;
                color: #384144;
                font-size: 1.125rem;
            }

            p {
                margin: 8px 0;
                font-size: 0.875rem;
            }
        }
    }

    /* Fullscreen styles */
    .el-dialog.is-fullscreen {
        .preview-content {
            height: calc(100vh - 200px);
        }

        .pdf-preview {
            height: 100%;
        }

        .image-preview {
            max-height: 100%;
        }
    }
</style>