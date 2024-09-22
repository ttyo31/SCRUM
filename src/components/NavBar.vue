<template>
    <v-toolbar color="primary">
      <v-toolbar-title class="text-white">WFH SYSTEM</v-toolbar-title>
      
      <v-tabs v-model="tab" class="ml-auto" background-color="transparent" slider-color="white">
        <router-link to="/home">
          <v-tab value="one" class="text-white">Home</v-tab>
        </router-link>
        
        <router-link to="/about">
          <v-tab value="two" class="text-white">Calendar</v-tab>
        </router-link>
        
        <router-link to="/test">
          <v-tab value="three" class="text-white">Submission Test</v-tab>
        </router-link>
        
        <v-menu
          v-model="dropdownVisible"
          offset-y
          :close-on-content-click="true"
          transition="scale-transition"
          style="z-index: 1000;"
        >
          <template #activator="{ props }">
            <v-tab
              value="four"
              class="text-white"
              v-bind="props"
            >
              WFH Application
            </v-tab>
          </template>
          
          <v-list
            class="transparent-dropdown"
            style="width: 100;"
          >
            <v-list-item>
              <router-link to="/WFHrequestForm">
                <v-list-item-title>Request Form</v-list-item-title>
              </router-link>
            </v-list-item>
            <v-list-item>
              <router-link to="/WFHapplications">
                <v-list-item-title>Application Summary</v-list-item-title>
              </router-link>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-tabs>
    </v-toolbar>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const tab = ref('one'); // Default selected tab
  const dropdownVisible = ref(false); // Control visibility of the dropdown
  </script>
  
  <style scoped>
  v-toolbar {
    position: sticky;
  }
  .transparent-dropdown {
    background-color: rgba(255, 255, 255, 0.8);
    box-shadow: none !important; /* No elevation */
    border-radius: 4px;
  }
  
  .v-list-item {
    transition: background-color 0.3s;
    text-decoration: none !important;
    color: inherit;
  }

  .v-list-item-title {
    color: black;
  }
  </style>
  