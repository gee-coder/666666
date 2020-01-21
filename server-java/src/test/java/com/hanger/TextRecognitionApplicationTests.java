package com.hanger;

import com.alibaba.fastjson.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;

@SpringBootTest
class TextRecognitionApplicationTests {
    private final RestTemplate restTemplate;

    @Autowired
    TextRecognitionApplicationTests(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
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



}
