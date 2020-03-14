import {request} from "./request.js"
import store from "../store/index.js"

//添加新题目
export function initTest() {
  return request({
    url: '/initTest',
    method: 'get'
  })
}