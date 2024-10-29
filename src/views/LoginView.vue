<template>
  <v-container class="form-container centering" fluid>
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="headline"><h1 style="text-align: center;">Login</h1></v-card-title>
          <v-card-text>
            <v-form v-model="valid" ref="form" @submit.prevent="onFinish" @keyup.enter="onFinish">
              <v-text-field
                v-model="formState.email"
                label="Email"
                :rules="[v => !!v || 'Please input your email!']"
                required
              ></v-text-field>

              <v-text-field
                v-model="formState.password"
                label="Password"
                type="password"
                :rules="[v => !!v || 'Please input your password!']"
                required
              ></v-text-field>

              <v-checkbox
                v-model="formState.remember"
                label="Remember me"
              ></v-checkbox>

              <div class="centering"><v-btn type="submit" class="black-button">Submit</v-btn></div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal for error messages -->
    <v-dialog v-model="errorDialog" max-width="400">
      <v-card>
        <v-card-title class="headline">Login Error</v-card-title>
        <v-card-text>
          <p>{{ errorMessage }}</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="closeErrorDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router'; 
import { supabase } from '../utils/supabase';
import useUser from '../utils/useUser';

// Get fetchStaffDetails from composable
const { fetchStaffDetails } = useUser();

// Reactive form state for login
const formState = reactive({
  email: '',
  password: '',
  remember: true,
});

// Error handling
const errorDialog = ref(false);
const errorMessage = ref('');

// Router for navigation
const router = useRouter();

// Handle login form submission
const onFinish = async () => {
  const { email, password } = formState;
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });

  if (data.user) {
    await fetchStaffDetails(data.user.email); 
    // Route to the homepage
    router.push('/home');
    location.reload()
  } else if (error) {
    console.error('Login error:', error.message);
    // Show the error dialog
    errorMessage.value = error.message;
    errorDialog.value = true;
  }
};

// Close error dialog
const closeErrorDialog = () => {
  errorDialog.value = false;
};

</script>

<style scoped>
.form-container {
  min-height: 100vh; 
  background-color: #f5f5f5;
}

.v-card {
  padding: 24px; 
  border-radius: 8px; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
}
.centering {
  display: flex;
  justify-content: center;
  align-items: center;
}

.black-button {
  background-color: white;
  color: black;
  border: solid 1px black;
}
.black-button:hover {
  background-color: black;
  color: white;
}
</style>