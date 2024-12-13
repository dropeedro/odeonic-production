import { createRouter, createWebHistory } from "vue-router";
import DefaultLayout from '../components/DefaultLayout.vue';
import AdminLayout from '../components/AdminLayout.vue';
import UserLayout from '../components/UserLayout.vue';
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Success from "../views/Success.vue";
import DashboardContent from "../views/Admin/DashboardContent.vue";
import PlanManagement from "../views/Admin/PlanManagement.vue";
import UserManagement from "../views/Admin/UserManagement.vue";
import UserHome from "../views/users/UserHome.vue"
import { keycloak } from '../keycloak';

const routes = [
    {
        path: '/',
        component: DefaultLayout,
        children: [
            { path: '', name: 'Home', component: Home },
            { path: 'login', name: 'Login', component: Login },
            { path: 'register', name: 'Register', component: Register },
            { path: 'success', name: 'Success', component: Success }
        ]
    },
    {
        path: '/admin',
        component: AdminLayout,
        children: [
            { path: '', name: 'AdminDashboard', component: DashboardContent, meta: { requiresAuth: true }},
            { path: 'plans', name: 'PlanManagement', component: PlanManagement, meta: { requiresAuth: true }},
            { path: 'users', name: 'UserManagement', component: UserManagement, meta: { requiresAuth: true }}
        ]
    },
    {
        path: '/user',
        component: UserLayout,
        children: [
            { path: '', name: 'UserHome', component: UserHome, meta: { requiresAuth: false }}, //cambiar a true
        ]
    }
    
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (keycloak.authenticated) {
            next();
        } else {
            keycloak.login();
        }
    } else {
        next();
    }
});

export default router;
