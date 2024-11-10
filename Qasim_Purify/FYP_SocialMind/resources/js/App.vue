<template>
  <div>
    <RouterView />
  </div>
</template>

<script>
import { RouterView } from 'vue-router';
  export default {
    name: 'App',
  };
</script>



<!-- <script>
import { mapActions } from 'vuex'

export default {
  name: 'App',

  methods: {
    ...mapActions(['checkAuth'])
  },
  created() {
    this.checkAuth()
  }
}
</script> -->
