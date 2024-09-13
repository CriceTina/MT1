<template>
    <div>
      <div>
        <el-input clearable="true" v-model="input" style="width: 200px;" placeholder="请输入反馈标题搜索"></el-input>
        <el-button type="primary" @click="findBySearch()">搜索</el-button>
        <el-button type="primary" @click="reset()">清空</el-button>
      </div>
      <div>
        <el-table
            :data="tableData"
            style="width: 100%"
            :header-cell-style="{'text-align':'center'}">
          <el-table-column prop="feedback_id" label="用户反馈ID" width="100"></el-table-column>
          <el-table-column prop="user_id" label="用户ID" width="100"></el-table-column>
          <el-table-column prop="feedback_title" label="反馈标题" width="100"></el-table-column>
          <el-table-column prop="feedback_type" label="反馈类型" width="100"></el-table-column>
          <el-table-column prop="feedback_time" label="反馈时间" width="100"></el-table-column>
          <el-table-column prop="feedback_status" label="反馈状态" width="100"></el-table-column>
          <el-table-column prop="feedback_content" label="反馈内容" ></el-table-column>
          <el-table-column align="center" label="操作" >
            <template slot-scope="scope">
              <el-button type="primary" @click="edit(scope.row)" plain>编辑</el-button>
              <el-popconfirm @confirm="del(scope.row.feedback_id)" confirm-button-text='确定'cancel-button-text='取消'icon="el-icon-info"icon-color="red"title="确定删除吗？"> 
                <el-button slot="reference" type="danger"plain>删除</el-button>
            </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div style="margin-top: 10px;">
        <el-pagination
        @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="pageNum"
            :page-sizes="[5, 10, 15, 20]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total">
        </el-pagination>
      </div>
      <div>
        <el-dialog title="修改信息" :visible.sync="dialogFormVisible" width="30%">
  <el-form :model="form">
    <el-form-item label="更改反馈状态" :label-width="auto">
      <el-input v-model="form.feedback_status" autocomplete="off" style="width: 90%;"></el-input>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="submit()">确 定</el-button>
  </div>
</el-dialog>
      </div>
    </div>
  </template>
  
  <script>
  import request from '@/utils/request';
  export default {
    data() {
      return {
        input: '',
        tableData: [],
        pageSize: 5,
        pageNum: 1,
        total: 100,
        dialogFormVisible: false,
        form: []
      }
    },
    created(){
      this.findBySearch();
    },
    methods:{
      findBySearch(){
        request.post('/UserFeedback/findBySearch',{
          feedbackTitle: this.input,
          pageSize: this.pageSize,
          pageNum: this.pageNum
        }).then(res=>{
          //console.log(res)
          let data = JSON.stringify(res.data.feedbacks);
          //console.log(data)
          this.tableData = JSON.parse(data);
          //分页信息
          this.total = res.data.total;
        })
      },
      reset(){
        this.input='';
        this.findBySearch();
      },
      handleSizeChange(pageSize){
        this.pageSize = pageSize;
        this.findBySearch();
      },
      handleCurrentChange(pageNum){
        this.pageNum = pageNum;
        this.findBySearch();
      },
      del(id){
        request.post('/UserFeedback/delete',{delete_id:id}).then(res=>{
          this.$message({
                message: '删除成功',
                type: 'success'
        });
        this.findBySearch();
        })
      },
      edit(obj){
        this.form = obj;
        this.dialogFormVisible = true;
      },
      submit(){
        console.log(this.form);
        request.post('/UserFeedback/edit',{
         form: this.form
        }).then(res=>{
          this.$message({
                message: '编辑成功',
                type: 'success'
        });
        this.dialogFormVisible=false;
        this.findBySearch();
        })
      },
    }
  }
  </script>