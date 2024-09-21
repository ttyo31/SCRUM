<template>
  <v-card class="pa-4 ma-16" elevation="7">
    <!-- <div class="centering ma-8"><h1 style="text-align: center; margin: 0px;">WFH Application Form</h1></div> -->
    <v-form ref="form" v-model="valid" @submit.prevent="onSubmit">
      <v-row>

        <!-- select date -->
        <v-col cols="12" md="6">
          <div class="centering">
          <v-date-picker
            v-model="formData.wfh_date"
            no-title
            scrollable
            @input="menu = false"
          ></v-date-picker>
          </div>
        </v-col>

        <!-- input Staff ID -->
        <v-col cols="12" md="5">
          <div class="centering ma-16 mr-16">
          <v-text-field
            v-model="formData.staff_id"
            label="Staff ID"
            :rules="[v => !!v || 'Please input your Staff ID!']"
            required
          ></v-text-field>
          </div>
        </v-col>

        <v-col cols="12" md="1"></v-col>
      </v-row>

      <!-- submit button -->
      <div class="centering"><v-btn type="submit" class="black-button">Submit</v-btn></div>
      
      <!-- feedback dialog for application error -->
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title class="headline">Error</v-card-title>
          <v-card-text>{{ dialogMessage }}</v-card-text>
          <v-card-actions>
            <v-btn color="error" text @click="dialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- feedback dialog for application success -->
      <v-dialog v-model="successDialog" max-width="500px">
        <v-card>
          <v-card-title class="headline">Success</v-card-title>
          <v-card-text>Your WFH request has been submitted successfully!</v-card-text>
          <v-card-actions>
            <v-btn color="success" text @click="successDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </v-form>
  </v-card>
</template>

<script setup>
import { ref } from 'vue';
import { supabase } from '../utils/supabase';

const formData = ref({
  staff_id: null,
  wfh_date: null,
});
const dialog = ref(false);
const dialogMessage = ref('');
const successDialog = ref(false);
const menu = ref(false);
const valid = ref(true);

const onSubmit = async () => {
  if (!valid.value) return;

  try {
    const { data: staffData, error: staffError } = await supabase
      .from('staff')
      .select('mgr_id')
      .eq('id', formData.value.staff_id)
      .single();

    if (staffError || !staffData) {
      showDialog('Error fetching manager ID or staff not found');
      return;
    }

    const mgr_id = staffData.mgr_id;

    const { error: applicationError } = await supabase
      .from('applications')
      .insert([
        {
          staff_id: formData.value.staff_id,
          mgr_id: mgr_id,
          wfh_date: formData.value.wfh_date,
          approval: 0,
        }
      ]);

    if (applicationError) {
      showDialog('Error submitting application: ' + applicationError.message);
    } else {
      successDialog.value = true;
      formData.value.staff_id = null;
      formData.value.wfh_date = null;
    }
  } catch (err) {
    showDialog('An unexpected error occurred: ' + err.message);
  }
};

const showDialog = (message) => {
  dialogMessage.value = message;
  dialog.value = true;
};
</script>

<style scoped>
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