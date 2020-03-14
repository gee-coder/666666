<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/test' }">数据总览</el-breadcrumb-item>
      <el-breadcrumb-item>题目管理</el-breadcrumb-item>
      <el-breadcrumb-item>添加题目</el-breadcrumb-item>
    </el-breadcrumb>


		<!-- 卡片视图区 -->
		<el-card>
      <!-- 步骤条区 -->
		  <el-steps :space="200" :active="(activeIndex - 0 === 3) ? 4 : (activeIndex - 0)" finish-status="success">
		    <el-step title="题目"></el-step>
		    <el-step title="标准答案"></el-step>
        <el-step title="得分点"></el-step>
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
        <el-tab-pane label="题目" name="0">
          <el-form-item label="题目:" prop="question">
            <el-input
						type="textarea"
						rows="6"
						v-model="form.question"
						placeholder="请输入题目"
						maxlength="255"
						show-word-limit></el-input>
          </el-form-item>
        </el-tab-pane>
        <el-tab-pane label="标准答案" name="1">
          <el-form-item label="标准答案:" prop="standardAnswer">
            <el-input
						type="textarea"
						rows="6"
						v-model="form.standardAnswer"
						placeholder="请输入标准答案"
						maxlength="255"
						show-word-limit></el-input>
          </el-form-item>
        </el-tab-pane>
        <el-tab-pane label="得分点" name="2">
          <el-form-item label="得分点:" prop="scoringPoint">
						<el-tag
					  :key="tag"
					  v-for="tag in form.scoringPoint"
					  closable
					  @close="handleClose(tag)"
						hit
						:type="tagColor[form.scoringPoint.indexOf(tag) % 5]">
					  {{tag}}
						</el-tag>
					  <el-input
					  class="input-new-tag"
					  v-if="inputVisible"
					  v-model="inputValue"
					  ref="saveTagInput"
					  size="small"
					  @keyup.enter.native="handleInputConfirm"
					  @blur="handleInputConfirm"
						maxlength="99"
						show-word-limit>
					  </el-input>
					  <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
          </el-form-item>
        </el-tab-pane>
        <el-tab-pane label="完成" name="3">
					恭喜您！新题目添加成功！
					<el-link type="primary" href="/addProblem">继续添加</el-link>
					</el-tab-pane>
      </el-tabs>
      </el-form>
		</el-card>
  </div>
</template>

<script>
	import {
	  addProblem,
	  } from "network/problem.js"
	
  export default {
    name: 'addProblem',
    data() {
      return {
        //步骤的索引数据，从0开始
        activeIndex: '0',
        //暂存当前页面涉及的表单数据
        form: {
          question: '',
          standardAnswer: '',
          scoringPoint: []
        },
				//新添得分点标签的输入框是否可见
				inputVisible: false,
				//新添得分点标签的输入框可见的时候对应的初始值
				inputValue: '',
				//标签的颜色
				tagColor: ['', 'success', 'info', 'danger', 'warning'],
				//每一步涉及的表单数据的本地校验规则
				rules: {
				  question: [
				    { required: true, message: '请输入题目', trigger: 'blur' },
				    { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
				  ],
				  standardAnswer: [
				    { required: true, message: '请输入标准答案', trigger: 'blur' },
				    { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
				  ]
				}
      }
    },
    methods: {
      //判断对应索引的标签页内是否有合法值
      haveValue(index) {
        console.log('index:' + index)
        if(index === '0') {
          if((this.form.question.length >= 1) && (this.form.question.length <= 255)) {
						return true;
					} else {
						this.$message.error('请输入题目！')
						return false;
					}
        } else if(index === '1') {
					if((this.form.standardAnswer.length >= 1) && (this.form.standardAnswer.length <= 255)) {
						return true;
					} else {
						this.$message.error('请输入标准答案！')
						return false;
					}
        } else if(index === '2') {
          if(this.form.scoringPoint.length >= 1) {
          	return true;
          } else {
          	this.$message.error('请至少保留一个得分点！')
          	return false;
          }
        } else {
          return false;
        }
      },
      //在跳转到下一个标签时执行该函数判断是否满足跳转条件
      beforeTabChange(newIndex, oldIndex) {
        if ((newIndex - oldIndex === 1) && (this.haveValue(oldIndex))) {
					if (oldIndex === '1') {
						return true;
					} else if (oldIndex === '2') {
						//提交最终表单
						addProblem({
							question: this.form.question,
							standardAnswer: this.form.standardAnswer,
							scoringPoint: this.form.scoringPoint
						}).then(res => {
							console.log(res)
							if(res.status !== 200) {
								this.$message.error('请求失败！')
								return false; 
							} else {
								if(res.data.code === "111") {
									this.$message.success('新题添加成功！')
									return true;
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
			//关闭标签
			handleClose(tag) {
				this.form.scoringPoint.splice(this.form.scoringPoint.indexOf(tag), 1);
			},
			//显示输入标签的输入框
			showInput() {
				this.inputVisible = true;
				this.$nextTick(_ => {
					this.$refs.saveTagInput.$refs.input.focus();
				});
			},
			//处理输入确认按钮
			handleInputConfirm() {
				let inputValue = this.inputValue;
				if (inputValue) {
					this.form.scoringPoint.push(inputValue);
				}
				this.inputVisible = false;
				this.inputValue = '';
			}
    }
  }
</script>

<style lang="less" scoped>
	
  /*固定表单的宽度*/
  .el-form-item {
    width: 390px;
  }

  /*标签页的上边距*/
  .el-tab-pane {
    margin-top: 20px;
  }
	
</style>
