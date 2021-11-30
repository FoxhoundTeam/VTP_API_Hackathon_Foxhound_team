import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

let opts = {
  routes: [
    {
      path: "/",
      name: "Index",
      redirect: "/dashboard",
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/dashboard",
      name: "Dashboard",
      component: () => import('../views/Dashboard.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/websocket",
      name: "WebSocketSchema",
      component: () => import('../views/WebSocketSchemaTable.vue'),
      meta: {
        requiresAuth: true
      },
      children: [
        {
          path: "create",
          name: "WebSocketSchemaCreate",
          component: () => import('../components/modals/WebSocketSchemaModal.vue'),
          meta: {
            requiresAuth: true
          },
        },
        {
          path: "edit/:id",
          name: "WebSocketSchemaEdit",
          component: () => import('../components/modals/WebSocketSchemaModal.vue'),
          meta: {
            requiresAuth: true
          },
        },
      ]
    },
    {
      path: "/websocket_callback",
      name: "WebSocketCallback",
      component: () => import('../views/WebSocketCallbackTable.vue'),
      meta: {
        requiresAuth: true
      },
      children: [
        {
          path: "create",
          name: "WebSocketCallbackCreate",
          component: () => import('../components/modals/WebSocketCallbackModal.vue'),
          meta: {
            requiresAuth: true
          },
        },
        {
          path: "edit/:id",
          name: "WebSocketCallbackEdit",
          component: () => import('../components/modals/WebSocketCallbackModal.vue'),
          meta: {
            requiresAuth: true
          },
        },
      ]
    },
    {
      path: "/violations",
      name: "Violation",
      component: () => import('../views/ViolationsTable.vue'),
      meta: {
        requiresAuth: true
      },
      children: [
        {
          path: ":id/",
          name: "ViolationView",
          component: () => import('../components/modals/ViolationModal.vue'),
          meta: {
            requiresAuth: true
          },
        },
      ]
    },
    {
      path: "/settings",
      name: "Settings",
      component: () => import('../views/Settings.vue'),
      meta: {
        requiresAuth: true
      },
    },
    {
      path: "/login",
      name: "login",
      component: () => import('../views/Login.vue'),
      meta: {
        requiresAuth: false
      }
    },
  ],
  linkExactActiveClass: 'active'
};
const router = new VueRouter(opts);

export default router
