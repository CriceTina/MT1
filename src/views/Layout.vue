<template>
    <div>
      <el-container>
        <!-- 侧边栏-->
        <el-aside :width="asideWidth" style=" min-height: 100vh; background-color: #001529">
          <div style="height: 60px; line-height: 60px;color: white; display: flex; align-items: center; justify-content: center">
            <img src="@/assets/logo1.webp" alt="" style="width: 40px;height: 40px;">
            <transition name="el-fade-in-linear">
              <span style="margin-left: 5px; font-size: 18px;" v-show="!isCollapse">MT1后台管理系统</span>
            </transition>
            
            
          </div>
  
          <el-menu :dufault-active="$route.path" router :collapse="isCollapse" collapse-transition="false" style="border: none; " background-color="#001529" text-color="rgba(255,255,255,0.65)" active-text-color="#fff" :default-active="$route.path">
            <el-submenu index="1">
              <template slot="title">
                <i class ="el-icon-menu"></i>
                <span>用户管理</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/UserManagement">用户管理</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-submenu index="2">
              <template slot="title">
                <i class ="el-icon-s-home"></i>
                <span>用户反馈</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/FeedbackView">用户反馈</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-submenu index="3">
              <template slot="title">
                <i class ="el-icon-s-home"></i>
                <span>数据可视化</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/backenddataView">后台数据管理</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-menu-item index="/PublishNoticeView">
              <i class ="el-icon-s-opportunity"></i>
              <span slot="title">发布通知</span>
            </el-menu-item>
          
  
          </el-menu>
  
        </el-aside>
  
        <el-container>
          <!--      头部--->
          <el-header>
            <el-row>
              <el-col :span="4"> <div><i :class="CollapseIcon" style="font-size: 26px;margin-top: 20px;" @click="handleCollapse"></i></div></el-col>
              <el-col :span="20">
                <div style="display: flex; flex: 1;align-content: center;justify-content: flex-end; padding:10px 0 0 0;">
              <!-- 下拉菜单区域-->
              <el-dropdown >
                <img src="@/assets/logo1.webp" alt="" style="width: 40px; height: 40;">
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item>个人信息</el-dropdown-item>
                  <el-dropdown-item>修改密码</el-dropdown-item>
                  <el-dropdown-item><div @click="logout">退出登录</div></el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown> 
            <span style="padding: 1000 0 0 0;">{{ admin.data.adminName }}</span> 
                </div>
  
              </el-col>
            </el-row>
           
            
              
          </el-header>
  
          <!-- 主体-->
          <el-main>
            <router-view/>
          </el-main>
        </el-container>
      </el-container>
  
    </div>
  </template>
  <script>
  export default {
    name: 'HomeView',
    data(){
      return{
        asideWidth: '200px',
        isCollapse: false,// 收缩
        CollapseIcon:'el-icon-s-fold',
        admin: localStorage.getItem('admin') ? JSON.parse(localStorage.getItem('admin')) : {}
      }
    },
    methods: {
      handleCollapse(){
        this.isCollapse = !this.isCollapse;
        this.asideWidth = this.isCollapse ? '64px':'200px';
        this.CollapseIcon = this.isCollapse ? 'el-icon-s-unfold':'el-icon-s-fold';
      },
      logout(){
        localStorage.removeItem('admin');
        this.$router.push('/LoginView');
      }
    }
  }
  </script>
  <style>
  .el-menu--inline{
    background-color: #000c17 !important;
  }
  .el-menu--inline .el-menu-item{
    background-color: #000c17 !important;
    padding-left: 49px !important;
  }
  .el-menu-item:hover,  .el-submenu__title:hover  {
    color: #fff !important;
  }
  .el-submenu__title:hover i{
    color: #fff !important;
  }
  .el-menu-item.is-active{
    background-color: #1890ff !important;
    border-radius: 10px;
    margin: 4px;
  }
  .el-menu-item{
    height: 40px;
    line-height: 40px;
  }
  .el-submenu__title{
    height: 40px;
    line-height: 40px;
  }
  .el-aside{
    transition: width .3s;
    box-shadow: 2px 0 6px rgba(0,21,41,.35);
  }
  .el-header{
    box-shadow: 2px 0 6px rgba(0,21,41,.35);
  }
  </style>