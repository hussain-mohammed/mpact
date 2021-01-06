import Vue from 'vue'
import Router from 'vue-router';

Vue.use(Router)

export default new Router({
  mode: "history",
  routes: [
    {
      path: '',
      redirect: "/login",
    },
    {
      path: '/login',
      name: 'Auth',
      component: () => import('../views/authentication.vue')
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../views/chat.vue')
    }
  ]
})