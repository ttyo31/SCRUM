<template>
  <v-app>
    <v-main>
      <!-- Conditionally show Navbar only when not on the login page -->
      <Navbar v-if="showNavbar" />
      <router-view />  

      <!-- Inactivity Warning Dialog -->
      <v-dialog v-model="showWarningDialog" max-width="400px">
        <v-card>
          <v-card-title class="headline">Inactivity Warning</v-card-title>
          <v-card-text>
            You will be logged out in <strong>{{ countdown }}</strong> seconds due to inactivity.
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="resetInactivityTimer">Stay Logged In</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-main>
  </v-app>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import { computed, onBeforeUnmount, ref, watchEffect } from 'vue';
import Navbar from './components/NavBar.vue';
import { supabase } from './utils/supabase'; // Adjust path if necessary

const route = useRoute();
const router = useRouter();
const showNavbar = computed(() => route.path !== '/'); // Hide Navbar on login page

// Authentication State
const isAuthenticated = ref(false);

// Inactivity Timer and Dialog Logic
const inactivityTimer = ref(null);
const countdownTimer = ref(null);
const countdown = ref(60); // Start the countdown at 60 seconds
const showWarningDialog = ref(false);

const logout = async () => {
  await supabase.auth.signOut(); // Log the user out
  router.push('/'); // Redirect to login page
  showWarningDialog.value = false;
  isAuthenticated.value = false; // Reset authentication status
};

const startCountdown = () => {
  showWarningDialog.value = true;
  countdown.value = 60;

  // Update the countdown every second
  countdownTimer.value = setInterval(() => {
    countdown.value -= 1;
    if (countdown.value <= 0) {
      clearInterval(countdownTimer.value);
      logout();
    }
  }, 1000);
};

const resetInactivityTimer = () => {
  if (!isAuthenticated.value) return;

  // Clear existing timers
  clearTimeout(inactivityTimer.value);
  clearInterval(countdownTimer.value);

  // Hide warning dialog if it’s open
  showWarningDialog.value = false;

  // Set a new inactivity timer
  inactivityTimer.value = setTimeout(() => {
    startCountdown();
  }, 2400000); // 4 minutes for activity, leaving 60 seconds for warning
};

// Check authentication status and start timer if logged in
watchEffect(async () => {
  const { data: { user } } = await supabase.auth.getUser();
  isAuthenticated.value = !!user;

  if (isAuthenticated.value) {
    resetInactivityTimer();

    // Add event listeners for user activity when logged in
    window.addEventListener('keydown', resetInactivityTimer);
    window.addEventListener('click', resetInactivityTimer);
  } else {
    // Remove event listeners when not authenticated
    window.removeEventListener('keydown', resetInactivityTimer);
    window.removeEventListener('click', resetInactivityTimer);
  }
});

onBeforeUnmount(() => {
  // Clean up event listeners and timers when the component is unmounted
  window.removeEventListener('mousemove', resetInactivityTimer);
  window.removeEventListener('keydown', resetInactivityTimer);
  window.removeEventListener('click', resetInactivityTimer);
  clearTimeout(inactivityTimer.value);
  clearInterval(countdownTimer.value);
});
</script>

<script>
export default {
  name: 'App',
};
</script>

<style scoped>
.v-dialog {
  text-align: center;
}
</style>
