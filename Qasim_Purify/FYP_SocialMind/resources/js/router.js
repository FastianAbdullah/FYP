import { createRouter, createWebHistory } from 'vue-router';
import Index from './components/Index.vue';
// import Login from './components/Login.vue';
// Import other components

const routes = [
  { path: '/', component: Index },
//   { path: '/login', component: Login },
  // Define other routes
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
