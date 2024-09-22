<template>
  <div class="form-container">
    <a-form
      :model="formState"
      name="basic"
      :label-col="{ span: 8 }"
      :wrapper-col="{ span: 16 }"
      autocomplete="off"
      @finish="onFinish"
      @finishFailed="onFinishFailed"
    >
      <a-form-item
        label="Email"
        name="email"
        :rules="[{ required: true, message: 'Please input your email!' }]"
      >
        <a-input v-model:value="formState.email" />
      </a-form-item>

      <a-form-item
        label="Password"
        name="password"
        :rules="[{ required: true, message: 'Please input your password!' }]"
      >
        <a-input-password v-model:value="formState.password" />
      </a-form-item>

      <a-form-item name="remember" :wrapper-col="{ offset: 8, span: 16 }">
        <a-checkbox v-model:checked="formState.remember">Remember me</a-checkbox>
      </a-form-item>

      <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
        <a-button type="primary" html-type="submit">Submit</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { supabase } from '../utils/supabase';
import { useRouter } from 'vue-router'; 

// Reactive form state for login
const formState = reactive({
  email: '',
  password: '',
  remember: true,
});

// Router for navigation
const router = useRouter();

// Reactive references for staff details
const fname = ref('');
const lname = ref('');

// Handle login form submission
const onFinish = async () => {
  const { email, password } = formState;
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });

  if (data.user) {
    await fetchStaffDetails(data.user); 
    // Route to the homepage after fetching staff details
    router.push('/home');
  } else if (error) {
    console.error('Login error:', error.message);
  }
};

// Fetch staff details by email and store fname and lname
const fetchStaffDetails = async (user) => {
  const { data, error } = await supabase
    .from('staff')
    .select('*')
    .eq('mail', user.email); // Assuming 'mail' column is used for the email

  if (data && data.length > 0) {
    console.log('Staff details:', data[0]);
    fname.value = data[0].fname;
    lname.value = data[0].lname;
  } else if (error) {
    console.error('Error fetching staff details:', error);
  }
};

// Handle form submission failure
const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};

</script>

<style scoped>
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh; 
  background-color: #f5f5f5;
}

a-form {
  background: white; 
  padding: 24px; 
  border-radius: 8px; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
}
</style>
