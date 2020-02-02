package com.hanger.service;

import com.hanger.entity.Problem;
import com.mongodb.client.result.DeleteResult;
import com.mongodb.client.result.UpdateResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Service;

import java.awt.print.Book;
import java.util.List;
import java.util.regex.Pattern;

/**
 * @author hanger
 * 2020-01-20 13:41
 *
 * 问题的增删改查
 */

@Service
public class ProblemService {

    private final MongoTemplate mongoTemplate;

    @Autowired
    public ProblemService(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    //添加新题目
    public Problem addProblem(Problem problem) {
        return this.mongoTemplate.insert(problem,"problem");
    }

    //查询题目总数
    public long getProblemsNum() {
        Query query = new Query();
        return this.mongoTemplate.count(query, Problem.class, "problem");
    }

    /*
    分页查询所有题目
    limit()指定查询结果数量
    skip()指定查询偏移量
    sort()实现查询结果排序
    1表示使用升序排列，-1表示降序排序
     */
    public List<Problem> findProblemByPage(Integer pageNum, Integer pageSize) {
        //pageNum为要查询的页数,pageSize为每页的记录条数
        Pageable pageable = PageRequest.of(pageNum, pageSize);
        Query query = new Query();
        return this.mongoTemplate.find(query.with(pageable), Problem.class,"problem");
    }

    //通过题目和标准答案模糊查询
    public List<Problem> findLikes(String search) {
        //封装查询条件
        Query query = new Query();
        //构建查询条件
        Criteria criteria = new Criteria();
        //查询的正则表达式
        Pattern pattern = Pattern.compile("^.*" + search + ".*$" , Pattern.CASE_INSENSITIVE);
        criteria.orOperator(
                Criteria.where("question").regex(pattern),
                Criteria.where("standardAnswer").regex(pattern));
        query.addCriteria(criteria);
        return this.mongoTemplate.find(query, Problem.class,"problem");
    }

    //更新题目基本信息
    public Problem saveProblem(Problem problem) {
        return this.mongoTemplate.save(problem, "problem");
    }

    //根据题目id查找题目
    public Problem findProblemByQuestionId(String questionId) {
        return this.mongoTemplate.findById(questionId, Problem.class, "problem");
    }

    //根据题目id删除题目
    public DeleteResult delProblemByQuestionId(String questionId) {
        Query query = new Query(Criteria.where("questionId").is(questionId));
        return this.mongoTemplate.remove(query, Problem.class, "problem");
    }

    //获取第randomNumber个记录（从一开始）
    public Problem findTheRandomNumberRecord(long randomNumber) {
        Query query = new Query();
        //从第几条记录开始
        query.skip(randomNumber - 1);
        //取多少条记录
        query.limit(1);
        return this.mongoTemplate.findOne(query, Problem.class, "problem");
    }






}
