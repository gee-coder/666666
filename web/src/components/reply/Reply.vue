<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/test' }">数据总览</el-breadcrumb-item>
      <el-breadcrumb-item>作答管理</el-breadcrumb-item>
      <el-breadcrumb-item>作答列表</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 卡片视图区 -->
    <el-card>
      <!-- 搜索与附加功能区 -->
      <el-row :gutter="60">
        <el-col :span="8">
          <el-input
          placeholder="请输入作答的相关字"
          v-model="query"
          clearable
          @clear="handleFindAllReplys"
          @change="handleFindLikes">
            <el-button
            slot="append"
            icon="el-icon-search"
						@click="handleFindLikes">搜索</el-button>
          </el-input>
        </el-col>
      </el-row>
			
      <!-- 列表区 -->
      <el-table
      :data="replyList"
      border
      show-overflow-tooltip>
			<el-table-column label="#" type="index"></el-table-column>
      <el-table-column label="作答ID" prop="answerId"></el-table-column>
      <el-table-column label="题目ID" prop="questionId"></el-table-column>
      <el-table-column label="作答结果" width="120px">
				<template slot-scope="answerScope">
				  <el-tooltip
				  effect="light"
				  content="点击查看"
				  placement="top"
				  :enterable="false">
					<el-button
					type="text"
					@click="openAnswer(answerScope.row.answer)">点击查看</el-button>
				  </el-tooltip>
				</template>
			</el-table-column>
      <el-table-column label="系统打分" prop="systemScore"></el-table-column>
      <el-table-column label="人工打分" prop="score"></el-table-column>
      <el-table-column label="操作" width="121px">
        <template slot-scope="operationScope">
          <el-tooltip
          effect="light"
          content="删除该答题记录"
          placement="top"
          :enterable="false">
            <el-button
            size="mini"
            type="danger"
            icon="el-icon-delete"
						@click="delReply(operationScope.row.answerId)"></el-button>
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
  </div>
</template>

<script>
	import {
	  findAllReplys,
	  deleteReply,
	  findLikes
	  } from "network/reply.js"

  export default {
    name: 'reply',
    data() {
      return {
        //渲染修改用户弹框的数据
        form: {
          answerId: '',
          questionId: '',
          answer: '',
          systemScore: 0,
          score: 0
        },
        //保存当前页面记录条数的数据
        pageSize: 6,
        //保存当前页号的数据
        currentPage: 1,
        //保存当前数据库总记录数的数据
        total: 0,
        //保存当前页面的用户信息的数据
        replyList: [],
        //保存搜索框内当前查询条件的数据
        query: '',
      }
    },
		created() {
		  //在当前组件创建完毕时就异步调用handleFindAllProblems
		  this.handleFindAllReplys()
		},
    methods: {
			handleFindAllReplys() {
				findAllReplys({
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
				    this.replyList = res.data.info
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
			      this.replyList = res.data.info
			    }
			  }).catch(err => {
			  console.log(err)
			  return this.$message.error('请求失败！')
			  })
			},
      //当页面大小pageSize被改变时重新调用
      sizeChange(val) {
        this.pageSize = val
        this.handleFindAllReplys()
      },
      //当页码currentPage被改变时重新调用
      currentChange(val) {
        this.currentPage = val
        this.handleFindAllReplys()
      },
			//弹出标准答案详细内容的对话框
			openAnswer(answer) {
			  this.$alert(answer, '作答结果', {
			    confirmButtonText: '确定',
			    callback: action => {
			    }
			  });
			},
			/*点击删除按钮执行该函数从而展示出删除对话框
			点击删除提示框中的确认按钮后执行该删除操作函数
			*/
			delReply(id) {
			  this.$confirm('是否删除该作答记录？', '提示', {
			    confirmButtonText: '确定',
			    cancelButtonText: '取消',
			    type: 'warning'
			  }).then(() => {
			    deleteReply({
			      answerId: id
			    }).then(res => {
			      console.log(res)
			      if(res.status !== 200) {
			        this.$message.error('请求失败！')
			      } else {
			        if(res.data.code === "111") {
			          this.$message.success('删除成功！')
			          //删除成功后刷新当前页面
			          this.handleFindAllReplys()
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
  /*给搜索与附加功能区添加下边距*/
  .el-row {
    margin-bottom: 20px;
  }

</style>
