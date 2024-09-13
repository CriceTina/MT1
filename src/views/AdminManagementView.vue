<template>
  <div>
    <div>
      <el-input clearable="true" v-model="input" style="width: 200px;" placeholder="请输入用户名搜索"></el-input>
      <el-button type="primary" @click="findBySearch()">搜索</el-button>
      <el-button type="warning" @click="reset()">清空</el-button>
      <el-button type="primary" @click="add()">新增</el-button>
    </div>
    <div>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="id" label="管理员ID"></el-table-column>
        <el-table-column prop="username" label="管理员名称"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button type="primary" @click="edit(scope.row)" plain>编辑</el-button>
          </template>

          <el-popconfirm confirm-button-text='确定' cancel-button-text='取消' icon="el-icon-info" icon-color="red"
            title="确定删除吗？">
            <el-button slot="reference" type="danger" plain>删除</el-button>
          </el-popconfirm>
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
      <el-dialog title="新增管理员" :visible.sync="dialogFormVisible" width="30%">
        <el-form :model="form">
          <el-form-item label="管理员名称" label-width="20%">
            <el-input v-model="form.name" autocomplete="off" style="width: 90%;"></el-input>
          </el-form-item>
          <el-form-item label="管理员密码" label-width="20%">
            <el-input v-model="form.password" autocomplete="off" style="width: 90%;"></el-input>
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
        form: {}
      }
    },
    created() {
      //this.load();
    },
    methods: {
      load() {
        request.post('/administrator/view_users').then(res => {
          let data = JSON.stringify(res);
          this.tableData = JSON.parse(data);
        })
      },
      findBySearch() {
        request.post('/administrator/', {
          userName: this.input
        }).then(res => {
          let data = JSON.stringify(res);
          this.tableData = JSON.parse(data);
        })
      },
      reset() {
        this.input = '';
        this.load();
      },
      handleSizeChange() {

      },
      handleCurrentChange() {

      },
      add() {
        this.dialogFormVisible = true;
      },
      submit() {
        request.post('/', this.form).then(res => {
          this.$message({
            message: '添加成功',
            type: 'success'
          });
        })
        this.dialogFormVisible = false;
      },
      edit(obj) {
        this.form = obj;

      }
    }
  }
</script>