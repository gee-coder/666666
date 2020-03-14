package com.hanger.controller;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.hanger.entity.Problem;
import com.hanger.service.ProblemService;
import com.hanger.service.ReplyService;
import com.hanger.util.JsonUtil;
import com.mongodb.client.result.DeleteResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.*;


/**
 * @author hanger
 * 2020-01-20 13:42
 */

@RestController
@CrossOrigin
public class ProblemController {
    private Logger logger = LoggerFactory.getLogger(ProblemController.class);

    private final ProblemService problemService;
    private final ReplyService replyService;

    @Autowired
    public ProblemController(ProblemService problemService, ReplyService replyService) {
        this.problemService = problemService;
        this.replyService = replyService;
    }


    //添加新题目
    @RequestMapping(value = "addProblem", method = RequestMethod.POST)
    public String addProblem(@RequestBody String str) {
        logger.info("添加新题目" + str);
        Map map = JSON.parseObject(str, Map.class);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"question", "standardAnswer", "scoringPoint"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        String question = (String) map.get("question");
        String standardAnswer = (String) map.get("standardAnswer");
        JSONArray jsonArray = (JSONArray) map.get("scoringPoint");
        List<String> list = jsonArray.toJavaList(String.class);
        String[] temp = new String[list.size()];
        String[] scoringPoint = list.toArray(temp);

        //作为测试样例不再检验数据合法性

        Problem problemIn = new Problem(question, standardAnswer, scoringPoint);
        Problem problemOut = problemService.addProblem(problemIn);
        System.out.println(JSON.toJSONString(problemOut));
        logger.info("添加新问题成功");

        return "{\"code\":\"111\"}";
    }



    //分页查询所有题目
    @RequestMapping(value = "findProblemByPage",method = RequestMethod.POST)
    public String findProblemByPage(@RequestBody String str) {
        logger.info("分页查询所有题目" + str);
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
        List<Problem> problems = problemService.findProblemByPage(pageNum - 1, pageSize);

        long td = problemService.getProblemsNum();
        String ps = JSON.toJSONString(problems);
        System.out.println(ps);

        return "{\"total\":" + td + ",\"info\":" + ps + "}";
    }



    //通过题目和标准答案模糊查询题目
    @RequestMapping(value = "findLikes",method = RequestMethod.POST)
    public String findLikes(@RequestBody String str) {
        logger.info("通过题目和标准答案模糊查询题目" + str);
        HashMap map = JSON.parseObject(str, HashMap.class);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"search"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        String search = (String) map.get("search");

        List<Problem> problems = problemService.findLikes(search);

        long td = problems.size();
        System.out.println(td);
        String bs = JSON.toJSONString(problems);
        System.out.println(bs);

        return "{\"total\":" + td + ",\"info\":" + bs + "}";
    }



    //修改题目的基本信息
    @RequestMapping(value = "alterProblem",method = RequestMethod.POST)
    public String alterProblem(@RequestBody String str) {
        logger.info("修改题目的基本信息" + str);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"questionId","question", "standardAnswer", "scoringPoint"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        Problem problem = JSON.parseObject(str, Problem.class);

        Problem p = problemService.findProblemByQuestionId(problem.getQuestionId());
        //检验题目是否存在
        if (p == null) {
            logger.warn("该题目不存在");
            return "{\"code\":\"101\"}";
        }

        //作为测试样例不再检验数据合法性
        Problem newProblem = problemService.saveProblem(problem);
        System.out.println(JSON.toJSONString(newProblem));
        logger.info("题目信息更新成功");

        return "{\"code\":\"111\"}";
    }



    //通过id删除题目
    @RequestMapping(value = "delProblemByQuestionId",method = RequestMethod.POST)
    public String delProblemByQuestionId(@RequestBody String str) {
        logger.info("通过id删除题目" + str);
        HashMap map = JSON.parseObject(str, HashMap.class);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"questionId"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        String questionId = (String) map.get("questionId");

        Problem problem = problemService.findProblemByQuestionId(questionId);
        if (problem == null) {
            logger.warn("该题目不存在");
            return "{\"code\":\"111\"}";
        }

        DeleteResult deleteProblemResult = problemService.delProblemByQuestionId(questionId);
        //删除该问题的所有回答记录
        DeleteResult deleteReplyResult = replyService.delReplyByQuestionId(questionId);
        System.out.println("删除题目相关回答记录" + deleteReplyResult.getDeletedCount() + "条");
        if (deleteProblemResult.getDeletedCount() <= 0) {
            logger.warn("题目删除失败");
            return "{\"code\":\"404\"}";
        } else {
            logger.info("题目删除成功");
            return "{\"code\":\"111\"}";
        }
    }



    //通过id查询题目
    @RequestMapping(value = "findProblemByQuestionId",method = RequestMethod.POST)
    public String findProblemByQuestionId(@RequestBody String str) {
        logger.info("通过id查询题目" + str);
        HashMap map = JSON.parseObject(str, HashMap.class);
        //验证请求体中的请求个数与key名是否合法
        String [] jsonKeys = {"questionId"};
        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
            logger.warn("请求体参数格式错误");
            return "{\"code\":\"000\"}";
        }

        String questionId = (String) map.get("questionId");

        Problem problem = problemService.findProblemByQuestionId(questionId);
        if (problem == null) {
            logger.warn("该题目不存在");
            return "{\"code\":\"101\"}";
        }

        String p = JSON.toJSONString(problem);
        System.out.println(p);

        return "{\"code\":\"111\",\"info\":[" + p + "]}";
    }



    //随机获取一个题目
    @RequestMapping(value = "getARandomProblem",method = RequestMethod.GET)
    public String getARandomProblem() {
        //获取问题的总个数
        long td = problemService.getProblemsNum();

        //随机生成一个[1-td]的整数num
        long num = (long) (Math.random() * td + 1);
        System.out.println(num);

        //查找第num条记录（从1开始）
        Problem problem = problemService.findTheRandomNumberRecord(num);
        String p = JSON.toJSONString(problem);
        System.out.println(p);

        return p;
    }









}
