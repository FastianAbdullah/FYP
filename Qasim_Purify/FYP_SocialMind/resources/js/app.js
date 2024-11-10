import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store/index.js';
import axios from 'axios';

axios.defaults.withCredentials = true;
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

const app = createApp(App);
app.use(router);
app.use(store);
app.mount('#app');
