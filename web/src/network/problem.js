import {request} from "./request.js"
import store from "../store/index.js"

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

//修改题目信息
export function alterProblem(data) {
  return request({
    url: '/alterProblem',
    method: 'post',
    data
  })
}

//删除题目
export function deleteProblem(data) {
  return request({
    url: '/delProblemByQuestionId',
    method: 'post',
    data
  })
}

//随机获取一道题目
export function getARandomProblem() {
  return request({
    url: '/getARandomProblem',
    method: 'get'
  })
}

//添加新题目
export function initTest() {
  return request({
    url: '/initTest',
    method: 'get'
  })
}