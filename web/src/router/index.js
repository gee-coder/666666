import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
		redirect: '/test',
    component: () => import('components/Home.vue')
  },
  {
    path: '/home',
    redirect: '/test',
    component: () => import('components/Home.vue'),
    children: [
    	{
    		path: '/test',
    		component: () => import('components/test/Test.vue')
    	},
      {
      	path: '/problem',
      	component: () => import('components/problem/Problem.vue')
      },
      {
      	path: '/addProblem',
      	component: () => import('components/problem/AddProblem.vue')
      },
      {
        path: '/reply',
        component: () => import('components/reply/Reply.vue')
      },
      {
        path: '/addReply',
        component: () => import('components/reply/AddReply.vue')
      }
    ]
  },


]

const router = new VueRouter({
  mode: 'history',
  routes
})



export default router
