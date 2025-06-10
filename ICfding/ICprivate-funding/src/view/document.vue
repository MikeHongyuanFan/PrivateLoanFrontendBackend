<template>
    <div class="doc">
        <div class="filters">
            <div class="left">
                <div class="filter">
                    <h1>Search By Description</h1>
                    <el-input v-model="searchedApplication" style="width: 200px" placeholder="Search By Description" />
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
                v-loading="loading"
                :data="paginatedData"
                style="width: 100%"
                :default-sort="{ prop: 'id', order: 'ascending' }"
                :cell-style="{ padding: '10px 0' }"
                @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection" align="center" width="50" />
                <el-table-column prop="title" label="Title" sortable width="150" />
                <el-table-column prop="document_type_display" label="Type" width="150" />
                <el-table-column prop="application" label="Application" width="130" />
                <el-table-column prop="created_by_name" label="Uploaded By" min-width="150" />                
                <el-table-column prop="created_at" label="Uploaded At" width="200">
                    <template #default="{ row }">
                        {{ new Date(row.created_at).toLocaleString() }}
                    </template>
                </el-table-column>
                <el-table-column prop="version" label="Version" width="90" />
                <el-table-column label="Action" align="center" width="200">
                    <template #default="{ row }">
                        <div class="actions">
                            <el-tooltip content="View" placement="top">
                                <div class="view" @click="handleView(row)">
                                    <el-icon :size="20" color="#2984DE"><View /></el-icon>
                                </div>
                            </el-tooltip>
                            <el-tooltip content="Download" placement="top">
                                <div class="download" @click="handleDownload(row)">
                                    <el-icon :size="20" color="#7A858E"><Download /></el-icon>
                                </div>
                            </el-tooltip>
                            <el-tooltip content="New Version" placement="top">
                                <div class="upload" @click="handleUpload(row)">
                                    <el-icon :size="20" color="#1AAD0A"><Upload /></el-icon>
                                </div>
                            </el-tooltip>
                            <el-tooltip content="Edit" placement="top">
                                <div class="edit" @click="openEditDialog(row)">
                                    <el-icon :size="20" color="#E6A23C"><Edit /></el-icon>
                                </div>
                            </el-tooltip>
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
                <el-form-item label="Application ID" prop="application">
                    <el-input v-model="documentForm.application" type="number" />
                </el-form-item>
                <el-form-item label="Borrower ID" prop="borrower">
                    <el-input v-model="documentForm.borrower" type="number" />
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
                <el-form-item label="Application ID" prop="application">
                    <el-input v-model="documentForm.application" type="number" />
                </el-form-item>
                <el-form-item label="Borrower ID" prop="borrower">
                    <el-input v-model="documentForm.borrower" type="number" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="editDialogVisible = false">Cancel</el-button>
                    <el-button type="primary" @click="handleEdit(editFormRef)">Save</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted, watch } from 'vue';
    import { useRouter } from 'vue-router';
    import { ElMessage, ElMessageBox } from 'element-plus';
    import { View, Download, Upload, Edit } from '@element-plus/icons-vue';
    import { api } from '@/api';

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
    
    const searchedApplication = ref("")
    const selectedDoc = ref("")
    const loading = ref(false)
    const uploadDialogVisible = ref(false)
    const editDialogVisible = ref(false)
    const currentDocument = ref(null)
    const docs = ref([])
    
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
            if (searchedApplication.value) {
                params.search = searchedApplication.value;
            }
            
            if (selectedDoc.value) {
                params.document_type = selectedDoc.value;
            }
            
            const [error, data] = await api.getDocuments(params);
            
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
    
    // Watch for filter changes
    watch([searchedApplication, selectedDoc], () => {
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
    const handleView = (row) => {
        if (row && row.file_url) {
            window.open(row.file_url, '_blank');
        } else {
            ElMessage.warning('Document URL not available');
        }
    };

    // Download document
    const handleDownload = async (row) => {
        try {
            loading.value = true
            const [error, data] = await api.downloadDocument(row.id);
            
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
                        const [error] = await api.createDocumentVersion(row.id, formData);
                        
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
                api.deleteDocument(item.id)
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

            const [error] = await api.createDocument(formData);
            
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

            const [error] = await api.updateDocument(currentDocument.value.id, formData);
            
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
        padding-left: 18px;
        display: flex;
        flex-direction: row;
        gap: 25px;
    }
    .table_buttons {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
    }
    :deep(.el-table .el-table__cell) {
        padding: 0;
    }
    :deep(.el-table tbody .cell) {
        height: auto;
        padding: 0 5px;
        color: #272727;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 400;
        line-height: 140%;
    }
    :deep(.el-table th.el-table__cell) {
        background: #F8F8F8;
    }
    :deep(.el-table thead .cell) {
        padding: 10px 5px;
        color: #272727;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 140%;
    }
    :deep(.el-checkbox) {
        --el-checkbox-input-border: 1.5px solid #B2B3BD;
        --el-checkbox-checked-input-border-color: #2984DE;
        --el-checkbox-checked-bg-color: #2984DE;
        --el-checkbox-input-border-color-hover: #2984DE;
    }
    :deep(.el-pagination) {
        --el-pagination-button-bg-color: #FFF;
        --el-pagination-button-disabled-bg-color: #FFF;
    }
    :deep(.el-pager li) {
        background: #FFF;
        color: rgba(0, 0, 0, 0.20);
        border-radius: 4px;
        border: 1.5px solid rgba(64, 64, 64, 0.16);
        font-weight: 500;
    }
    :deep(.el-pager li):hover {
        border: 1.5px solid #2984DE;
    }
    :deep(.el-pagination button) {
        height: 32px;
        padding: 0 15px;
        gap: 5px;
        border-radius: 4px;
        color: #1F1F1F;
        border: 1.5px solid rgba(64, 64, 64, 0.16);
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 140%;
    }
    :deep(.el-pagination button):hover {
        border: 1.5px solid #2984DE;
    }
    :deep(.el-pagination .btn-prev::after) {
        content: "Previous";
    }
    :deep(.el-pagination .btn-next::before) {
        content: "Next";
    }
    :deep(.el-pagination.is-background .btn-prev:disabled) {
        background: #FFF;
    }
    :deep(.el-pagination.is-background .btn-next:disabled) {
        background: #FFF;
    }
    :deep(.el-pagination.is-background .el-pager li.is-active) {
        background: rgba(114, 114, 114, 0.08);
        color: #625E5E;
        font-weight: 500;
    }
    :deep(.el-dialog) {
        border-radius: 8px;
    }
    :deep(.el-dialog__header) {
        margin: 0;
        padding: 20px;
        border-bottom: 1px solid #EBEEF5;
    }
    :deep(.el-dialog__body) {
        padding: 20px;
    }
    :deep(.el-dialog__footer) {
        padding: 20px;
        border-top: 1px solid #EBEEF5;
    }
    :deep(.el-upload) {
        width: 100%;
    }
    :deep(.el-upload-dragger) {
        width: 100%;
        height: 120px;
    }
</style>