import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    //网络请求的主机地址加端口号:java server host and port的缩写
    JSHAP: 'http://127.0.0.1:8081',
		//网络请求的主机地址加端口号:python server host and port的缩写
    PSHAP: 'http://未知'
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
