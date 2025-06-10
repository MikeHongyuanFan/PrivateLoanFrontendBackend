import { createRouter, createWebHashHistory } from 'vue-router'
import Layout from '@/layout.vue'
//导入各模块图标
import dashboard from '@/assets/icons/nav_dashboard.png'
import application from '@/assets/icons/nav_application.png'
import borrower from '@/assets/icons/nav_borrower.png'
import guarantor from '@/assets/icons/nav_guarantor.png'
import broker from '@/assets/icons/nav_broker.png'
import bdm from '@/assets/icons/nav_bdm.png'
import branch from '@/assets/icons/nav_branch.png'
import product from '@/assets/icons/nav_product.png'
import document from '@/assets/icons/nav_document.png'
import setting from '@/assets/icons/nav_setting.png'
import notification from '@/assets/icons/nav_notification.png'
// Create a proper nav_inbox.png icon using the mail emoji
import inbox from '@/assets/icons/nav_inbox.png'

export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/view/login.vue'),
    meta: {
      hidden: true,
      title: 'Login',
      isTop: true,
    },
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard/index',
    meta: {
      hidden: false,
      title: 'Dashboard',
      icon: dashboard,
      i18nTitle: 'system.dashboard',
      isTop: true,
    },
    children: [
      {
        path: '/dashboard/index',
        component: () => import('@/view/dashboard/overview.vue'),
        meta: {
          title: 'Overview',
          keepAlive: true,
          breadcrumb: [
            { label: 'Dashboard', path: '/dashboard/index' },
            { label: 'Overview' },
          ],
        },
      },
      {
        path: '/dashboard/repayment',
        component: () => import('@/view/dashboard/repayment.vue'),
        meta: {
          title: 'Overview',
          keepAlive: false,
          breadcrumb: [
            { label: 'Dashboard', path: '/dashboard/index' },
            { label: 'Repayment' },
          ],
        },
      },
    ],
  },
  //application
  {
    path: '/application',
    component: Layout,
    redirect: '/application/index',
    meta: {
      hidden: false,
      title: 'Application',
      icon: application,
      i18nTitle: 'system.application',
      isTop: true,
    },
    children: [
      {
        path: '/application/index',
        component: () => import('@/view/application/applicationlist.vue'),
        meta: {
          title: 'Application',
          keepAlive: true,
          breadcrumb: [
            { label: 'Application', path: '/application' },
            { label: 'Application List' },
          ],
        },
      },
      {
        path: '/application/:applicationId',
        component: () => import('@/view/application/application.vue'),
        meta: {
          title: 'Application',
          breadcrumb: [
            { label: 'Application', path: '/application' },
            { label: 'Application Detail' },
          ],
        },
      },
    ],
  },
  //borrower
  {
    path: '/borrower',
    component: Layout,
    redirect: '/borrower/index',
    meta: {
      hidden: false,
      title: 'Borrower',
      icon: borrower,
      i18nTitle: 'system.borrower',
      isTop: true,
    },
    children: [
      {
        path: '/borrower/index',
        component: () => import('@/view/borrower/borrowerlist.vue'),
        meta: {
          title: 'Borrower',
          keepAlive: true,
          breadcrumb: [
            { label: 'Borrower', path: '/borrower' },
            { label: 'Borrower List' },
          ],
        },
      },
      {
        path: '/borrower/:borrowerId',
        component: () => import('@/view/borrower/borrower.vue'),
        meta: {
          title: 'Borrower',
          breadcrumb: [
            { label: 'Borrower', path: '/borrower' },
            { label: 'Borrower Detail' },
          ],
        },
      },
    ],
  },
  //guarantor
  {
    path: '/guarantor',
    component: Layout,
    redirect: '/guarantor/index',
    meta: {
      hidden: false,
      title: 'Guarantor',
      icon: guarantor,
      i18nTitle: 'system.guarantor',
      isTop: true,
    },
    children: [
      {
        path: '/guarantor/index',
        component: () => import('@/view/guarantor/guarantorlist.vue'),
        meta: {
          title: 'Guarantor',
          keepAlive: true,
          breadcrumb: [
            { label: 'Guarantor', path: '/guarantor' },
            { label: 'Guarantor List' },
          ],
        },
      },
      {
        path: '/guarantor/:guarantorId',
        component: () => import('@/view/guarantor/guarantor.vue'),
        meta: {
          title: 'Guarantor',
          breadcrumb: [
            { label: 'Guarantor', path: '/guarantor' },
            { label: 'Guarantor Detail' },
          ],
        },
      },
    ],
  },
  //broker
  {
    path: '/broker',
    component: Layout,
    redirect: '/broker/index',
    meta: {
      hidden: false,
      title: 'Broker',
      icon: broker,
      i18nTitle: 'system.broker',
      isTop: true,
    },
    children: [
      {
        path: '/broker/index',
        component: () => import('@/view/broker/brokerlist.vue'),
        meta: {
          title: 'Broker',
          keepAlive: true,
          breadcrumb: [
            { label: 'Broker', path: '/broker' },
            { label: 'Broker List' },
          ],
        },
      },
      {
        path: '/broker/:brokerId',
        component: () => import('@/view/broker/broker.vue'),
        meta: {
          title: 'Broker',
          breadcrumb: [
            { label: 'Broker', path: '/broker' },
            { label: 'Broker Detail' },
          ],
        },
      },
    ],
  },
  //bdm
  {
    path: '/bdm',
    component: Layout,
    redirect: '/bdm/index',
    meta: {
      hidden: false,
      title: 'BDM',
      icon: bdm,
      i18nTitle: 'system.bd',
      isTop: true,
    },
    children: [
      {
        path: '/bdm/index',
        component: () => import('@/view/bdm/bdmlist.vue'),
        meta: {
          title: 'BDM',
          keepAlive: true,
          breadcrumb: [{ label: 'BDM', path: '/bdm' }, { label: 'BDM List' }],
        },
      },
      {
        path: '/bdm/:bdmId',
        component: () => import('@/view/bdm/bdm.vue'),
        meta: {
          title: 'BDM',
          breadcrumb: [{ label: 'BDM', path: '/bdm' }, { label: 'BDM Detail' }],
        },
      },
    ],
  },
  //branch
  {
    path: '/branch',
    component: Layout,
    redirect: '/branch/index',
    meta: {
      hidden: false,
      title: 'Branch',
      icon: branch,
      i18nTitle: 'system.branch',
      isTop: true,
    },
    children: [
      {
        path: '/branch/index',
        component: () => import('@/view/branch/branchlist.vue'),
        meta: {
          title: 'Branch',
          keepAlive: true,
          breadcrumb: [
            { label: 'Branch', path: '/branch' },
            { label: 'Branch List' },
          ],
        },
      },
      {
        path: '/branch/:branchId',
        component: () => import('@/view/branch/branch.vue'),
        meta: {
          title: 'Branch',
          breadcrumb: [
            { label: 'Branch', path: '/branch' },
            { label: 'Branch Detail' },
          ],
        },
      },
    ],
  },
  //product
  {
    path: '/product',
    component: Layout,
    redirect: '/product/index',
    meta: {
      hidden: false,
      title: 'Product',
      icon: product,
      i18nTitle: 'system.product',
      isTop: true,
    },
    children: [
      {
        path: '/product/index',
        component: () => import('@/view/product.vue'),
        meta: {
          title: 'Product',
          keepAlive: true,
          breadcrumb: [
            { label: 'Product', path: '/product' },
            { label: 'Product List' },
          ],
        },
      },
    ],
  },
  //document
  {
    path: '/document',
    component: Layout,
    redirect: '/document/index',
    meta: {
      hidden: false,
      title: 'Document',
      icon: document,
      i18nTitle: 'system.documents',
      isTop: true,
    },
    children: [
      {
        path: '/document/index',
        component: () => import('@/view/document.vue'),
        meta: {
          title: 'Document',
          breadcrumb: [{ label: 'Document', path: '/document' }],
        },
      },
    ],
  },
  //user
  {
    path: '/user',
    component: Layout,
    redirect: '/user/index',
    meta: {
      hidden: false,
      title: 'User',
      icon: branch,
      i18nTitle: 'system.user',
      isTop: true,
    },
    children: [
      {
        path: '/user/index',
        component: () => import('@/view/user/userlist.vue'),
        meta: {
          title: 'User List',
          keepAlive: true,
          breadcrumb: [
            { label: 'User', path: '/user' },
            { label: 'User List' },
          ],
        },
      },
      {
        path: '/user/:userId',
        component: () => import('@/view/user/user.vue'),
        meta: {
          title: 'User Detail',
          breadcrumb: [
            { label: 'User', path: '/user' },
            { label: 'User Detail' },
          ],
        },
      },
    ],
  },
  //setting
  {
    path: '/setting',
    component: Layout,
    redirect: '/setting/index',
    meta: {
      hidden: false,
      title: 'Setting',
      icon: setting,
      i18nTitle: 'system.setting',
      isTop: false,
    },
    children: [
      {
        path: '/setting/index',
        component: () => import('@/view/settings.vue'),
        meta: {
          title: 'Setting',
          breadcrumb: [{ label: 'Setting', path: '/setting' }],
        },
      },
    ],
  },
  //notification
  {
    path: '/notification',
    component: Layout,
    redirect: '/notification/index',
    meta: {
      hidden: false,
      title: 'Notification',
      icon: notification,
      i18nTitle: 'system.notification',
      isTop: false,
    },
    children: [
      {
        path: '/notification/index',
        component: () => import('@/view/notification.vue'),
        meta: {
          title: 'Notification',
          breadcrumb: [{ label: 'Notification', path: '/notification' }],
        },
      },
    ],
  },
  //inbox
  {
    path: '/inbox',
    component: Layout,
    redirect: '/inbox/index',
    meta: {
      hidden: false,
      title: 'Inbox',
      icon: inbox,
      i18nTitle: 'system.inbox',
      isTop: false,
    },
    children: [
      {
        path: '/inbox/index',
        component: () => import('@/view/inbox.vue'),
        meta: {
          title: 'Inbox',
          breadcrumb: [{ label: 'Inbox', path: '/inbox' }],
        },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: constantRoutes,
})

export default router

