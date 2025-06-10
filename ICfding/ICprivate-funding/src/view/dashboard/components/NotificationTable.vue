<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'

onMounted(() => {
})

const tableData = ref([])

tableData.value = new Array(10)
  .fill(null)
  .map((_, index) => ({
    application: `${index}-123124`,
    type: 'Repayment',
    subject: 'Subject',
    time: '17/06/2024',
  }));
</script>

<template>
  <el-table :data="tableData" class="table" :header-cell-style="{ background: '#f8f8f8', color: '#272727' }">
    <el-table-column prop="application" label="Application" />
    <el-table-column prop="type" label="Type" />
    <el-table-column prop="subject" label="Subject" />
    <el-table-column prop="time" label="Time" />
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
