package com.hanger;


import com.alibaba.fastjson.JSON;
import com.hanger.entity.Problem;
import com.hanger.entity.Reply;
import com.hanger.service.ProblemService;
import com.hanger.service.ReplyService;
import com.hanger.util.ExcelUtil;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;

import java.io.*;
import java.util.Arrays;
import java.util.List;


@SpringBootTest
class TextRecognitionApplicationTests {
    private final RestTemplate restTemplate;
    private final ProblemService problemService;
    private final ReplyService replyService;

    @Autowired
    TextRecognitionApplicationTests(RestTemplate restTemplate, ProblemService problemService, ReplyService replyService) {
        this.restTemplate = restTemplate;
        this.problemService = problemService;
        this.replyService = replyService;
    }


    @Test
    void contextLoads() {
        String param = "{\"input\":10}";
        System.out.println(param);

        HttpEntity<String> entity = new HttpEntity<>(param, new HttpHeaders());
        ResponseEntity<String> exchange = restTemplate.exchange(
                "https://aistudio.baidu.com/serving/online/2118?apiKey=4d94a703-5a89-4e18-9fd3-c4c085fcb01c",
                HttpMethod.POST,
                entity,
                String.class);
        System.out.println(exchange.getBody());
    }


    @Test
    void t1() {
        for (int i = 0; i < 13; i++) {
            System.out.println(i % 5);
        }
    }


    @Test
    void arr() {
        String[] str = new String[9];
        for (int i = 0; i < 5; i++) {
            if ((i/2) == ((i + 1)/2)) {
                str[i] = "da";
            }
        }

        System.out.println(Arrays.toString(str));
        for (String s:
             str) {
            System.out.println(s);
        }
    }


    @Test
    void excelProblems() throws Exception{
        InputStream inputStream = new FileInputStream("D:/test.xlsx");
        List<Problem> ps = ExcelUtil.excel2JavaBeans("xlsx", inputStream, Problem.class);
        System.out.println(JSON.toJSONString(ps));
    }


    @Test
    void randomNum() {
        for (int i = 0; i < 100; i++) {
            //随机生成一个[1-12]的整数
//            long num = (long) (Math.random() * 12 + 1);
            //随机生成一个[0-10]的整数
            long num = (long) (Math.random() * (10 + 1));
            System.out.println(num);
        }
    }


    @Test
    void pint() {
        //获取问题的总个数
        long td = problemService.getProblemsNum();

        long num = (long) (Math.random() * td + 1);
        System.out.println(num);

        Problem problem = problemService.findTheRandomNumberRecord(num);
        String p = JSON.toJSONString(problem);
        System.out.println(p);
    }


    @Test
    void TestData() {
        //系统打分
        Integer[] sys = new Integer[]{8,6,6,1,9,10,5,6,9,0,9,8};
        //人工打分
        Integer[] man = new Integer[]{7,5,6,0,10,10,9,7,9,3,6,8};
        //方差数组
        Double[] out = new Double[man.length];
        //计算准确率
        double sum = 0;

        for (int i = 0; i < man.length; i++) {
            double c = (sys[i] + man[i]) / 2.0;
            System.out.println("第" + i + "个平均数=" + c);
            System.out.println("第" + i + "个=" + Math.pow(sys[i] - c, 2));
            out[i] = (Math.pow(sys[i] - c, 2) + Math.pow(man[i] - c, 2)) / 2.0;

            int abs = Math.abs(sys[i] - man[i]);
            sum += abs;
        }
        System.out.println(Arrays.toString(out));


        double o = (sum / man.length) / 10;
        System.out.println(o);
        System.out.println("准确率：" + ((1 - o) * 100) + "%");

    }


    @Test
    void theFields() {
        //查找所有问题的系统和人工打分
//        List<String> fields = Arrays.asList("systemScore", "score");
//        List<Reply> replys = replyService.findAllTheFields(fields);
//        System.out.println(replys);
        Integer[] out = new Integer[10];
        for (int i = 0; i < 10; i++) {
            System.out.println(out[i]);
        }
    }


}
