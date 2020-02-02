package com.hanger.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;


/**
 * @author hanger
 * 2020-01-20 13:31
 */

@Document(collection="problem")
public class Problem {

    @Id
    //_id让mongodb自动生成
    private String questionId;
    //题目
    private String question;
    //标准答案
    private String standardAnswer;
    //得分点关键字
    private String[] scoringPoint;


    public Problem() {
    }

    public Problem(String question, String standardAnswer, String[] scoringPoint) {
        this.question = question;
        this.standardAnswer = standardAnswer;
        this.scoringPoint = scoringPoint;
    }

    public Problem(String questionId, String question, String standardAnswer, String[] scoringPoint) {
        this.questionId = questionId;
        this.question = question;
        this.standardAnswer = standardAnswer;
        this.scoringPoint = scoringPoint;
    }

    public String getQuestionId() {
        return questionId;
    }

    public void setQuestionId(String questionId) {
        this.questionId = questionId;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String getStandardAnswer() {
        return standardAnswer;
    }

    public void setStandardAnswer(String standardAnswer) {
        this.standardAnswer = standardAnswer;
    }

    public String[] getScoringPoint() {
        return scoringPoint;
    }

    public void setScoringPoint(String[] scoringPoint) {
        this.scoringPoint = scoringPoint;
    }

}
