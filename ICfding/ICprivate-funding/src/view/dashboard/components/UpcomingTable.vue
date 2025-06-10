<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'

onMounted(() => {
})

const tableData = ref([])

tableData.value = new Array(2)
  .fill(null)
  .map((_, index) => ({
    application: `${index}-123124`,
    amount: 'Repayment',
    status: 'Subject',
    dueDate: '17/06/2024',
  }));
</script>

<template>
  <el-table :data="tableData" class="table" :header-cell-style="{ background: '#f8f8f8', color: '#272727' }">
    <el-table-column prop="application" label="Application" />
    <el-table-column prop="amount" label="Amount" />
    <el-table-column prop="status" label="Status" />
    <el-table-column prop="dueDate" label="Due Date" />
  </el-table>
</template>

<style lang="scss" scoped>
.table {
  height: 100%;

  .number {
    font-weight: 400;
    font-size: 12px;

    ::v-deep(.el-statistic__content) {
      font-size: 12px;
    }
  }
}
</style>
