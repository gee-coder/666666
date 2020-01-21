package com.hanger.controller;

import com.alibaba.fastjson.JSON;
import com.hanger.entity.Problem;
import com.hanger.entity.Reply;
import com.hanger.service.ProblemService;
import com.hanger.service.ReplyService;
import com.hanger.util.JsonUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;

/**
 * @author hanger
 * 2020-01-20 13:42
 */

@RestController
@CrossOrigin
public class ReplyController {
    private Logger logger = LoggerFactory.getLogger(ProblemController.class);

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


    //添加新回答
    @RequestMapping(value = "addReply",method = RequestMethod.POST)
    public String addReply(@RequestBody String str) {
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

        String param = "{\"question\":\"" + problem.getQuestion() +
                "\",\"standardAnswer\":\"" + problem.getStandardAnswer() +
                "\",\"scoringPoint\":\"" + problem.getScoringPoint() +
                "\",\"answer\":\"" + answer +
                "\"}";

        HttpEntity<String> entity = new HttpEntity<>(param, new HttpHeaders());
        ResponseEntity<String> responseEntity = restTemplate.exchange(URL_ROOT + "serving", HttpMethod.POST, entity, String.class);
        System.out.println(responseEntity.getBody());

        HashMap pythonMap = JSON.parseObject(responseEntity.getBody(), HashMap.class);
        Integer systemScore = (Integer) pythonMap.get("systemScore");
        String scoringDetailed = (String) pythonMap.get("scoringDetailed");

        Reply replyIn = new Reply(questionId, answer, systemScore, scoringDetailed);
        Reply replyOut = replyService.addReply(replyIn);
        System.out.println(JSON.toJSONString(replyOut));
        logger.info("添加新回答成功");

        return "{\"code\":\"111\",\"questionId\":\"" + replyOut.getAnswerId() + "\"}";
    }


//
//    //检查作者新添书的书名是否已经存在
//    @RequestMapping(value = "checkBookName",method = RequestMethod.POST)
//    public String checkBookName(@RequestBody String str) {
//        logger.info("检查作者新添书的书名是否已经存在" + str);
//        HashMap map = JSON.parseObject(str, HashMap.class);
//        //验证请求体中的请求个数与key名是否合法
//        String [] jsonKeys = {"author","bookName"};
//        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
//            logger.warn("请求体参数格式错误");
//            return "{\"code\":\"000\"}";
//        }
//
//        String author = (String) map.get("author");
//        String bookName = (String) map.get("bookName");
//
//        List<Test> authorTests = testService.findBookByBookAuthor(author);
//        for (Test b:
//                authorTests) {
//            if (bookName.equalsIgnoreCase(b.getBookName())) {
//                logger.warn("书本重复");
//                return "{\"code\":\"101\"}";
//            }
//        }
//
//        return "{\"code\":\"111\"}";
//    }
//
//
//
//    //分页查询所有书
//    @RequestMapping(value = "findBookByPage",method = RequestMethod.POST)
//    public String findBookByPage(@RequestBody String str) {
//        logger.info("分页查询所有书" + str);
//        HashMap map = JSON.parseObject(str, HashMap.class);
//        //验证请求体中的请求个数与key名是否合法
//        String [] jsonKeys = {"pageSize","pageNum"};
//        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
//            logger.warn("请求体参数格式错误");
//            return "{\"code\":\"000\"}";
//        }
//
//        Integer pageSize = (Integer) map.get("pageSize");
//        Integer pageNum = (Integer) map.get("pageNum");
//
//        //分页查询所有书，Mongo的分页是从0开始的需-1
//        List<Test> tests = testService.findBookByPage(pageNum - 1, pageSize);
//
//        long td = testService.getBooksNum();
//        String bs = JSON.toJSONString(tests);
//        System.out.println(bs);
//
//        return "{\"total\":" + td + ",\"info\":" + bs + "}";
//    }
//
//
//
//    //查找所有某Tag书
//    @RequestMapping(value = "findBookByBookTag",method = RequestMethod.POST)
//    public String findBookByBookTag(@RequestBody String str) {
//        logger.info("查找所有某Tag书" + str);
//        HashMap map = JSON.parseObject(str, HashMap.class);
//        //验证请求体中的请求个数与key名是否合法
//        String [] jsonKeys = {"tag"};
//        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
//            logger.warn("请求体参数格式错误");
//            return "{\"code\":\"000\"}";
//        }
//
//        String tag = (String) map.get("tag");
//
//        //检验标签是否合法
//        if (checkTag(tag) == 0) {
//            logger.warn("标签格式错误");
//            return "{\"code\":\"100\"}";
//        }
//
//        //查询该Tag的所有的书
//        List<Test> tests = testService.findBookByBookTag(tag);
//        System.out.println(JSON.toJSONString(tests));
//        return JSON.toJSONString(tests);
//    }
//
//
//
//    //通过id查询书
//    @RequestMapping(value = "findBookByBookId",method = RequestMethod.POST)
//    public String findBookByBookId(@RequestBody String str) {
//        logger.info("通过id查询书" + str);
//        HashMap map = JSON.parseObject(str, HashMap.class);
//        //验证请求体中的请求个数与key名是否合法
//        String [] jsonKeys = {"bookId"};
//        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
//            logger.warn("请求体参数格式错误");
//            return "{\"code\":\"000\"}";
//        }
//
//        String bookId = (String) map.get("bookId");
//
//        Test test = testService.findBookByBookId(bookId);
//        if (test == null) {
//            logger.warn("该书不存在");
//            return "{\"code\":\"001\"}";
//        }
//
//        String bs = JSON.toJSONString(test);
//
//        return "{\"code\":\"111\",\"info\":" + bs + "}";
//    }
//
//
//
//    //通过书名和作者模糊查询书
//    @RequestMapping(value = "findLikes",method = RequestMethod.POST)
//    public String findLikes(@RequestBody String str) {
//        logger.info("通过书名和作者模糊查询书" + str);
//        HashMap map = JSON.parseObject(str, HashMap.class);
//        //验证请求体中的请求个数与key名是否合法
//        String [] jsonKeys = {"search"};
//        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
//            logger.warn("请求体参数格式错误");
//            return "{\"code\":\"000\"}";
//        }
//
//        String search = (String) map.get("search");
//
//        List<Test> likes = testService.findLikes(search);
//
//        long td = likes.size();
//        System.out.println(td);
//        String bs = JSON.toJSONString(likes);
//        System.out.println(bs);
//
//        return "{\"total\":" + td + ",\"info\":" + bs + "}";
//    }
//
//
//
//    //修改书的基本信息
//    @RequestMapping(value = "alterBook",method = RequestMethod.POST)
//    public String alterBook(@RequestBody String str) {
//        logger.info("添加书" + str);
//        HashMap map = JSON.parseObject(str, HashMap.class);
//        //验证请求体中的请求个数与key名是否合法
//        String [] jsonKeys = {"bookId","bookName","tag","author","brief"};
//        if (!(JsonUtil.checkFormatStrict(str , jsonKeys))) {
//            logger.warn("请求体参数格式错误");
//            return "{\"code\":\"000\"}";
//        }
//
//        String bookId = (String) map.get("bookId");
//        String author = (String) map.get("author");
//        String bookName = (String) map.get("bookName");
//        String brief = (String) map.get("brief");
//        String tag = (String) map.get("tag");
//
//        Test test = testService.findBookByBookId(bookId);
//        if (test == null) {
//            logger.warn("该书不存在");
//            return "{\"code\":\"101\"}";
//        }
//
//        /*
//        判断该作者名、书名、简介、标签等字段格式是否需要更新
//        如果需要更新再判断字段的合法性
//        作者名、书名  1-16个字符
//        简介         20-800个字符
//        标签         必须属于tag.txt标签池中的任何一个
//         */
//        if (!author.equals(test.getAuthor())) {
//            //检验作者名是否合法
//            if ((author.length() < 1) || (author.length() > 16)) {
//                logger.warn("作者名格式错误");
//                return "{\"code\":\"001\"}";
//            }
//            test.setAuthor(author);
//        }
//        if (!bookName.equals(test.getBookName())) {
//            //检验书名是否合法
//            if ((bookName.length() < 1) || (bookName.length() > 16)) {
//                logger.warn("书名格式错误");
//                return "{\"code\":\"010\"}";
//            }
//            test.setBookName(bookName);
//        }
//        if (!brief.equals(test.getBrief())) {
//            //检验简介是否合法
//            if ((brief.length() < 20) || (brief.length() > 800)) {
//                logger.warn("简介格式错误");
//                return "{\"code\":\"011\"}";
//            }
//            test.setBrief(brief);
//        }
//        if (!tag.equals(test.getTag())) {
//            //检验标签是否合法
//            if (checkTag(tag) == 0) {
//                logger.warn("标签格式错误");
//                return "{\"code\":\"100\"}";
//            }
//            test.setTag(tag);
//        }
//
//        System.out.println(JSON.toJSONString(test));
//        Test newTest = testService.saveBook(test);
//        System.out.println(JSON.toJSONString(newTest));
//        logger.info("书信息更新成功");
//        return "{\"code\":\"111\"}";
//    }
//
//
//
//    /*
//    检验标签是否合法
//    合法会返回1
//    其他情况都是不合法直接转发到前端即可
//     */
//    private Integer checkTag(String tag) {
//        HashMap<Integer, String> tags = FileUtil.fileToArr(new File("tag.txt"));
//
//        for (int raw = 1;raw <= tags.size();raw++) {
//            if (tags.get(raw).equalsIgnoreCase(tag)) {
//                return 1;
//            }
//        }
//
//        logger.warn("标签格式错误");
//        return 0;
//    }
//
//


}
