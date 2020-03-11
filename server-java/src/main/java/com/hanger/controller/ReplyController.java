package com.hanger.controller;

import com.alibaba.fastjson.JSON;
import com.hanger.entity.Problem;
import com.hanger.entity.Reply;
import com.hanger.service.ProblemService;
import com.hanger.service.ReplyService;
import com.hanger.util.JsonUtil;
import com.mongodb.client.result.DeleteResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

/**
 * @author hanger
 * 2020-01-20 13:42
 */

@RestController
@CrossOrigin
public class ReplyController {
    private Logger logger = LoggerFactory.getLogger(ReplyController.class);

    private final String URL_ROOT = "https://aistudio.baidu.com/";

    private final RestTemplate restTemplate;
    private final ProblemService problemService;
    private final ReplyService replyService;

    @Autowired
    public ReplyController(RestTemplate restTemplate, ProblemService problemService, ReplyService replyService) {
        this.restTemplate = restTemplate;
        this.problemService = problemService;
        this.replyService = replyService;
    }


    //获取系统打分分值
    @RequestMapping(value = "getSystemScore",method = RequestMethod.POST)
    public String getSystemScore(@RequestBody String str) {
        logger.info("添加新回答" + str);
        HashMap map = JSON.parseObject(str, HashMap.class);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"questionId", "answer"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        String questionId = (String) map.get("questionId");
        String answer = (String) map.get("answer");

        //作为测试样例不再检验数据合法性

        Problem problem = problemService.findProblemByQuestionId(questionId);
        //检验题目是否存在
        if (problem == null) {
            logger.warn("该题目不存在");
            return "{\"code\":\"101\"}";
        }

//        //向python接口发送的json类型请求参数
//        String param = "{\"question\":\"" + problem.getQuestion() +
//                "\",\"standardAnswer\":\"" + problem.getStandardAnswer() +
//                "\",\"scoringPoint\":\"" + Arrays.toString(problem.getScoringPoint()) +
//                "\",\"answer\":\"" + answer +
//                "\"}";
//        //请求的参数封装
//        HttpEntity<String> entity = new HttpEntity<>(param, new HttpHeaders());
//        //向URL_ROOT发起post类型请求并携带封装好的参数、传回String集合类型的封装结果
//        ResponseEntity<String> responseEntity = restTemplate.exchange(URL_ROOT + "serving", HttpMethod.POST, entity, String.class);
//        System.out.println(responseEntity.getBody());
//
//        HashMap pythonMap = JSON.parseObject(responseEntity.getBody(), HashMap.class);
//        if (pythonMap == null) {
//            logger.warn("python接口请求失败");
//            return "{\"code\":\"001\"}";
//        }
//
//        Integer systemScore = (Integer) pythonMap.get("systemScore");

        //随机生成一个[0-10]的整数num
        long systemScore = (long) (Math.random() * (10 + 1));
        return "{\"code\":\"111\", \"systemScore\":" + systemScore + "}";
    }



    //添加新回答
    @RequestMapping(value = "addReply",method = RequestMethod.POST)
    public String addReply(@RequestBody String str) {
        logger.info("添加新回答" + str);
        HashMap map = JSON.parseObject(str, HashMap.class);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"questionId", "answer", "systemScore", "score"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        String questionId = (String) map.get("questionId");
        String answer = (String) map.get("answer");
        Integer systemScore = (Integer) map.get("systemScore");
        Integer score = (Integer) map.get("score");

        //作为测试样例不再检验数据合法性

        Problem problem = problemService.findProblemByQuestionId(questionId);
        //检验题目是否存在
        if (problem == null) {
            logger.warn("该题目不存在");
            return "{\"code\":\"101\"}";
        }

        Reply replyIn = new Reply(questionId, answer, systemScore, score);
        Reply replyOut = replyService.addReply(replyIn);
        System.out.println(JSON.toJSONString(replyOut));
        logger.info("添加新回答成功");

        return "{\"code\":\"111\"}";
    }



    //分页查询所有回答
    @RequestMapping(value = "findReplyByPage",method = RequestMethod.POST)
    public String findReplyByPage(@RequestBody String str) {
        logger.info("分页查询所有回答" + str);
        HashMap map = JSON.parseObject(str, HashMap.class);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"pageSize","pageNum"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        Integer pageSize = (Integer) map.get("pageSize");
        Integer pageNum = (Integer) map.get("pageNum");

        //分页查询所有题目，Mongo的分页是从0开始的需-1
        List<Reply> replys = replyService.findReplyByPage(pageNum - 1, pageSize);

        long td = replyService.getReplysNum();
        String rs = JSON.toJSONString(replys);
        System.out.println(rs);

        return "{\"total\":" + td + ",\"info\":" + rs + "}";
    }



    //通过题目ID、作答结果、系统给分和得分描述模糊查询
    @RequestMapping(value = "findReplyLikes",method = RequestMethod.POST)
    public String findReplyLikes(@RequestBody String str) {
        logger.info("模糊查询回答" + str);
        HashMap map = JSON.parseObject(str, HashMap.class);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"search"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        String search = (String) map.get("search");

        List<Reply> replys = replyService.findLikes(search);

        long td = replys.size();
        System.out.println(td);
        String bs = JSON.toJSONString(replys);
        System.out.println(bs);

        return "{\"total\":" + td + ",\"info\":" + bs + "}";
    }



    //通过id删除回答
    @RequestMapping(value = "delReplyByAnswerId",method = RequestMethod.POST)
    public String delReplyByAnswerId(@RequestBody String str) {
        logger.info("通过id删除回答" + str);
        HashMap map = JSON.parseObject(str, HashMap.class);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"answerId"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        String answerId = (String) map.get("answerId");

        Reply reply = replyService.findReplyByAnswerId(answerId);
        if (reply == null) {
            logger.warn("该回答不存在");
            return "{\"code\":\"111\"}";
        }

        DeleteResult deleteResult = replyService.delReplyByAnswerId(answerId);
        if (deleteResult.getDeletedCount() <= 0) {
            logger.warn("回答删除失败");
            return "{\"code\":\"404\"}";
        } else {
            logger.info("回答删除成功");
            return "{\"code\":\"111\"}";
        }
    }



}
