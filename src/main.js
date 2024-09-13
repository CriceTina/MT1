import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.config.productionTip = false
Vue.use(ElementUI);
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

router.beforeEach((to, _from, next) => {
  // 验证是否需要登录
  if (to.matched.some(res => res.meta.requireAuth)) {
    var userId = window.sessionStorage.getItem('userId');
    console.log(userId);
    if (userId) { // 查询本地存储信息是否已经登录
      next(); // 如果已经登录，则继续
    } else {
      // 如果未登录，则重定向到登录页面，并将当前路由的完整路径作为查询参数传递
      next({
        path: '/login',
        query: { redirect: to.fullPath } // 登录成功后回到当前页面
      });
    }
  } else {
    next(); // 如果不需要登录，则直接放行
  }
});

