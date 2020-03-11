package com.hanger.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * @author hanger
 * 2020-01-20 13:31
 */

@Document(collection="reply")
public class Reply {

    @Id
    //_id让mongodb自动生成
    private String answerId;
    //问题id
    private String questionId;
    //作答结果
    private String answer;
    //系统打分分值
    private Integer systemScore;
    //人工打分分值
    private Integer score;

    public Reply() {
    }

    public Reply(String questionId, String answer, Integer systemScore, Integer score) {
        this.questionId = questionId;
        this.answer = answer;
        this.systemScore = systemScore;
        this.score = score;
    }

    public String getAnswerId() {
        return answerId;
    }

    public void setAnswerId(String answerId) {
        this.answerId = answerId;
    }

    public String getQuestionId() {
        return questionId;
    }

    public void setQuestionId(String questionId) {
        this.questionId = questionId;
    }

    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
    }

    public Integer getSystemScore() {
        return systemScore;
    }

    public void setSystemScore(Integer systemScore) {
        this.systemScore = systemScore;
    }

    public Integer getScore() {
        return score;
    }

    public void setScore(Integer score) {
        this.score = score;
    }

    @Override
    public String toString() {
        return "Reply{" +
                "answerId='" + answerId + '\'' +
                ", questionId='" + questionId + '\'' +
                ", answer='" + answer + '\'' +
                ", systemScore=" + systemScore +
                ", score=" + score +
                '}';
    }
}
