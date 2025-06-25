<template>
  <FeePopup @close="handleClose" :dashboard-mode="true" />
</template>

<script setup>
import FeePopup from './fee.vue'

const props = defineProps({
  action: {
    type: String,
    default: 'Add Fee'
  }
})

const emit = defineEmits(['close'])

const handleClose = () => {
  emit('close')
}
</script>

<style lang="scss" scoped>
/* No additional styling needed - FeePopup handles its own styling */
</style> 