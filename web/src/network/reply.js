import {request} from "./request.js"

//获取系统打分分值
export function getSystemScore(data) {
  return request({
    url: '/getSystemScore',
    method: 'post',
    data
  })
}

//添加新回答
export function addReply(data) {
  return request({
    url: '/addReply',
    method: 'post',
    data
  })
}

//获取回答的分页列表
export function findAllReplys(data) {
  return request({
    url: '/findReplyByPage',
    method: 'post',
    data
  })
}

//通过题目ID、作答结果、系统给分和得分描述模糊查询
export function findLikes(data) {
  return request({
    url: '/findReplyLikes',
    method: 'post',
    data
  })
}

//删除回答
export function deleteReply(data) {
  return request({
    url: '/delReplyByAnswerId',
    method: 'post',
    data
  })
}