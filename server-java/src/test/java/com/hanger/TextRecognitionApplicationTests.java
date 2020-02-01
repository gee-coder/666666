package com.hanger;


import com.alibaba.fastjson.JSON;
import com.hanger.entity.Problem;
import com.hanger.service.ProblemService;
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

    @Autowired
    TextRecognitionApplicationTests(RestTemplate restTemplate, ProblemService problemService) {
        this.restTemplate = restTemplate;
        this.problemService = problemService;
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
            long num = (long) (Math.random() * 12 + 1);
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


}
