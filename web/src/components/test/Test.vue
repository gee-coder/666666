<template>
  <div>
		<el-row>
			<el-col :span="11">
				<el-card>
					<el-divider><i class="el-icon-pie-chart"></i>总览</el-divider>
					<div id="topChartL" :style="{height: '200px'}"></div>
				</el-card>
			</el-col>
			<el-col :span="13">
				<el-card class="right">
					<el-divider><i class="el-icon-data-analysis"></i>误差分布</el-divider>
					<div id="topChartR" :style="{ height: '200px'}"></div>
				</el-card>
			</el-col>
		</el-row>

		<el-row>
			<el-col :span="16">
				<el-card>
					<el-divider><i class="el-icon-data-line"></i>打分表</el-divider>
					<div id="mainChart" :style="{ height: '360px'}"></div>
				</el-card>
			</el-col>
			<el-col :span="8">
				<el-card class="right">
					<el-divider><i class="el-icon-data-board"></i>准确率</el-divider>
					<div id="rightChart" :style="{ height: '360px'}"></div>
				</el-card>
			</el-col>
		</el-row>
	
  </div>
</template>

<script>
	import {
	  initTest
	  } from "network/problem.js"
	
  export default {
    name: 'test',
    data() {
      return {
				color: [
					"#3fb1e3",
					"#a0a7e6",
					"#6be6c1",
					"#96dee8",
					"#c4ebad",
					"#626c91",
				],
				//题目总数
				problemNumber: 0,
				//测试总数
				replyNumber: 0,
				//误差绝对值1-10出现的次数
				errorNumber: [],
				form: {
					//横坐标数据数组
					xIndex: [],
					//系统打分数组
					systemScore: [],
					//人工打分数组
					score: [],
					//对应方差数组
					variance: []
				},
				//准确率
				precisionRate: 0.0
      }
    },
		mounted() {
			this.handleInitTest();
		},
    methods: {
			//获取页面数据
			handleInitTest() {
				initTest().then(res => {
			    if(res.status !== 200) {
			        return this.$message.error('请求失败！')
			    } else {
						console.log(res.data)
			      this.problemNumber = res.data.problemNumber
			      this.replyNumber = res.data.replyNumber
						this.errorNumber = res.data.errorNumber
						this.form.xIndex = res.data.xIndex
						this.form.systemScore = res.data.systemScore
						this.form.score = res.data.score
						this.form.variance = res.data.variance
						this.precisionRate = res.data.precisionRate
						this.drawTopL();
						this.drawTopR();
						this.drawMain();
						this.drawRight();
			    }
			  }).catch(err => {
			  console.log(err)
			  return this.$message.error('请求失败！')
			  })
			},
			drawTopL() {
				// 基于准备好的dom，初始化echarts实例
				let topChartL = this.$echarts.init(document.getElementById('topChartL'))
				// 绘制图表
				topChartL.setOption({
					//图表主题颜色
					color: this.color,
					//提示框
					tooltip: {
						formatter: '总数：{b}',
					},
					title: [
						{
							text: '题目总数',
							left: '25%',
							textAlign: 'center'
						},
						{
							text: '作答总数',
							left: '75%',
							textAlign: 'center'
						}
					],
					series: [
						{
							type: 'pie',
							radius: ['38%', '60%'],
							center: ['25%', '50%'],
							label: {
								normal: {
									show: true,
									position: 'center',
									textStyle: {
										fontSize: '25',
										fontWeight: 'bold'
									}
								}
							},
							data: [{value: 0, name: this.problemNumber}]
						},
						{
							type: 'pie',
							radius: ['38%', '60%'],
							center: ['75%', '50%'],
							label: {
								normal: {
									show: true,
									position: 'center',
									textStyle: {
										fontSize: '25',
										fontWeight: 'bold'
									}
								}
							},
							data: [{value: 0, name: this.replyNumber}]
						}
					]
				});
			},
			drawTopR() {
				// 基于准备好的dom，初始化echarts实例
				let topChartR = this.$echarts.init(document.getElementById('topChartR'))
				// 绘制图表
				topChartR.setOption({
					//图表主题颜色
					color: this.color,
					tooltip: {
						trigger: 'axis',
						axisPointer: {          // 坐标轴指示器，坐标轴触发有效
							type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
						}
					},
					grid: {
						left: '5%',
						right: '15%',
						top: '15%',
						bottom: '5%',
						containLabel: true
					},
					//工具箱，目前官方提供了五种工具
					toolbox: {
						feature: {
							//另存图表为图片
							saveAsImage: {}
						}
					},
					xAxis: {
						name: '误差绝对值',
						type: 'category',
						data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
					},
					yAxis: {
						name: '次数',
						type: 'value'
					},
					series: [
						{
							name: '误差次数',
							type: 'bar',
							barWidth: '50%',
							data: this.errorNumber
						}
					]
				});
			},
			drawMain() {
				// 基于准备好的dom，初始化echarts实例
				let mainChart = this.$echarts.init(document.getElementById('mainChart'))
				// 绘制图表
				mainChart.setOption({
					//图表主题颜色
					color: this.color,
					//图表的标题
					title: {
						//大标题
						text: '系统&人工打分表',
						//子标题
						subtext: '数据来源于实时测试数据',
						//标题位置
						left: 'center'
			    },
					//提示框
			    tooltip: {
						//提示框类型
						trigger: 'axis'
			    },
					//图表的数据项
			    legend: {
						//各个数据项的标题
						data: ['系统打分', '人工打分', '方差'],
						//数据项位置
						left: 10
			    },
					//图表的位置
			    grid: {
						//调整图标位置的值
						left: '5%',
						right: '10%',
						height: '70%',
						//是否把图表涉及的标签与图标看成一个整体移动
						containLabel: true
					},
					//工具箱，目前官方提供了五种工具
			    toolbox: {
						feature: {
							dataZoom: {
								yAxisIndex: 'none'
							},
							//还原初始位置
							restore: {},
							//另存图表为图片
							saveAsImage: {}
						}
			    },
					//设置缩放条
					dataZoom: [{type: 'slider'}],
					//横坐标
			    xAxis: {
						//横坐标标签名
						name: '记录索引',
						//横坐标类型
			      type: 'category',
						//横坐标数据项
			      data: this.form.xIndex
			    },
					//纵坐标
			    yAxis: {
						//纵坐标标签名
						name: '分值',
						//标签名位置
						nameLocation: 'center',
						//纵坐标类型
			      type: 'value'
			    },
					//与legend对应的连续数据集
			    series: [
						{
							//对应legend的名字
							name: '系统打分',
							//数据类型
							type: 'line',
							//具体数据
							data: this.form.systemScore
						},
						{
							//对应legend的名字
							name: '人工打分',
							//数据类型
							type: 'scatter',
							//具体数据
							data: this.form.score
						},
            {
							name: '方差',
							type: 'bar',
							//柱形图的柱宽
							barWidth: 30,
							//柱子样式
							itemStyle: {
								//柱子圆角
								barBorderRadius: 2
							},
							data: this.form.variance
            }],
				});
			},
			drawRight() {
				// 基于准备好的dom，初始化echarts实例
				let rightChart = this.$echarts.init(document.getElementById('rightChart'))
				// 绘制图表
				rightChart.setOption({
					//提示框
					tooltip: {
						formatter: '{a} <br/>{b} : {c}%',
					},
					toolbox: {
						feature: {
							saveAsImage: {}
						}
					},
					series: [
						{
							name: '系统打分',
							type: 'gauge',
							detail: {formatter: '{value}%'},
							data: [
								{
									value: this.precisionRate,
									name: '准确率'
								}
							]
						}
					]
				});
			}
			
    }
  }
</script>

<style lang="less" scoped="scoped">
	.right {
		margin-left: 10px;
	}
	  
	 

	
</style>
