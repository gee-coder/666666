package com.hanger.controller;

import com.alibaba.fastjson.JSON;
import com.hanger.entity.Problem;
import com.hanger.service.ProblemService;
import com.hanger.util.JsonUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.HashMap;


/**
 * @author hanger
 * 2020-01-20 13:42
 */

@RestController
@CrossOrigin
public class ProblemController {
    private Logger logger = LoggerFactory.getLogger(ProblemController.class);

    private final ProblemService problemService;
    private final RestTemplate restTemplate;

    @Autowired
    public ProblemController(ProblemService problemService, RestTemplate restTemplate) {
        this.problemService = problemService;
        this.restTemplate = restTemplate;
    }


    // 得分点推荐直接用前端调用
    // 类型： post
    // 参数： question，standardAnswer
    // 返回： scoringPoint推荐值



    //添加新问题
    @RequestMapping(value = "addProblem", method = RequestMethod.POST)
    public String addProblem(@RequestBody String str) {
        logger.info("添加新问题" + str);
        HashMap map = JSON.parseObject(str, HashMap.class);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"question", "standardAnswer", "scoringPoint"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        String question = (String) map.get("question");
        String standardAnswer = (String) map.get("standardAnswer");
        String scoringPoint = (String) map.get("scoringPoint");

        //作为测试样例不再检验数据合法性

        Problem problemIn = new Problem(question, standardAnswer, scoringPoint);
        Problem problemOut = problemService.addProblem(problemIn);
        System.out.println(JSON.toJSONString(problemOut));
        logger.info("添加新问题成功");
        return "{\"code\":\"111\",\"questionId\":\"" + problemOut.getQuestionId() + "\"}";
    }






}
