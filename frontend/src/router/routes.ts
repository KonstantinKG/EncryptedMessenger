import { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    // component: () => import('layouts/default.vue'),
    redirect: '/login',
    // children: [{ path: '', component: () => import('pages/chat.vue') }]
  },

  {
    path: '/login',
    component: () => import('pages/login.vue')
  },

  {
    path: '/register',
    component: () => import('pages/register.vue')
  },


  {
    path: '/chats',
    // component: () => import('pages/chats.vue')
    component: () => import('layouts/default.vue')
    // children: [{ path: '', component: () => import('pages/IndexPage.vue') }]
  },

  {
    path: '/chat/:id',
    component: () => import('pages/chat.vue')
    // children: [{ path: '', component: () => import('pages/IndexPage.vue') }]
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/error-page.vue')
  }
]

export default routes
