import Vue from 'vue'
import App from './App.vue'
//引入路由
import router from './router'
//引入vuex
import store from './store'
//引入element
import './plugins/element.js'
//引入echarts
import echarts from 'echarts'
//导入全局样式表
import 'css/global.css'
//解决使用element后在谷歌浏览器鼠标事件控制台警告
import 'default-passive-events'

Vue.config.productionTip = false
Vue.prototype.$echarts = echarts

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
