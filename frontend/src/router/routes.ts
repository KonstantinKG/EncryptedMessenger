import { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/chat/1'
    // children: [{ path: '', component: () => import('pages/IndexPage.vue') }]
  },

  {
    path: '/chats',
    component: () => import('pages/chats.vue'),
    // children: [{ path: '', component: () => import('pages/IndexPage.vue') }]
  },

  {
    path: '/chat/:id',
    component: () => import('pages/chat.vue'),
    // children: [{ path: '', component: () => import('pages/IndexPage.vue') }]
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
    path: '/:catchAll(.*)*',
    component: () => import('pages/error-page.vue')
  }
]

export default routes
