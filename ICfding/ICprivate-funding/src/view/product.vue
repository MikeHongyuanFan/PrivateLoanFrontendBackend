<template>
    <div class="product">
        <!-- Search and Filter Section -->
        <div class="filters">
            <div class="left">
                <div class="filter">
                    <h1>Search By Name</h1>
                    <el-input 
                        v-model="searchQuery" 
                        style="width: 240px" 
                        placeholder="Search products by name"
                        @input="handleSearch" 
                    />
                </div>
                <el-button type="primary" @click="handleSearch">Search</el-button>
                <el-button @click="clearSearch">Clear</el-button>
            </div>
            <el-button type="primary" @click="showCreateDialog = true">Create Product</el-button>
        </div>

        <!-- Products Table -->
        <div class="container">
            <el-table 
                :data="products" 
                style="width: 100%"
                v-loading="loading"
            >
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="name" label="Name" />
                <el-table-column prop="created_at" label="Created At" width="180">
                    <template #default="scope">
                        {{ formatDate(scope.row.created_at) }}
                    </template>
                </el-table-column>
                <el-table-column label="Actions" width="200">
                    <template #default="scope">
                        <el-button-group style="margin: 10px 0;">
                            <el-button 
                                size="small" 
                                @click="handleEdit(scope.row)"
                            >
                                Edit
                            </el-button>
                            <el-button 
                                size="small" 
                                type="danger" 
                                @click="handleDelete(scope.row)"
                            >
                                Delete
                            </el-button>
                        </el-button-group>
                    </template>
                </el-table-column>
            </el-table>

            <div class="pagination">
                <el-pagination
                    v-model:current-page="currentPage"
                    v-model:page-size="pageSize"
                    :total="total"
                    :page-sizes="[10, 20, 50, 100]"
                    layout="total, sizes, prev, pager, next"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                />
            </div>
        </div>

        <!-- Create/Edit Dialog -->
        <el-dialog
            :title="dialogMode === 'create' ? 'Create Product' : 'Edit Product'"
            v-model="showDialog"
            width="500px"
        >
            <el-form
                ref="productForm"
                :model="formData"
                :rules="rules"
                label-width="120px"
            >
                <el-form-item 
                    label="Name" 
                    prop="name"
                    :rules="[
                        { required: true, message: 'Name is required' },
                        { max: 255, message: 'Name cannot exceed 255 characters' }
                    ]"
                >
                    <el-input v-model="formData.name" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="showDialog = false">Cancel</el-button>
                    <el-button type="primary" @click="handleSubmit">
                        {{ dialogMode === 'create' ? 'Create' : 'Update' }}
                    </el-button>
                </span>
            </template>
        </el-dialog>

        <!-- Delete Confirmation Dialog -->
        <el-dialog
            title="Confirm Delete"
            v-model="showDeleteDialog"
            width="400px"
        >
            <p>Are you sure you want to delete this product?</p>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="showDeleteDialog = false">Cancel</el-button>
                    <el-button type="danger" @click="confirmDelete">Delete</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, onMounted, reactive, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { api } from '@/api';

// State
const products = ref([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);
const searchQuery = ref('');
const showDialog = ref(false);
const showCreateDialog = ref(false); // Added missing state variable
const showDeleteDialog = ref(false);
const dialogMode = ref('create');
const selectedProduct = ref(null);

const formData = reactive({
    name: ''
});

const productForm = ref(null);

// Validation rules based on schema
const rules = {
    name: [
        { required: true, message: 'Name is required', trigger: 'blur' },
        { max: 255, message: 'Name cannot exceed 255 characters', trigger: 'blur' }
    ]
};

// Watch for showCreateDialog changes
watch(showCreateDialog, (newVal) => {
  if (newVal) {
    dialogMode.value = 'create';
    resetForm();
    showDialog.value = true;
    showCreateDialog.value = false;
  }
});
const fetchProducts = async () => {
    try {
        loading.value = true;
        const params = {
            page: currentPage.value,
            page_size: pageSize.value
        };
        if (searchQuery.value) {
            params.name__icontains = searchQuery.value;
        }
        const [error, data] = await api.getProducts(params);
        if (error) {
            ElMessage.error('Failed to fetch products');
            console.error('Error fetching products:', error);
            return;
        }
        products.value = data.results;
        total.value = data.count;
    } catch (error) {
        ElMessage.error('Failed to fetch products');
        console.error('Error fetching products:', error);
    } finally {
        loading.value = false;
    }
};

const handleSearch = () => {
    currentPage.value = 1;
    fetchProducts();
};

const clearSearch = () => {
    searchQuery.value = '';
    handleSearch();
};

const handleSizeChange = (val) => {
    pageSize.value = val;
    fetchProducts();
};

const handleCurrentChange = (val) => {
    currentPage.value = val;
    fetchProducts();
};

const handleEdit = (product) => {
    dialogMode.value = 'edit';
    selectedProduct.value = product;
    formData.name = product.name;
    showDialog.value = true;
};

const handleDelete = (product) => {
    selectedProduct.value = product;
    showDeleteDialog.value = true;
};

const confirmDelete = async () => {
    try {
        const [error] = await api.deleteProduct(selectedProduct.value.id);
        if (error) {
            ElMessage.error('Failed to delete product');
            console.error('Error deleting product:', error);
            return;
        }
        ElMessage.success('Product deleted successfully');
        showDeleteDialog.value = false;
        fetchProducts();
    } catch (error) {
        ElMessage.error('Failed to delete product');
        console.error('Error deleting product:', error);
    }
};

const handleSubmit = async () => {
    if (!productForm.value) return;
    
    await productForm.value.validate(async (valid) => {
        if (valid) {
            try {
                let error;
                if (dialogMode.value === 'create') {
                    [error] = await api.createProduct(formData);
                    if (!error) {
                        ElMessage.success('Product created successfully');
                    }
                } else {
                    [error] = await api.updateProduct(selectedProduct.value.id, formData);
                    if (!error) {
                        ElMessage.success('Product updated successfully');
                    }
                }
                
                if (error) {
                    ElMessage.error('Operation failed');
                    console.error('Error submitting form:', error);
                    return;
                }
                
                showDialog.value = false;
                fetchProducts();
                resetForm();
            } catch (error) {
                ElMessage.error('Operation failed');
                console.error('Error submitting form:', error);
            }
        }
    });
};

const resetForm = () => {
    if (productForm.value) {
        productForm.value.resetFields();
    }
    formData.name = '';
    selectedProduct.value = null;
};

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
};

// Lifecycle hooks
onMounted(() => {
    fetchProducts();
});
</script>

<style scoped>
.product {
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
    align-items: end;
}

.pagination {
    margin-top: 20px;
    display: flex;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
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
:deep(.el-pagination .btn-prev) {
    margin-right: 8px;
}
:deep(.el-pagination .btn-prev::after) {
    content: "Previous";
}
:deep(.el-pagination .btn-next) {
    margin-left: 8px;
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
</style>