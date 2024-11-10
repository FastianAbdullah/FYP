import { createStore } from 'vuex';
import axios from 'axios';

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
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        axios.post('/logout')
          .then(() => {
            localStorage.removeItem('token');
            commit('setLoggedIn', false);
            resolve();
          })
          .catch(reject);
      });
    },
  },
});