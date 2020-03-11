<template>
	<div>
		<!-- 面包屑导航区 -->
		<el-breadcrumb separator-class="el-icon-arrow-right">
		  <el-breadcrumb-item :to="{ path: '/test' }">数据总览</el-breadcrumb-item>
		  <el-breadcrumb-item>作答管理</el-breadcrumb-item>
		  <el-breadcrumb-item>添加作答</el-breadcrumb-item>
		</el-breadcrumb>
		
		<!-- 卡片视图区 -->
		<el-card>
			<!-- 步骤条区 -->
			<el-steps :space="200" :active="(activeIndex - 0 === 2) ? 3 : (activeIndex - 0)" finish-status="success">
			  <el-step title="抽题&作答"></el-step>
			  <el-step title="系统&人工"></el-step>
			  <el-step title="完成"></el-step>
			</el-steps>
			
			<!-- tab侧栏区 -->
			<el-form
			label-position="top"
			label-width="80px"
			:model="form"
			:rules="rules"
			ref="formRef">
			<el-tabs
			:tab-position="'left'"
			v-model="activeIndex"
			:before-leave="beforeTabChange">
			  <el-tab-pane label="抽题&作答" name="0">
					<h3>
			    		<el-tooltip
			    		effect="light"
			    		content="换一题"
			    		placement="top"
			    		:enterable="false">
			    		<el-button
			    		type="warning"
			    		icon="el-icon-refresh"
			    		circle
			    		@click="handleGetARandomProblem"></el-button>
			    		</el-tooltip>
			    		{{form.problem.question}}
			    	</h3>
			    <el-form-item prop="answer">
						<el-input
						type="textarea"
						rows="6"
						v-model="form.answer"
						placeholder="请输入你的答案"
						maxlength="255"
						show-word-limit></el-input>
			    </el-form-item>
			  </el-tab-pane>
			  <el-tab-pane label="机器&人工" name="1">
					<span class="demonstration">机器打分</span>
					<el-rate
					disabled
					:max="10"
					v-model="form.systemScore"
					:colors="colors"
					show-score
					text-color="#ff9900"
					score-template="{value}分"></el-rate>
					<el-form-item class="socre_form">
						<span class="demonstration">人工打分</span>
						<el-button size="mini" type="warning" @click="setZero">0 分</el-button>
						<el-rate
						:max="10"
						v-model="form.score"
						:colors="colors"
						show-score
						text-color="#ff9900"
						score-template="{value}分"></el-rate>
					</el-form-item>
			  </el-tab-pane>
			  <el-tab-pane label="完成" name="2">
					恭喜您！新题目添加成功！
					<el-link type="primary" href="/addReply">继续添加</el-link>
					</el-tab-pane>
			</el-tabs>
			</el-form>
			
		</el-card>
	</div>
</template>

<script>
	import {
	  getARandomProblem
	} from "network/problem.js"
	
	import {
		getSystemScore,
		addReply
	} from "network/reply.js"
	
	
	export default {
	  name: 'addReply',
	  data() {
	    return {
				//步骤的索引数据，从0开始
				activeIndex: '0',
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
					score: -1,
				},
				colors: {
						3: '#99A9BF',
						6: { value: '#F7BA2A'},
						10: '#FF9900'
				},
				//每一步涉及的表单数据的本地校验规则
				rules: {
				  answer: [
				    { required: true, message: '请输入答案', trigger: 'blur' },
				    { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
				  ]
				}
	    }
	  },
		created() {
			//在当前组件创建完毕时就异步调用该方法
			this.handleGetARandomProblem()
		},
	  methods: {
			//判断对应索引的标签页内是否有合法值
			haveValue(index) {
			  // console.log('index:' + index)
			  if(index === '0') {
			    if((this.form.problem.question.length > 0) && (this.form.answer.length > 0) && (this.form.answer.length <= 255)) {
						return true;
					} else {
						this.$message.error('请输入答案！')
						return false;
					}
			  } else if(index === '1') {
					if((this.form.systemScore > -1) && (this.form.score > -1)) {
						return true;
					} else {
						this.$message.error('请进行人工打分！')
						return false;
					}
			  } else {
			    return false;
			  }
			},
			//在跳转到下一个标签时执行该函数判断是否满足跳转条件
			beforeTabChange(newIndex, oldIndex) {
			  if ((newIndex - oldIndex === 1) && (this.haveValue(oldIndex))) {
					if (oldIndex === '0') {
						//获取系统打分结果
						getSystemScore({
							questionId: this.form.problem.questionId,
							answer: this.form.answer
						}).then(res => {
							if(res.status !== 200) {
								this.$message.error('请求失败！')
								return false;
							} else {
								if(res.data.code === "111") {
									this.$message.success('获取系统打分结果成功！')
									this.form.systemScore = res.data.systemScore;
									return true;
								} else if(res.data.code === "101") {
									this.$message.error('该题目不存在！')
									return false;
								} else if(res.data.code === "001") {
									this.$message.error('python接口请求失败！')
									return false;
								} else if(res.data.code === "000") {
									this.$message.error('请求参数格式错误！')
									return false;
								}
							}
						}).catch(err => {
						console.log(err)
						this.$message.error('请求失败！')
						return false;
						})
					} else if (oldIndex === '1') {
						//提交最终作答记录
						addReply({
							questionId: this.form.problem.questionId,
							answer: this.form.answer,
							systemScore: this.form.systemScore,
							score: this.form.score
						}).then(res => {
							if(res.status !== 200) {
								this.$message.error('请求失败！')
								return false; 
							} else {
								if(res.data.code === "111") {
									this.$message.success('作答记录添加成功！')
									return true;
								} else if(res.data.code === "101") {
									this.$message.error('该题目不存在！')
									return false;
								} else if(res.data.code === "000") {
									this.$message.error('请求参数格式错误！')
									return false;
								}
							}
						}).catch(err => {
						console.log(err)
						this.$message.error('请求失败！')
						return false;
						})
					} else {
						return true;
					}
			  } else {
			    return false;
			  }
			},
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
			//设置为0分
			setZero() {
				this.form.score = 0;
			},
	  }
	}
</script>

<style lang="less" scoped="scoped">
	/*固定表单的宽度*/
	.el-form-item {
	  width: 390px;
	}
	
	/*标签页的上边距*/
	.el-tab-pane {
	  margin-top: 20px;
	}
	
	/*人工打分的上边距*/
	.socre_form {
		margin-top: 20px;
		
		.el-button {
			margin-left: 20px;
		}
	}

</style>
