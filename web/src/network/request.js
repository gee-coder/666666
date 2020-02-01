import axios from 'axios'
import store from "../store/index.js"

export function request(config) {
  /* 创建axios实例
  设置服务器的根地址
  设置请求超时时间5s
  */
  const instance = axios.create({
		baseURL: store.state.JSHAP,
    timeout: 5000
  })

  /* axios的request拦截器
  拦截将要发送出去的请求
  */
  instance.interceptors.request.use(config => {
    //此处编写拦截后要处理的代码，处理完后放行请求
    //为请求头添加token验证的Authorization字段
    // config.headers.Authorization = window.sessionStorage.getItem('token')
    return config
  }, err => {
    //出现错误将会执行这里的代码
    // console.log(err);
  })

  /* axios的response拦截器
  拦截将要响应的请求
  */
  instance.interceptors.response.use(res => {
    //此处编写拦截后要处理的代码，处理完后放行请求
    return res
  }, err => {
    //出现错误将会执行这里的代码
    // console.log(err);
  })

  //此处调用axios的自定义实例instance开始真正执行请求并且返回Promise类型的结果
  return instance(config)
}
