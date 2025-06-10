import { ref, onMounted } from 'vue'
import { api } from '@/api'

const branchesList = ref([])

//breach字典hook
export default function useBranch() {
  onMounted(() => {
    getBranches()
  })

  async function getBranches() {
    //如果有数据就不请求
    if (branchesList.value.length > 0) {
      return
    }
    let params = {
      page: 1,
      page_size: 100,
    }
    const [err, res] = await api.branches(params)
    if (!err) {
      // console.log('获取分支字典成功', res)
      branchesList.value = res?.results || []
    }
  }

  return {
    branchesList,
  }
}

