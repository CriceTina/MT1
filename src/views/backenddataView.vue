<template>
  <div>
    <div style="display: flex;">
      <!--用户数量-->
      <div style="flex: 1;">
        <el-row :gutter="20">
          <el-col :span="8">
            <div>
              <el-statistic group-separator="," :precision="2" :value="onlineuser_qty" :title="title1"></el-statistic>
            </div>
          </el-col>
          <el-col :span="8">
            <div>
              <el-statistic group-separator="," :precision="2" decimal-separator="." :value="user_qty" :title="title2">
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="4">
            <div>
              <el-statistic ref="statistic" @finish="hilarity" format="HH:mm:ss" :value="deadline4" title="距离明日："
                time-indices></el-statistic>
            </div>
          </el-col>
        </el-row>
        <div style="width: 100%;margin-top: 60px;">
          <div id="Line" style="width: 100%;height: 400px;"></div>
        </div>
      </div>
      <!-- 这个是翻译数量数据以及图-->
      <div style="flex: 1;">
        <el-row :gutter="20">
          <el-col :span="6">
            <div>
              <el-statistic group-separator="," :precision="0" decimal-separator="." :value="char_qty" :title="title3">
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic group-separator="," :precision="0" decimal-separator="." :value="file_qty" :title="title4">
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic group-separator="," :precision="0" decimal-separator="." :value="pic_qty" :title="title5">
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic group-separator="," :precision="0" decimal-separator="." :value="speech_qty" :title="title6">
              </el-statistic>
            </div>
          </el-col>
        </el-row>
        <div style="width: 100%;margin-top: 60px;margin-left: 60px;">
          <div id="Bie" style="width: 100%;height: 400px;"></div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
  import request from '@/utils/request';
import * as echarts from 'echarts';
  export default {
    data() {
      return {
        like: true,
        user_qty: 124,
        onlineuser_qty: 33,
        char_qty: null,
        file_qty: null,
        pic_qty: null,
        speech_qty: null,
        title1: "今日在线人数峰值",
        title2: "用户总人数",
        title3: "翻译文字数量",
        title4: "翻译文件数量",
        title5: "翻译图片数量",
        title6: "翻译语音数量",
        deadline4: Date.now() + (new Date().setHours(23, 59, 59) - Date.now()),
      }
    },
    created() {
      this.load();
    },
    mounted() {
      this.initEcharts();
      this.load();
    },
    methods: {
      hilarity() {
        this.$notify({
          title: "提示",
          message: "时间已到",
          duration: 0,
        });
      },
      initEcharts(){
        request.post('/BackendData/Bie').then(res=>{
          this.initBie(res.data.backend_data);
        })
        request.post('/BackendData/Line').then(res=>{
          this.initLine(res.data.BackendDatas)
        })
      },
      load() {
        request.post('/BackendData/getData').then(res=>{
          if(res.status == 200){
            console.log(res.data.backend_data)
            this.char_qty = parseFloat(res.data.backend_data[0].char_qty);
            this.file_qty = parseFloat(res.data.backend_data[0].file_qty);
            this.pic_qty = parseFloat(res.data.backend_data[0].pic_qty);
            this.speech_qty = parseFloat(res.data.backend_data[0].speech_qty);
            this.user_qty = parseFloat(res.data.backend_data[0].user_qty)
            this.onlineuser_qty = parseFloat(res.data.backend_data[0].onlineuser_qty)
          }
        })
      },
      initBie(Data) {
        let chartDom = document.getElementById('Bie');
        let myChart = echarts.init(chartDom);
        let option;

        option = {
          title: {
            text: '翻译情况',
            subtext: '饼状图',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [{
            name: '翻译分类',
            type: 'pie',
            radius: '50%',
            data: Data,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }]
        };

        option && myChart.setOption(option);
      },
      initLine(Data) {
        var chartDom = document.getElementById('Line');
        var myChart = echarts.init(chartDom);
        var option;

        option = {
          tooltip: {
            trigger: 'axis',
            position: function (pt) {
              return [pt[0], '10%'];
            }
          },
          title: {
            left: 'center',
            text: '用户上限数量时间图'
          },
          toolbox: {
            feature: {
              dataZoom: {
                yAxisIndex: 'none'
              },
              restore: {},
              saveAsImage: {}
            }
          },
          xAxis: {
            type: 'time',
            boundaryGap: false
          },
          yAxis: {
            type: 'value',
            boundaryGap: [0, '100%']
          },
          dataZoom: [{
              type: 'inside',
              start: 0,
              end: 20
            },
            {
              start: 0,
              end: 20
            }
          ],
          series: [{
            name: '当日使用的用户总量',
            type: 'line',
            smooth: true,
            symbol: 'none',
            areaStyle: {},
            data: Data
          }]
        };

        option && myChart.setOption(option);
      }

    }
  }
</script>