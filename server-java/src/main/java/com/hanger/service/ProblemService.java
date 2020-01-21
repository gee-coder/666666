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

import java.util.List;

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

    //添加新问题
    public Problem addProblem(Problem problem) {
        return this.mongoTemplate.insert(problem,"problem");
    }

    //根据问题id删除问题
    public DeleteResult delProblemByQuestionId(String questionId) {
        Query query = new Query(Criteria.where("questionId").is(questionId));
        return this.mongoTemplate.remove(query, Problem.class, "problem");
    }

    //更新问题基本信息
    public UpdateResult updateProblem(String questionId, Update update) {
        Query query = new Query(Criteria.where("questionId").is(questionId));
        return this.mongoTemplate.updateFirst(query, update, Problem.class, "problem");
    }

    /*
    分页查询所有书
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

    //根据问题id查找问题
    public Problem findProblemByQuestionId(String questionId) {
        Query query = new Query(Criteria.where("questionId").is(questionId));
        return this.mongoTemplate.findOne(query, Problem.class, "problem");
    }


}
