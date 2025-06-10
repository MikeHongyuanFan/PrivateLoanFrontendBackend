import axios from 'axios'

const api_base_url = import.meta.env.VITE_API_BASE_URL
import { ElMessage } from 'element-plus'
import useSystem from '@/hooks/useSystem'

const { logOut } = useSystem()
// console.log(api_base_url);

const sendRequest = axios.create({
  baseURL: api_base_url,
  // 超时时间3分钟
  timeout: 180000,
})

// 添加请求拦截器
sendRequest.interceptors.request.use(
  async (config) => {
    // Log the request configuration for debugging
    console.log('Request config:', {
      url: config.url,
      method: config.method,
      params: config.params,
      data: config.data
    });
    
    // 发送之前 处理请求头等信息
    let userInfo = localStorage.getItem('userInfo')
    if (userInfo) {
      userInfo = JSON.parse(userInfo)
      config.headers['Authorization'] = `Bearer ${userInfo.access}`
    }
    return config
  },
  (error) => {
    // 请求发生错误
    return Promise.reject(error)
  },
)
// 添加响应拦截
sendRequest.interceptors.response.use(
  (response) => {
    // 结合响应状态处理请求结果。
    const responseData = response.data
    return [null, responseData]
  },
  (error) => {
    const response = error.response
    //处理401鉴权失败
    if (response?.status === 401) {
      ElMessage.error(response.data.detail || response.data.error)
      logOut()
    }
    return [response?.data, null]
  },
)

export default sendRequest

