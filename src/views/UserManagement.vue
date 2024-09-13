<template>
  <div>
    <div>
      <el-input clearable="true" v-model="input" style="width: 200px;" placeholder="请输入用户名搜索"></el-input>
      <el-button type="primary" @click="findBySearch()">搜索</el-button>
      <el-button type="primary" @click="reset()">清空</el-button>
    </div>
    <div>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="id" label="用户ID"></el-table-column>
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="registration_time" label="注册时间"></el-table-column>
        <el-table-column prop="primary_language_id" label="主语言ID"></el-table-column>
        <el-table-column prop="last_login_time" label="最近登录时间"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" @click="edit(scope.row)" plain>编辑</el-button>
            <el-popconfirm @confirm="del(scope.row.id)" confirm-button-text='确定' cancel-button-text='取消'
              icon="el-icon-info" icon-color="red" title="确定删除吗？">
              <el-button slot="reference" type="danger" plain>删除</el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div style="margin-top: 10px;">
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="pageNum"
        :page-sizes="[5, 10, 15, 20]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>
    </div>
    <div>
      <el-dialog title="请填写信息" :visible.sync="dialogFormVisible" width="30%">
        <el-form :model="form">
          <el-form-item label="用户名称" :label-width="auto">
            <el-input v-model="form.username" autocomplete="off" style="width: 90%;"></el-input>
          </el-form-item>
          <el-form-item label="主语言" :label-width="auto">
            <el-input v-model="form.primary_language_id" autocomplete="off" style="width: 90%;"></el-input>
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
        pageSize: 5,
        pageNum: 1,
        total: 100,
        tableData: [],
        dialogFormVisible: false,
        form: []
      }
    },
    created() {
      this.findBySearch();
    },
    methods: {
      findBySearch() {
        request.post('/administrator/findBySearch', {
          userName: this.input,
          pageSize: this.pageSize,
          pageNum: this.pageNum
        }).then(res => {
          console.log(res)
          console.log(res.data.total)
          console.log(res.data.users)

          let data = JSON.stringify(res.data.users);
          this.tableData = JSON.parse(data);
          //分页信息
          this.total = res.data.total;
        })
      },
      submit() {
        console.log(this.form);
        request.post('/administrator/edit', {
          form: this.form
        }).then(res => {
          this.$message({
            message: '编辑成功',
            type: 'success'
          });
          this.dialogFormVisible = false;
          this.findBySearch();
        })
      },
      reset() {
        this.input = '';
        this.findBySearch();
      },
      edit(obj) {
        this.form = obj;
        this.dialogFormVisible = true;
      },
      del(id) {
        request.post('/administrator/delete', {
          delete_id: id
        }).then(res => {
          console.log(res)
          this.$message({
            message: '删除成功',
            type: 'success'
          });
          this.findBySearch();
        })
      },
      handleSizeChange(pageSize) {
        this.pageSize = pageSize;
        this.findBySearch();
      },
      handleCurrentChange(pageNum) {
        this.pageNum = pageNum;
        this.findBySearch();
      }

    }
  }
</script>