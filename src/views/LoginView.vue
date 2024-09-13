<template>
    <div class="login-container">
      <div class="login-form">
        <h2>管理员登录</h2>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="adminName">用户名：</label>
            <el-input type="text" id="adminName" v-model="adminName" placeholder="请输入用户名" required></el-input>
          </div>
          <div class="form-group">
            <label for="adminPassword">密码：</label>
            <el-input type="password" id="adminPassword" show-password v-model="adminPassword" placeholder="请输入密码" required></el-input>
          </div>
          <div class="form-group">
            <button type="submit">登录</button>
          </div>
        </form>
        <div v-if="error">{{ error }}</div>
      <div v-if="success">{{ success }}</div>
      </div>  
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
          adminName: '',
          adminPassword: '',
          error: null,
        success: null,
      };
    },
    methods: {
      handleLogin() {
        axios.post('http://192.168.148.26:5000/administrator/login', {
          adminName: this.adminName,
          adminPassword: this.adminPassword,
        })
        .then(response => {
          this.success = response.data.message;
          this.error = null;
          if(response.data.code == 0){
            localStorage.setItem('admin',JSON.stringify(response.data));
            this.$message({
                message: '登陆成功',
                type: 'success'
        });
            this.$router.push('/');
          }
        })
        .catch(error => {
          this.error = error.response.data.message;
          this.success = null;
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  
  .login-form {
    width: 300px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input[type="text"],
  input[type="password"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  