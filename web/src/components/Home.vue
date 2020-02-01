<template>
  <el-container class="home_container">
    <!-- 头部区 -->
    <el-header>
      <div>
        <img src="~img/logo.png" alt=""></img>
        <span>文本识别测试系统</span>
      </div>
    </el-header>
    <!-- 主体区 -->
    <el-container>
      <!-- 侧边区 -->
      <el-aside :width="isCollapse ? '64px' : '200px'">
        <!-- 侧边区的折叠按钮 -->
        <div class="toggle_button" @click="handleToggle">|||</div>
        <!-- 侧边区的菜单区 -->
        <el-menu
        background-color="#4FC08D"
        text-color="#555"
        active-text-color="#FF0"
        unique-opened
        :collapse="isCollapse"
        :collapse-transition="false"
        router
        :default-active="this.$route.path">
        <!-- 一级菜单首页 -->
        <el-menu-item index="/test">
          <i class="el-icon-data-analysis"></i>
          <span>测试</span>
        </el-menu-item>
        <!-- 一级菜单 -->
        <el-submenu
        :index="item.id + ''"
        v-for="item in menus"
        :key="item.id">
          <!-- 一级菜单的模板区 -->
          <template slot="title">
            <!-- 图标 -->
            <i :class="item.icon"></i>
            <!-- 文本 -->
            <span>{{item.name}}</span>
          </template>
          <!-- 二级菜单 -->
          <el-menu-item
          :index="subItem.path"
          v-for="subItem in item.children"
          :key="subItem.id">
            <template slot="title">
              <!-- 图标 -->
              <i :class="subItem.icon"></i>
              <!-- 文本 -->
              <span>{{subItem.name}}</span>
            </template>
          </el-menu-item>
        </el-submenu>
      </el-menu>
      </el-aside>
      <!-- 内容区 -->
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
  export default {
    name: 'home',
    data() {
      return {
        //是否折叠
        isCollapse: false,
        //导航菜单栏
        menus:[{
          id: 100,
          icon: 'el-icon-document',
          name: '题目管理',
          children: [{
            id: 110,
            path: '/problem',
            icon: 'el-icon-tickets',
            name: '题目列表',
          },
          {
            id: 120,
            path: '/addProblem',
            icon: 'el-icon-document-add',
            name: '添加题目',
          }]
        },
        {
          id: 200,
          icon: 'el-icon-edit',
          name: '作答管理',
          children: [{
            id: 210,
            path: '/reply',
            icon: 'el-icon-edit-outline',
            name: '作答列表',
          }]
        }]
      }
    },
    methods: {
     //汉堡按钮开关
      handleToggle() {
        this.isCollapse = !this.isCollapse
      }
    }
  }
</script>

<style lang="less" scoped="scoped">
  .home_container {
    // 页面撑满全屏
    height: 100%;
  }


  .el-header {
    // 设置头部主题颜色
    background-color: #41A863;
    // 使头部内的元素两边对齐，内容居中
    display: flex;
    justify-content: space-between;
    align-items: center;

    > div {
      // 使图片和文本居中
      display: flex;
      align-items: center;

      img {
        // 控制图片大小为50px
        height: 50px;
      }

      span {
        // 文本和图片之间的间距20px
        margin-left: 20px;
        // 文本颜色为白色,大小为25px
        color: #FFF;
        font-size: 25px;
      }
    }
  }


  .el-aside {
    // 设置侧边栏颜色
    background-color: #4FC08D;

   .toggle_button {
      // 设置侧边栏开关背景颜色
      background-color: #4FC08D;
      font-size: 10px;
      line-height: 24px;
      color: #fff;
      text-align: center;
      //文本按钮‘|’之间的间距
      letter-spacing: 0.2em;
      //移动到此处鼠标变小手样式
      cursor: pointer;
    }

    .el-menu {
      border-right: none;
    }
  }


  .el-main {
    // 设置主体内容颜色
    background-color: #FFFAE8;
  }

</style>
