<template>
    <div>
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
          <el-form-item label="通知标题" prop="title">
      <el-input type="textarea" v-model="ruleForm.title"></el-input>
    </el-form-item>
    <el-form-item label="通知类型" prop="type">
      <el-radio-group v-model="ruleForm.type">
      <el-radio label="新版本更新"></el-radio>
      <el-radio label="账户安全提醒"></el-radio>
      <el-radio label="翻译任务提醒"></el-radio>
    </el-radio-group>
    </el-form-item>
    <el-form-item label="通知内容" prop="desc">
      <el-input type="textarea" v-model="ruleForm.desc"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即发送</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
    </div>
</template>

  <script>
  import axios from 'axios';
    export default {
      data() {
        return {
          ruleForm: {
            title:'',
            type: '',
            desc: ''
          },
          rules: {
            title: [
              { required: true, message: '请填写通知标题', trigger: 'blur' }
            ],
            type: [
              { required: true, message: '请至少选择一个通知类型', trigger: 'change' }
            ],
            desc: [
              { required: true, message: '请填写通知内容', trigger: 'blur' }
            ]
          }
        };
      },
      methods: {
        submitForm(formName) {
          this.$refs[formName].validate((valid) => {
    if (valid) {
      // http://172.20.10.4:5000/administrator/login
      // http://172.20.10.4:5000/systemnotification/admin_send_notification

      
    
      axios.post('http://127.0.0.1:5000/ss/a', {
        announce_title: this.ruleForm.title,
        announce_type: this.ruleForm.type,
        announce_content: this.ruleForm.desc
      }).then(res => {
        this.$message({
            message: '提交成功',
            type: 'success'
          });
        console.log('连接到主机');
          this.resetForm(formName);
      })
      .catch(error => {
        console.error('请求失败:', error);
        this.$message.error('请求失败，请检查网络连接或联系管理员');
      });
    } else {
      this.$message.error('请填写完必填项目');
      return false;
    }
  });
        },
        resetForm(formName) {
          this.$refs[formName].resetFields();
        }
      }
    }
  </script>