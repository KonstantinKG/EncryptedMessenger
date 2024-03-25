import { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login'
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
    component: () => import('layouts/default.vue'),
    children: [
      {
        path: ':id',
        name: 'Chat',
        component: () => import('pages/chat.vue')
      },
      {
        path: ':id/members',
        name: 'Members',
        component: () => import('pages/members.vue')
      }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/error-page.vue')
  }
]

export default routes
