/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

import axios from 'axios';


// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://localhost:8000',
}


// 创建带有认证拦截器的 Axios 实例
export const apiClient = axios.create({
  baseURL: apiConfig.baseURL,
});


// 请求拦截器：自动添加 Bearer token
apiClient.interceptors.request.use(
  (config) => {
    // 从 localStorage 获取 token
    const userStoreStr = localStorage.getItem('user-store');
    if (userStoreStr) {
      try {
        const userStore = JSON.parse(userStoreStr);
        if (userStore.token) {
          config.headers.Authorization = `Bearer ${userStore.token}`;
        }
      } catch (e) {
        console.error('解析用户存储失败:', e);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const aiChatConfig = {
  // OpenAI API地址
  apiEndpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
  
  // API Key (由开发人员指定)
  apiKey: 'sk-7f82bded3425435ea452f8f0df9262a2',
  
  // 使用的模型
  model: 'qwen3-max-preview'
}
