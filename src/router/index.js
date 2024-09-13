import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Layout',
    component: () => import(/* webpackChunkName: "about" */ '../views/Layout.vue'),
    redirect:'/UserManagement',
    children: [
      {
        path: '/UserManagement',
        name: 'UserManagement',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/UserManagement.vue')
      },
      {
        path: '/FeedbackView',
        name: 'FeedbackView',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/FeedbackView.vue')
      },
      {
        path: '/backenddataView',
        name: 'backenddataView',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/backenddataView.vue')
      },
      {
        path: '/PublishNoticeView',
        name: 'PublishNoticeView',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/PublishNoticeView.vue')
      },
      {
        path: '/AdminManagementView',
        name: 'AdminManagementView',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/AdminManagementView.vue')
      }
    ]
  },
  {
    path: '/LoginView',
    name: 'LoginView',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/LoginView.vue')
  },
  {
    path: '/test',
    name: 'test',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/test.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to,from,next)=>{
  if(to.path === '/LoginView'){
    next();
  }
  const admin = localStorage.getItem('admin');
  if(!admin && to.path!=='/LoginView'){
    return next('/LoginView');
  }
  next();
})

export default router
