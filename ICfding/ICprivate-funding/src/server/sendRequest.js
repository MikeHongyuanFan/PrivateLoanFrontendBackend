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

// Flag to prevent multiple token refresh requests
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  
  failedQueue = []
}

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
  async (error) => {
    const originalRequest = error.config
    const response = error.response

    // Handle 401 errors with automatic token refresh
    if (response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // If we're already refreshing, queue this request
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(token => {
          originalRequest.headers['Authorization'] = `Bearer ${token}`
          return sendRequest(originalRequest)
        }).catch(err => {
          return Promise.reject(err)
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      const userInfo = localStorage.getItem('userInfo')
      if (userInfo) {
        const parsedUserInfo = JSON.parse(userInfo)
        
        if (parsedUserInfo.refresh) {
          try {
            // Attempt to refresh the token
            const refreshResponse = await axios.post(
              `${api_base_url}/api/users/auth/refresh/`,
              { refresh: parsedUserInfo.refresh }
            )

            if (refreshResponse.data.access) {
              // Update stored tokens
              const newUserInfo = {
                ...parsedUserInfo,
                access: refreshResponse.data.access
              }
              localStorage.setItem('userInfo', JSON.stringify(newUserInfo))

              // Update the authorization header for the original request
              originalRequest.headers['Authorization'] = `Bearer ${refreshResponse.data.access}`
              
              // Process any queued requests
              processQueue(null, refreshResponse.data.access)
              isRefreshing = false

              // Retry the original request
              return sendRequest(originalRequest)
            }
          } catch (refreshError) {
            console.error('Token refresh failed:', refreshError)
            processQueue(refreshError, null)
            isRefreshing = false
            
            // If refresh fails, log out the user
            ElMessage.error('Session expired. Please log in again.')
            logOut()
            return Promise.reject(refreshError)
          }
        }
      }

      // If no refresh token available, log out immediately
      processQueue(error, null)
      isRefreshing = false
      ElMessage.error('Session expired. Please log in again.')
      logOut()
    }

    // For other errors, show the error message
    if (response?.status !== 401) {
      ElMessage.error(response?.data?.detail || response?.data?.error || 'An error occurred')
    }

    return [response?.data, null]
  },
)

export default sendRequest

