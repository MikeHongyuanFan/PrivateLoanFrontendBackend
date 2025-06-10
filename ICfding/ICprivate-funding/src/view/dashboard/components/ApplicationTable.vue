<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'

onMounted(() => {
})

const tableData = ref([])

tableData.value = new Array(10)
  .fill(null)
  .map((_, index) => ({
    application: `${index}-REF123`,
    type: 'Residential',
    amount: '500000.00',
    status: 'Paid',
    createDate: '2023-10-01',
  }));
</script>

<template>
  <el-table :data="tableData" class="table" :header-cell-style="{ background: '#f8f8f8', color: '#272727' }">
    <el-table-column prop="application" label="Application" />
    <el-table-column prop="type" label="Type" />
    <el-table-column prop="amount" label="Amount">
      <template #default="scope">
        <el-statistic class="number" :value="Number(scope.row.amount)" v-if="scope.row.amount" :precision="2"
          :formatter="(value) => `$ ${value.toFixed(2)}`" />
      </template>
    </el-table-column>
    <el-table-column prop="status" label="Status" />
    <el-table-column prop="createDate" label="Create Date" />
  </el-table>
</template>

<style lang="scss" scoped>
.table {
  height: 100%;
  font-family: Inter;

  .number {
    font-weight: 400;
    font-size: 12px;

    ::v-deep(.el-statistic__content) {
      font-size: 12px;
    }
  }
}
</style>
