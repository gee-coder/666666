import {request} from "./request.js"
import store from "../store/index.js"

//获取得分点
    // 类型： post
    // 参数： question，standardAnswer
    // 返回： scoringPoint
export function getScoringPoint(data) {
  return request({
		baseURL: store.state.PSHAP,
    url: '/未知',
    method: 'post',
    data
  })
}

//添加新题目
export function addProblem(data) {
  return request({
    url: '/addProblem',
    method: 'post',
    data
  })
}

//获取题目的分页列表
export function findAllProblems(data) {
  return request({
    url: '/findProblemByPage',
    method: 'post',
    data
  })
}

//根据题目和标准答案模糊查找题目
export function findLikes(data) {
  return request({
    url: '/findLikes',
    method: 'post',
    data
  })
}

//修改书信息
export function alterProblem(data) {
  return request({
    url: '/alterProblem',
    method: 'post',
    data
  })
}

//删除书
export function deleteProblem(data) {
  return request({
    url: '/delProblemByQuestionId',
    method: 'post',
    data
  })
}

//删除书
export function getARandomProblem() {
  return request({
    url: '/getARandomProblem',
    method: 'get'
  })
}