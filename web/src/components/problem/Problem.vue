<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/test' }">数据总览</el-breadcrumb-item>
      <el-breadcrumb-item>题目管理</el-breadcrumb-item>
      <el-breadcrumb-item>题目列表</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片视图区 -->
    <el-card>
      <!-- 搜索与附加功能区 -->
      <el-row :gutter="60">
        <el-col :span="8">
          <el-input
          placeholder="请输入题目或标准答案的相关字"
          v-model="query"
          clearable
					@clear="handleFindAllProblems"
					@change="handleFindLikes">
            <el-button
            slot="append"
            icon="el-icon-search"
						@click="handleFindLikes">搜索</el-button>
          </el-input>
        </el-col>
      </el-row>
			
      <!-- 题目列表区 -->
      <el-table
      :data="problemList"
      stripe
      show-overflow-tooltip>
      <el-table-column label="题目ID" prop="questionId"></el-table-column>
      <el-table-column label="题目" prop="question"></el-table-column>
      <el-table-column label="标准答案" width="120px">
				<template slot-scope="standardAnswerScope">
				  <el-tooltip
				  effect="light"
				  content="点击查看"
				  placement="top"
				  :enterable="false">
					<el-button
					type="text"
					@click="openStandardAnswer(standardAnswerScope.row.standardAnswer)">标准答案</el-button>
				  </el-tooltip>
				</template>
			</el-table-column>
      <el-table-column label="得分点" width="120px">
				<template slot-scope="scoringPointScope">
				  <el-tooltip
				  effect="light"
				  content="点击查看"
				  placement="top"
				  :enterable="false">
					<el-button
					type="text"
					@click="openScoringPoint(scoringPointScope.row.scoringPoint)">得分点</el-button>
				  </el-tooltip>
				</template>
			</el-table-column>
      <el-table-column label="操作" width="120px">
        <template slot-scope="operationScope">
          <el-tooltip
          effect="light"
          content="修改该题目信息"
          placement="top"
          :enterable="false">
            <el-button
            size="mini"
            type="warning"
            icon="el-icon-edit"
						@click="editProblem(operationScope.row)"></el-button>
          </el-tooltip>
          <el-tooltip
          effect="light"
          content="删除该题目"
          placement="top"
          :enterable="false">
            <el-button
            size="mini"
            type="danger"
            icon="el-icon-delete"
						@click="delProblem(operationScope.row.questionId)"></el-button>
          </el-tooltip>
        </template>
      </el-table-column>
      </el-table>
			
      <!-- 分页区 -->
      <el-pagination
      @size-change="sizeChange"
      @current-change="currentChange"
      :current-page="currentPage"
      :page-sizes="[6, 8, 10, 12]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total">
      </el-pagination>
    </el-card>
		
		<!-- 得分点详细信息对话框区 -->
		<el-dialog
		  title="得分点详细"
		  :visible.sync="showScoringPointView"
		  width="35%">
		  <!-- 得分点详细信息对话框内容区 -->
			<el-tag
			:key="tag"
			v-for="tag in form.scoringPoint">
			{{tag}}
			</el-tag>
		  <!-- 得分点详细信息对话框底部区 -->
		  <span slot="footer">
		    <el-button type="primary" @click="showScoringPointView = false">确 定</el-button>
		  </span>
		</el-dialog>
		
		<!-- 修改题目信息对话框区 -->
		<el-dialog
		  title="修改题目信息"
		  :visible.sync="showEditView"
		  width="35%">
		  <!-- 修改题目信息对话框内容区 -->
		  <el-form
		  :model="form"
		  :rules="rules"
		  label-width="100px"
		  ref="formRef">
		    <el-form-item label="题目:" prop="question">
		      <el-input
					type="textarea"
					autosize
					v-model="form.question"
					placeholder="请输入题目"></el-input>
		    </el-form-item>
		    <el-form-item label="标准答案:" prop="standardAnswer">
		      <el-input
					type="textarea"
					autosize
					v-model="form.standardAnswer"
					placeholder="请输入标准答案"></el-input>
		    </el-form-item>
				<el-form-item label="得分点:" prop="scoringPoint">
					<el-tag
					:key="tag"
					v-for="tag in form.scoringPoint"
					closable
					@close="handleClose(tag)"
					hit>
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
		  </el-form>
		  <!-- 修改题目信息对话框底部区 -->
		  <span slot="footer" class="dialog-footer">
		    <el-button @click="showEditView = false">取 消</el-button>
		    <el-button type="primary" @click="handleEditProblem">确 定</el-button>
		  </span>
		</el-dialog>
		
  </div>
</template>

<script>
	import {
	  findAllProblems,
	  deleteProblem,
	  alterProblem,
	  findLikes
	  } from "network/problem.js"

  export default {
    name: 'problem',
    data() {
      return {
				//新添得分点标签的输入框是否可见
				inputVisible: false,
				//新添得分点标签的输入框可见的时候对应的初始值
				inputValue: '',
				//暂存当前查看详细、修改涉及的表单数据
				form: {
					questionId: '',
				  question: '',
				  standardAnswer: '',
				  scoringPoint: []
				},
        //控制修改题目弹框是否可见的数据
        showEditView: false,
				//控制得分点详细信息弹框是否可见的数据
				showScoringPointView: false,
        //保存当前页面记录条数的数据
        pageSize: 6,
        //保存当前页号的数据
        currentPage: 1,
        //保存当前数据库总记录数的数据
        total: 0,
        //保存当前页面的题目信息的数据
        problemList: [],
        //保存搜索框内当前查询条件的数据
        query: '',
				//每一步涉及的表单数据的本地校验规则
				rules: {
				  question: [
				    { required: true, message: '请输入题目', trigger: 'blur' },
				    { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
				  ],
				  standardAnswer: [
				    { required: true, message: '请输入标准答案', trigger: 'blur' },
				    { min: 1, max: 255, message: '长度在 1 到 255 个字符', trigger: 'blur' }
				  ],
				  scoringPoint: [
				    { type: 'array', required: true, message: '请至少保留一个得分点', trigger: 'change' },
				  ]
				}
      }
    },
		created() {
		  //在当前组件创建完毕时就异步调用handleFindAllProblems
		  this.handleFindAllProblems()
		},
    methods: {
			/*根据数据模型当中的当前页面大小pageSize和
			当前页码currentPage发送查询第currentPage页
			每页pageSize条数据的请求*/
			handleFindAllProblems() {
			  findAllProblems({
			    pageSize: this.pageSize,
			    pageNum: this.currentPage
			  }).then(res => {
			    if(res.status !== 200) {
			        return this.$message.error('请求失败！')
			    } else {
			      if(res.data.code === "000") {
			          return this.$message.error('请求参数格式错误！')
			      }
			      this.total = res.data.total
			      this.problemList = res.data.info
			    }
			  }).catch(err => {
			  console.log(err)
			  return this.$message.error('请求失败！')
			  })
			},
			//通过数据模型中的查询条件query查询当前id
			handleFindLikes() {
			  if (this.query === '') {
			    return ;
			  }
			  findLikes({
			    search: this.query,
			  }).then(res => {
			    if(res.status !== 200) {
			        return this.$message.error('请求失败！')
			    } else {
			      if(res.data.code === "000") {
			          return this.$message.error('请求参数格式错误！')
			      }
			      this.total = res.data.total
			      this.problemList = res.data.info
			    }
			  }).catch(err => {
			  console.log(err)
			  return this.$message.error('请求失败！')
			  })
			},
			//当页面大小pageSize被改变时重新调用handleFindAllProblems
			sizeChange(val) {
			  this.pageSize = val
			  this.handleFindAllProblems()
			},
			//当页码currentPage被改变时重新调用handleFindAllProblems
			currentChange(val) {
			  this.currentPage = val
			  this.handleFindAllProblems()
			},
			//弹出标准答案详细内容的对话框
			openStandardAnswer(standardAnswer) {
			  this.$alert(standardAnswer, '标准答案', {
			    confirmButtonText: '确定',
			    callback: action => {
			    }
			  });
			},
			//弹出得分点详细内容的对话框
			openScoringPoint(scoringPoint) {
			  this.showScoringPointView = true
			  this.form.scoringPoint = scoringPoint
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
			},
			/*当点击修改按钮时调用该函数
			将数据模型中控制弹窗视图是否可见的布尔值showEditView改为true
			同时把通过scope属性的scope.row获取当前行的DOM节点row
			渲染到数据模型form中，该函数并不负责真正的修改
			*/
			editProblem(row) {
			  this.showEditView = true
				this.form.questionId = row.questionId
			  this.form.question = row.question
			  this.form.standardAnswer = row.standardAnswer
			  this.form.scoringPoint = row.scoringPoint
			},
			/*当点击修改的弹窗视图中的确认按钮时调用该函数
			将showEditView改为false隐藏弹窗
			同时把数据模型form中修改过的当前属性值提交到服务端保存
			*/
			handleEditProblem() {
			  this.$refs.formRef.validate((valid) => {
			    if (valid) {
			      this.showEditView = false
			      alterProblem({
			        questionId: this.form.questionId,
			        question: this.form.question,
			        standardAnswer: this.form.standardAnswer,
			        scoringPoint: this.form.scoringPoint
			      }).then(res => {
			        console.log(res)
			        if(res.status !== 200) {
			            return this.$message.error('请求失败！')
			        } else {
			          if(res.data.code === "111") {
			            this.$message.success('修改题目信息成功！')
			            //修改用户成功后刷新当前页面
			            this.handleFindAllProblems()
			            return ;
			          } else if(res.data.code === "000") {
			            return this.$message.error('请求参数格式错误！')
			          } else if(res.data.code === "101") {
			            return this.$message.error('该题目不存在！')
			          }
			        }
			      }).catch(err => {
			      console.log(err)
			      return this.$message.error('请求失败！')
			      })
			    } else {
			      return this.$message.error('请按要求填写完再提交！')
			    }
			  });
			},
			/*点击删除按钮执行该函数从而展示出删除对话框
			点击删除提示框中的确认按钮后执行该删除操作函数
			*/
			delProblem(id) {
			  this.$confirm('是否删除该题目及其相关作答记录？', '提示', {
			    confirmButtonText: '确定',
			    cancelButtonText: '取消',
			    type: 'warning'
			  }).then(() => {
			    deleteProblem({
			      questionId: id
			    }).then(res => {
			      console.log(res)
			      if(res.status !== 200) {
			        this.$message.error('请求失败！')
			      } else {
			        if(res.data.code === "111") {
			          this.$message.success('删除成功！')
			          //删除成功后刷新当前页面
			          this.handleFindAllProblems()
			        } else if(res.data.code === "000") {
			          this.$message.error('请求参数格式错误！')
			        } else if(res.data.code === "404") {
			          this.$message.error('数据库执行失败！')
			        }
			      }
			    }).catch(err => {
			    console.log(err)
			     this.$message.error('请求失败！')
			    })
			  }).catch(() => {
			    //关闭取消后的提示
			    // this.$message.info('已取消删除！')
			  });
			},
    }
  }
</script>

<style lang="less" scoped>
</style>
