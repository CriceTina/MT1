<template>
    <div>
      <form @submit.prevent="login">
        <input type="text" v-model="username" placeholder="AdminName">
        <input type="password" v-model="password" placeholder="AdminPassword">
        <button type="submit">Login</button>
      </form>
      <div v-if="error">{{ error }}</div>
      <div v-if="success">{{ success }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        error: null,
        success: null,
      };
    },
    methods: {
      login() {
        axios.post('http://172.20.10.4:5000/administrator/login', {
          adminName: this.username,
          adminPassword: this.password,
        })
        .then(response => {
          this.success = response.data.message;
          this.error = null;
          console.log("用户名"+this.username);
          console.log("密码"+this.password)
        })
        .catch(error => {
          this.error = error.response.data.message;
          this.success = null;

        });
      },
    },
  };
  </script>
  