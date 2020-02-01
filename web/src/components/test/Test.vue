<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item>测试区</el-breadcrumb-item>
    </el-breadcrumb>
    
    <!-- 卡片视图区 -->
    <el-card>
			<el-divider><i class="el-icon-data-line"></i>数据总览</el-divider>
			<span>这里准备放echarts的组件，总括数据</span>
			<el-divider><i class="el-icon-edit"></i>答题测试</el-divider>
			
				<el-form
				label-position="top"
				label-width="80px"
				:model="form"
				ref="formRef">
				<el-form-item class="item_problem">
					<div>
						<el-tooltip
						effect="light"
						content="换一题"
						placement="top"
						:enterable="false">
						<el-button
						type="warning"
						icon="el-icon-refresh"
						circle
						@click="handleGetARandomProblem()"></el-button>
						</el-tooltip>
						{{form.problem.question}}
					</div>
				</el-form-item>
				<el-form-item class="item_answer" prop="answer">
					<el-input
					type="textarea"
					rows="6"
					v-model="form.answer"
					placeholder="请输入你的答案"
					maxlength="255"
					show-word-limit></el-input>
					<el-button type="primary">提交</el-button>
				</el-form-item>
				</el-form>
			
    </el-card>
  </div>
</template>

<script>
	import {
	  getARandomProblem
	  } from "network/problem.js"
	
	
  export default {
    name: 'test',
    data() {
      return {
				//暂存当前页面涉及的表单数据
				form: {
					problem: {
						questionId: '',
						question: '',
						standardAnswer: '',
						scoringPoint: []
					},
					answer: '',
					systemScore: -1,
					scoringDetailed: '',
				},
				
      }
    },
		created() {
		  //在当前组件创建完毕时就异步调用该方法
		  this.handleGetARandomProblem()
		},
    methods: {
			//随机获取一道题
			handleGetARandomProblem() {
			  getARandomProblem().then(res => {
			    if(res.status !== 200) {
			        return this.$message.error('请求失败！')
			    } else {
			      this.form.problem.questionId = res.data.questionId
			      this.form.problem.question = res.data.question
						this.form.problem.standardAnswer = res.data.standardAnswer
						this.form.problem.scoringPoint = res.data.scoringPoint
			    }
			  }).catch(err => {
			  console.log(err)
			  return this.$message.error('请求失败！')
			  })
			},
			
    }
  }
</script>

<style lang="less" scoped="scoped">
	
	/*固定表单的宽度*/
	.el-form-item {
	  width: 50%;
	}
	
	
	/*题目表单项左对齐*/
	.item_problem {
		text-align: left;
		div {
			font-family: "lucida console";
			font-size: 20px;
		}
		
		.el-button {
			//按钮右边距10px
			margin-right: 10px;
		}
	}
	
	
  /*作答表单项右对齐*/
  .item_answer {
		text-align: right;
		
		.el-button {
			//按钮上边距20px
			margin-top: 10px;
		}
  }
	
</style>
