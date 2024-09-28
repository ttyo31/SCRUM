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

      <router-link to="/TeamSchedule">
        <v-tab value="three" class="text-white">Team Schedule</v-tab>
      </router-link>

      <router-link v-if="role == 1 || dept === 'HR'" to="/OverallSchedule">
        <v-tab value="four" class="text-white">Overall Schedule</v-tab>
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
            value="three"
            class="text-white"
            v-bind="props"
          >
            WFH Application
          </v-tab>
        </template>
        
        <v-list class="transparent-dropdown" style="width: 100;">
          <v-list-item>
            <router-link to="/WFHrequestForm">
              <v-list-item-title>Request Form</v-list-item-title>
            </router-link>
          </v-list-item>
          <v-list-item>
            <router-link to="/WFHapplicationsManager">
              <v-list-item-title>Manager Application Summary</v-list-item-title>
            </router-link>
          </v-list-item>
          <v-list-item>
            <router-link to="/WFHapplicationsStaff">
              <v-list-item-title>Staff Application Summary</v-list-item-title>
            </router-link>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-tabs>
    
    <!-- Log Out button placed at the far right -->
    <v-spacer></v-spacer>
    <v-btn @click="logOut" color="secondary" class="text-white">
      Log Out
    </v-btn>
  </v-toolbar>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'; // Import the router to redirect
import useUser from '../utils/useUser'; // Import the useUser composable

const tab = ref('one'); // Default selected tab
const dropdownVisible = ref(false); // Control visibility of the dropdown

// Access user details using the composable
const { role, dept, clearUserData } = useUser();

// Access the router for navigation
const router = useRouter();

// Function to handle logging out
const logOut = () => {
  clearUserData(); // Clear the user data from localStorage
  router.push('/'); // Redirect the user to the login page
};

// Mounted hook for debugging user role and department
onMounted(() => {
  console.log('User role:', role.value);
  console.log('User department:', dept.value);
});
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
