<template>
  <div class="login-page">
    <div class="container">
      <div class="row justify-content-center align-items-center">
        <div class="col-xxl-5 col-xl-6 col-lg-8 col-md-10">
          <div class="gradient-card py-sm-12 py-8 px-sm-8 px-5 rounded-5">
            <p class="fs-24 fw-medium clr-neutral-80 mb-5">Welcome !</p>
            <h4 class="h4 fw-bold mb-2 clr-neutral-90">Sign in to </h4>
            <p class="clr-neutral-80">Get Started with 10,000 Free Words</p>
            <form @submit.prevent="login">
              <div class="d-flex flex-wrap gap-xl-6 gap-4 align-items-center justify-content-center mt-6">
                <!-- Social login buttons (functionality not implemented) -->
                <a href="#" class="link d-inline-flex align-items-center justify-content-center gap-4 py-3 px-8 rounded-2 bg-neutral-6 login-with-btn">
                  <img src="../../../public/img/login-facebook.svg" alt="image" class="img-fluid">
                  <span class="d-inline-block clr-neutral-80 fs-14">Facebook</span>
                </a>
                <a href="#" class="link d-inline-flex align-items-center justify-content-center gap-4 py-3 px-8 rounded-2 bg-neutral-6 login-with-btn">
                  <img src="../../../public/img/login-google.svg" alt="image" class="img-fluid">
                  <span class="d-inline-block clr-neutral-80 fs-14">Google</span>
                </a>
              </div>
              <div v-if="error" class="alert alert-danger mt-4" role="alert">
                {{ error }}
              </div>
              <div class="mt-8">
                <label class="clr-neutral-80 mb-2">User Name</label>
                <input v-model="form.email" type="email" class="form-control border border-neutral-17 clr-neutral-90 :focus-clr-current rounded-2 py-4 px-4 bg-neutral-4 placeholder-50 focus-bg-none" placeholder="Enter your email">
              </div>
              <div class="mt-8">
                <label class="clr-neutral-80 mb-2">Password</label>
                <div class="pass-field-area">
                  <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="form-control border border-neutral-17 clr-neutral-90 :focus-clr-current rounded-2 py-4 px-4 bg-neutral-4 placeholder-50 focus-bg-none" placeholder="Enter your password">
                  <button type="button" class="bg-transparent border-0 pass-eye" @click="togglePassword">
                    <i :class="showPassword ? 'bi bi-eye-fill' : 'bi bi-eye-slash-fill'"></i>
                  </button>
                </div>
              </div>
              <div class="d-flex flex-wrap align-items-center justify-content-between mt-8">
                <div class="form-check check-box check-box check-box-neutral-30 gap-1">
                  <input v-model="form.remember" class="form-check-input check-box__input clr-white my-auto border-0 bg-neutral-17" type="checkbox" id="n30dash">
                  <label class="form-check-label clr-neutral-80 fs-12 ps-1" for="n30dash"> Remember me </label>
                </div>
                <a href="#" class="link clr-neutral-80 fs-12 :clr-primary-key">Forgot Password ?</a>
              </div>
              <button type="submit" class="link d-inline-flex justify-content-center align-items-center gap-2 py-4 px-6 border border-primary-key bg-primary-key rounded-1 fw-bold clr-white border-0 w-100 mt-8 :arrow-btn">
                <span>Login Now</span>
                <i class="bi bi-arrow-right"></i>
              </button>
              <p class="mb-0 clr-neutral-80 text-center mt-8">
                Don't have an Account?
                <router-link to="/register" class="link clr-primary-key fw-semibold">Register</router-link>
              </p>
              <div class="text-center mt-6">
                <router-link to="/" class="link d-inline-flex justify-content-center align-items-center gap-2 py-2 px-4 border border-primary-key bg-primary-key :bg-primary-30 rounded-pill fs-14 fw-bold text-center clr-white">
                  <span class="d-block">Back to Home</span>
                  <span class="d-block fs-10">
                    <i class="bi bi-arrow-up-right"></i>
                  </span>
                </router-link>
              </div>
              
            </form>
          </div>
        </div>
      </div>
      <div class="login-copyright">
        <p class="mb-0 text-center clr-neutral-80">Copyright @2023 <span class="clr-white">Social Mind</span></p>
      </div>
    </div>
    <img src="../../../public/img/login-shape-top.png" alt="image" class="img-fluid login-shape login-shape-top">
    <img src="../../../public/img/login-shape-left.png" alt="image" class="img-fluid login-shape login-shape-left">
    <img src="../../../public/img/login-shape-right.png" alt="image" class="img-fluid login-shape login-shape-right">
    <img src="../../../public/img/login-shape-line-left.png" alt="image" class="img-fluid login-shape login-shape-line-left">
    <img src="../../../public/img/login-shape-line-right.png" alt="image" class="img-fluid login-shape login-shape-line-right">
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        email: '',
        password: '',
        remember: false
      },
      showPassword: false,
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post(`/login`, this.form);
        const token = response.data.token;
        
        // Update Vuex login state and set token
        this.$store.dispatch('login', token);

        // Redirect to home after login
        this.$router.push('/');
      } catch (error) {
        if (error.response && error.response.data.errors) {
          const errorMessages = Object.values(error.response.data.errors).flat();
          this.error = errorMessages.join(' ');
        } else {
          this.error = 'An unexpected error occurred. Please try again.';
        }
        console.error('Login error:', this.error);
      }
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    }
  }
};
</script>
