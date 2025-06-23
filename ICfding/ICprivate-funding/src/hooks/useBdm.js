import { ref, onMounted } from 'vue'
import { api } from '@/api'

const bdmList = ref([])

// BDM dictionary hook
export default function useBdm() {
  onMounted(() => {
    getBdms()
  })

  async function getBdms() {
    // If data already exists, don't request again
    if (bdmList.value.length > 0) {
      return
    }
    let params = {
      page: 1,
      page_size: 100,
    }
    const [err, res] = await api.bdmDropdown(params)
    if (!err) {
      // console.log('获取BDM字典成功', res)
      bdmList.value = res || []
    }
  }

  return {
    bdmList,
  }
} 