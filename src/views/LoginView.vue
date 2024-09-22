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
import { reactive } from 'vue';
import { supabase } from '../utils/supabase';


const formState = reactive({
  email: '',
  password: '',
  remember: true,
});

const onFinish = async () => {
  const { email, password } = formState;
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });

  if (data.user) {
    fetchStaffDetails(data.user); 
  } else if (error) {
    console.error('Login error:', error.message);
  }
};

const fetchStaffDetails = async (user) => {
  const { data, error } = await supabase
    .from('staff')
    .select('*')
    .eq('mail', user.email);

  if (data && data.length > 0) {
    console.log('Staff details:', data[0]);
    // Do something with staff data
  } else if (error) {
    console.error('Error fetching staff details:', error);
  }
};


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
