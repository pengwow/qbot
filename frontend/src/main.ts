import { createApp } from 'vue'
import App from './App.vue'
// @ts-ignore 临时忽略缺少类型声明文件的问题
import router from './router/index.ts'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createPinia } from 'pinia'

/**
 * 创建并挂载Vue应用实例
 * 集成路由、Element Plus和Pinia
 */
const app = createApp(App)
const pinia = createPinia()

// 使用路由
app.use(router)

// 使用Element Plus
app.use(ElementPlus)

// 使用Pinia
app.use(pinia)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 挂载应用
app.mount('#app')