<script setup>
import { ref } from 'vue';
const props = defineProps({
    total: {
        type: Number,
        default: 1
    }
})

const pageSize = 10
const selected = ref({
    search: "",
    page: 1,
})

const emits = defineEmits(['change'])
const handleChange = (current) => {
    emits('change', current, pageSize)
}
</script>

<template>
    <div class="pagination">
        <el-pagination background layout="prev, pager, next" :total="props.total" @change="handleChange" />
    </div>

</template>

<style lang="scss" scoped>
.pagination {
    margin-top: 20px;
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
</style>