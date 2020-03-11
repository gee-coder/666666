package com.hanger.controller;

import com.hanger.entity.Reply;
import com.hanger.service.ProblemService;
import com.hanger.service.ReplyService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import java.util.Arrays;
import java.util.List;

/**
 * @author hanger
 * 2020-03-11 15:59
 */

@RestController
@CrossOrigin
public class TestController {
    private Logger logger = LoggerFactory.getLogger(TestController.class);

    private final ProblemService problemService;
    private final ReplyService replyService;

    public TestController(ProblemService problemService, ReplyService replyService) {
        this.problemService = problemService;
        this.replyService = replyService;
    }


    //初始化首页
    @RequestMapping(value = "initTest", method = RequestMethod.GET)
    public String initTest() {
        logger.info("初始化首页");

        //获取问题的总个数
        long problemNumber = problemService.getProblemsNum();
        //查找所有问题的系统和人工打分
        List<String> fields = Arrays.asList("systemScore", "score");
        List<Reply> replys = replyService.findAllTheFields(fields);
//        System.out.println(replys);
        //获取回答记录总个数
        int replyNumber = replys.size();
        //误差绝对值1-10出现的次数
        Integer[] errorNumber = new Integer[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
        //横坐标数据数组
        Integer[] xIndex = new Integer[replyNumber];
        //系统打分数组
        Integer[] systemScore = new Integer[replyNumber];
        //人工打分数组
        Integer[] score = new Integer[replyNumber];
        //方差数组
        Double[] variance = new Double[replyNumber];
        //计算准确率的辅助
        double sum = 0;

        for (int i = 0; i < replyNumber; i++) {
            //获取当前回答记录
            Reply reply = replys.get(i);
            //横坐标下标从1开始
            xIndex[i] = i + 1;
            //添加系统打分
            systemScore[i] = reply.getSystemScore();
            //添加人工打分
            score[i] = reply.getScore();
            //计算并添加对应方差
            double c = (systemScore[i] + score[i]) / 2.0;
            variance[i] = (Math.pow(systemScore[i] - c, 2) + Math.pow(score[i] - c, 2)) / 2.0;
            //计算差值的绝对值
            int abs = Math.abs(systemScore[i] - score[i]);
            //如果差值绝对值不等于0就将数组在位的值加1，从而记录对应差值的个数
            if (abs != 0) {
                errorNumber[abs - 1] += 1;
            }
            //计算总偏移数
            sum += abs;
        }

        //准确率
        double precisionRate = (1 - ((sum / replyNumber) / 10)) * 100;
        //四舍五入保留一位小数
        precisionRate = (double) Math.round(precisionRate * 10) / 10;

        return "{\"problemNumber\":" + problemNumber +
                ", \"replyNumber\":" + replyNumber +
                ", \"errorNumber\":" + Arrays.toString(errorNumber) +
                ", \"xIndex\":" + Arrays.toString(xIndex) +
                ", \"systemScore\":" + Arrays.toString(systemScore) +
                ", \"score\":" + Arrays.toString(score) +
                ", \"variance\":" + Arrays.toString(variance) +
                ", \"precisionRate\":" + precisionRate +
                "}";
    }





}
