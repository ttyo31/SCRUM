<template>
  <v-card>
    <v-tabs
      v-model="tab"
      bg-color="primary"
    >
    <router-link to="/"><v-tab value="one" class="text-white">Home</v-tab></router-link>
      <router-link to="/about"><v-tab value="one" class="text-white">calendar</v-tab></router-link>
      <v-tab value="three">Item Three</v-tab>
    </v-tabs>
  </v-card>
  <v-app>
    <v-main>
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
