<template>
  <!-- old nav bar code
    <v-card>
    <v-tabs
      v-model="tab"
      bg-color="primary"
    >
    <router-link to="/"><v-tab value="one" class="text-white">Home</v-tab></router-link>
      <router-link to="/about"><v-tab value="one" class="text-white">calendar</v-tab></router-link>
      <v-tab value="three">Item Three</v-tab>
      <router-link to="/test"><v-tab value="one" class="text-white">Submission Test</v-tab> </router-link>
    </v-tabs>
  </v-card> -->
  <v-app>
    <v-main>
       <!-- Conditionally show Navbar only when not on the login page -->
       <Navbar v-if="showNavbar" />
      <router-view/>  
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
}
</script>


<script setup>
  import { useRoute } from 'vue-router';
  import { computed } from 'vue';
  import Navbar from './components/NavBar.vue'


  const route = useRoute();

  const showNavbar = computed(() => route.path !== '/'); 
  
</script>
