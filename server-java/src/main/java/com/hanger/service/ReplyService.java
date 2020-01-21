package com.hanger.service;

import com.hanger.entity.Problem;
import com.hanger.entity.Reply;
import com.mongodb.client.result.DeleteResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author hanger
 * 2020-01-20 13:41
 *
 * 回答的增删查
 */

@Service
public class ReplyService {

    private final MongoTemplate mongoTemplate;

    @Autowired
    public ReplyService(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    //添加新回答
    public Reply addReply(Reply reply) {
        return this.mongoTemplate.insert(reply,"reply");
    }

    //通过回答的id删除回答
    public DeleteResult delReplyByAnswerId(String answerId) {
        Query query = new Query(Criteria.where("answerId").is(answerId));
        return this.mongoTemplate.remove(query, Reply.class, "reply");
    }

    /*
    分页查询所有书
    limit()指定查询结果数量
    skip()指定查询偏移量
    sort()实现查询结果排序
    1表示使用升序排列，-1表示降序排序
     */
    public List<Reply> findReplyByPage(Integer pageNum, Integer pageSize) {
        //pageNum为要查询的页数,pageSize为每页的记录条数
        Pageable pageable = PageRequest.of(pageNum, pageSize);
        Query query = new Query();
        return this.mongoTemplate.find(query.with(pageable), Reply.class,"reply");
    }


}
