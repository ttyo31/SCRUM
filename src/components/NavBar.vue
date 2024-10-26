<template>
  <v-toolbar color="primary">
    <v-toolbar-title class="text-white">WFH SYSTEM</v-toolbar-title>
    
    <v-tabs v-model="tab" class="ml-auto" background-color="transparent" slider-color="white">
      <router-link to="/home">
        <v-tab value="one" class="text-white">Home</v-tab>
      </router-link>
      
      <router-link to="/myschedule">
        <v-tab value="two" class="text-white">My Schedule</v-tab>
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
            value="five"
            class="text-white"
            v-bind="props"
          >
            WFH Application
          </v-tab>
        </template>
        
        <v-list class="transparent-dropdown" style="width: 100;">
          <v-list-item v-if="id != '130002'">
            <router-link to="/WFHrequestForm">
              <v-list-item-title>Request Form</v-list-item-title>
            </router-link>
          </v-list-item>
          <v-list-item v-if="role == 1 || role == 3">
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

      <v-spacer></v-spacer>

      <!-- Notifications Dropdown -->
      <v-menu v-model="notificationsVisible" :close-on-content-click="true" offset-y transition="scale-transition" style="z-index:1000;">
        <template #activator="{ props }">
          <div style="display: flex; align-items: center; justify-content: center;" value="six">
            <!-- Notifications Icon with Badge -->
            <v-tab icon @click="toggleNotifications" class="text-white align-center" v-bind="props">
              <v-icon>mdi-bell</v-icon>
              <v-badge v-if="unreadNotifications > 0" :content="unreadNotifications" color="red" overlap />
            </v-tab>
          </div>
        </template>
        <v-list class="transparent-dropdown">
          <v-list-item v-for="notification in notifications" :key="notification.id">
            <v-list-item-content>
              <v-list-item-title>{{ notification.message }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item v-if="notifications.length === 0">
            <v-list-item-title>No new notifications</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-tabs>

    <!-- Log Out button placed at the far right -->
    <v-spacer></v-spacer>
    <v-btn @click="logOut" color="white">
      Log Out
    </v-btn>
  </v-toolbar>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'; // Import the router to redirect
import { supabase } from '../utils/supabase'; // Ensure Supabase is properly configured
import useUser from '../utils/useUser'; // Import the useUser composable

const tab = ref('one'); // Default selected tab
const dropdownVisible = ref(false); // Control visibility of the dropdown
const notificationsVisible = ref(false); // Control visibility of notifications dropdown
const unreadNotifications = ref(0); // Number of unread notifications
const notifications = ref([]); // Array to hold notification messages

// Access user details using the composable
const { role, dept, clearUserData, id } = useUser(); // Assuming user ID is available in useUser composable

// Access the router for navigation
const router = useRouter();

// Function to handle logging out
const logOut = () => {
  clearUserData(); // Clear the user data from localStorage
  router.push('/'); // Redirect the user to the login page
};

// Fetch notifications from Supabase
async function fetchNotifications() {
  try {
    const { data: notificationsData, error } = await supabase
      .from('notifications')
      .select('*')
      .eq('staff_id', id.value)
      .eq('status', 'unread');

      console.log('Current User ID:', id.value); // Log the current user ID

    if (error) {
      throw new Error(error.message);
    }

    console.log('Fetched Notifications:', notificationsData); // Log notifications to ensure they are fetched
    notifications.value = notificationsData || [];
    unreadNotifications.value = notifications.value.length;
  } catch (error) {
    console.error('Error fetching notifications:', error);
  }
}

// Toggle notifications dropdown and mark as read when opened
const toggleNotifications = async () => {
  notificationsVisible.value = !notificationsVisible.value;
  if (notificationsVisible.value) {
    // Mark all notifications as read
    const { error } = await supabase
      .from('notifications')
      .update({ status: 'read' })
      .eq('staff_id', id.value); // Update the notifications for the logged-in user

    if (error) {
      console.error('Error marking notifications as read:', error);
    } else {
      unreadNotifications.value = 0; // Reset the unread count
    }
  }
};
// commented it out cuz code won't run 
// Real-time notification listener using Supabase subscription
// function listenToNotifications() {
//   const notificationSubscription = supabase
//     .from(`notifications:staff_id=eq.${id.value}`) // Subscribe to notifications table for this user
//     .on('INSERT', payload => {
//       console.log('New notification:', payload.new); // Log new notification
//       notifications.value.push(payload.new); // Add the new notification to the list
//       unreadNotifications.value += 1; // Increase unread notification count
//     })
//     .subscribe();
// }

// Mounted hook for fetching notifications and setting up real-time listener
onMounted(() => {
  fetchNotifications(); // Fetch notifications when the navbar is mounted
  // listenToNotifications(); // Set up real-time listener for new notifications
});
</script>

<style scoped>
v-toolbar {
  position: sticky;
}
.transparent-dropdown {
  background-color: rgba(255, 255, 255, 0.8);
  max-height: 300px; /* Set a max height for the dropdown */
  overflow-y: auto; /* Enable scrolling if content exceeds the height */
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