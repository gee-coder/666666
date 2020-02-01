<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/test' }">测试</el-breadcrumb-item>
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
          clearable>
            <el-button
            slot="append"
            icon="el-icon-search">搜索</el-button>
          </el-input>
        </el-col>
      </el-row>
			
      <!-- 用户列表区 -->
      <el-table
      :data="replyList"
      border
      show-overflow-tooltip>
      <el-table-column label="作答ID" prop="answerId"></el-table-column>
      <el-table-column label="题目ID" prop="questionId"></el-table-column>
      <el-table-column label="作答结果" prop="answer"></el-table-column>
      <el-table-column label="系统给分" prop="systemScore"></el-table-column>
      <el-table-column label="得分描述" prop="scoringDetailed"></el-table-column>
      <el-table-column label="操作" width="121px">
        <template slot-scope="operationScope">
          <el-tooltip
          effect="light"
          content="删除该用户"
          placement="top"
          :enterable="false">
            <el-button
            size="mini"
            type="danger"
            icon="el-icon-delete"></el-button>
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
          systemScore: '',
          scoringDetailed: ''
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
    methods: {
      //当页面大小pageSize被改变时重新调用handleFindAllUsers
      sizeChange(val) {
        this.pageSize = val
        this.handleFindAllUsers()
      },
      //当页码currentPage被改变时重新调用handleFindAllUsers
      currentChange(val) {
        this.currentPage = val
        this.handleFindAllUsers()
      }
    }
  }
</script>

<style lang="less" scoped>
  /*给搜索与附加功能区添加下边距*/
  .el-row {
    margin-bottom: 20px;
  }

</style>
