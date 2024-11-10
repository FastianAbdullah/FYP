import { createRouter, createWebHistory } from 'vue-router';
import Index from './components/Index.vue';
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import Pricing from './components/Pricing.vue';
import Privacy from './components/Privacy.vue';
import Terms from './components/Terms.vue';
// Import other components

const routes = [
  { path: '/', component: Index },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/pricing', component: Pricing },
  { path: '/privacy', component: Privacy },
  { path: '/terms', component: Terms }
  // Define other routes
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
