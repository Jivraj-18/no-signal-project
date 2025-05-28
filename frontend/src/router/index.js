import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import DashboardPage from '../components/DashboardPage.vue';
import UserProfilePage from '../components/UserProfilePage.vue';


const routes = [
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/ask',
    name: 'DashboardPage',
    component: DashboardPage
  },
  {
    path: '/profile',
    name: 'UserProfilePage',
    component: UserProfilePage
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;