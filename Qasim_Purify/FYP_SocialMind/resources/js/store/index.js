// index.js
import { createStore } from 'vuex';
import axios from 'axios';

// Configure axios defaults
axios.defaults.baseURL = 'http://127.0.0.1:8000';
axios.defaults.withCredentials = true; // Important for CSRF token
axios.defaults.headers.common['Accept'] = 'application/json';

// Add request and response interceptors
axios.interceptors.request.use(request => {
  console.log('Request:', request);
  return request;
});

axios.interceptors.response.use(
  response => {
    console.log('Response:', response);
    return response;
  },
  error => {
    console.log('Error Response:', error.response);
    return Promise.reject(error);
  }
);

export default createStore({
  state() {
    return {
      isLoggedIn: !!localStorage.getItem('token'),
    };
  },
  mutations: {
    setLoggedIn(state, value) {
      state.isLoggedIn = value;
    },
  },
  actions: {
    login({ commit }, token) {
      localStorage.setItem('token', token);
      commit('setLoggedIn', true);
    },
    logout({ commit }) {
      localStorage.removeItem('token');
      commit('setLoggedIn', false);
    },
  },
});
