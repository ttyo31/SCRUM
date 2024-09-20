<template>
    <a-card>
      <a-form
        :form="form"
        layout="vertical"
        @submit.prevent="onSubmit"
      >
        <!-- Staff ID Input -->
        <a-form-item
          label="Staff ID"
          :rules="[{ required: true, message: 'Please input your Staff ID!' }]"
        >
          <a-input v-model:value="formData.staff_id" placeholder="Enter your Staff ID" />
        </a-form-item>
  
        <!-- WFH Date Picker -->
        <a-form-item
          label="WFH Date"
          :rules="[{ required: true, message: 'Please select your Work From Home date!' }]"
        >
          <a-date-picker
            v-model:value="formData.wfh_date"
            placeholder="Select WFH Date"
          />
        </a-form-item>
  
        <!-- Submit Button -->
        <a-form-item>
          <a-button type="primary" html-type="submit">Submit</a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { message } from 'ant-design-vue';
  import { supabase } from '../utils/supabase'; // Ensure Supabase is set up correctly
  
  // Form data object
  const formData = ref({
    staff_id: null,
    wfh_date: null,
  });
  
  const onSubmit = async () => {
    try {
      // Retrieve manager id (mgr_id) based on the entered staff_id from the 'staff' table
      const { data: staffData, error: staffError } = await supabase
        .from('staff')
        .select('mgr_id')
        .eq('id', formData.value.staff_id)
        .single(); // Assuming staff_id is unique, using .single() ensures only one result
  
      if (staffError || !staffData) {
        message.error('Error fetching manager ID or staff not found: ' + (staffError?.message || 'No staff found'));
        return;
      }
  
      const mgr_id = staffData.mgr_id;
  
      // Insert the data into the 'applications' table
      const { error: applicationError } = await supabase
        .from('applications')
        .insert([
          {
            staff_id: formData.value.staff_id,
            mgr_id: mgr_id,  // Automatically fetched based on staff_id
            wfh_date: formData.value.wfh_date,
            approval: 0 // Pending approval by default
          }
        ]);
  
      if (applicationError) {
        message.error('Error submitting application: ' + applicationError.message);
      } else {
        message.success('WFH request submitted successfully!');
        // Reset the form after successful submission
        formData.value.staff_id = null;
        formData.value.wfh_date = null;
      }
    } catch (err) {
      message.error('An unexpected error occurred: ' + err.message);
    }
  };
  </script>
  
  <style scoped>
  /* You can add custom styles if needed */
  </style>
  