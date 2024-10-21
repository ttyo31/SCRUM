<template>
  <!-- <v-card class="pa-4 ma-16" elevation="7"> -->
    <div class="centering ma-10"></div>
    <v-form ref="form" v-model="valid" @submit.prevent="onSubmit">
      <div class="centering">
        <v-date-picker
          v-model="formData.wfh_date"
          no-title
          scrollable
          @input="menu = false"
        ></v-date-picker>
      </div>

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
  <!-- </v-card> -->
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '../utils/supabase';
import useUser from '../utils/useUser';

// Access the user data from the composable
const { id, mgr_id } = useUser();

const formData = ref({
  staff_id: null,
  wfh_date: null,
});

const dialog = ref(false);
const dialogMessage = ref('');
const successDialog = ref(false);
const menu = ref(false);
const valid = ref(true);

// Prefill staff_id and mgr_id from useUser
onMounted(() => {
  formData.value.staff_id = id.value;
});

//this email will be sent to manager for approval upon submission.
function sendemail(){

  //fit here

  const mgr_url = `https://scrumbackend.vercel.app/api/manageremail/${mgr_id.value}`
  const url = "https://scrumbackend.vercel.app/api/send-email"
  fetch(mgr_url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse the JSON response
  })
  .then(data => {
    const email = data.email
    const message = `There is WFH request by ${id.value} to be approved`
  const payload = {
    recipient: email,
    body:message
  }
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',  // Important: specify JSON content type
    },
    body: JSON.stringify(payload),  // Convert the payload to a JSON string
  }).then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('POST request successful:', data);
    })
    .catch(error => {
      console.error('Error with POST request:', error);
    });
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });


  // const message = "There is WFH request to be approved"
  // const payload = {
  //   recipient: recipient,
  //   body:message
  // }
  // fetch(url, {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',  // Important: specify JSON content type
  //   },
  //   body: JSON.stringify(payload),  // Convert the payload to a JSON string
  // }).then(response => {
  //     if (!response.ok) {
  //       throw new Error(`HTTP error! status: ${response.status}`);
  //     }
  //     return response.json();
  //   })
  //   .then(data => {
  //     console.log('POST request successful:', data);
  //   })
  //   .catch(error => {
  //     console.error('Error with POST request:', error);
  //   });
}

const onSubmit = async () => {
  if (!valid.value) return;

  try {
    // Since mgr_id is available from useUser.js, no need to fetch from Supabase again
    const applicationData = {
      staff_id: formData.value.staff_id,
      mgr_id: mgr_id.value,  // Use the manager ID from useUser.js
      wfh_date: formData.value.wfh_date,
      approval: 0, // Default approval status is pending
    };

    const { error: applicationError } = await supabase
      .from('applications')
      .insert([applicationData]);

    if (applicationError) {
      showDialog('Error submitting application: ' + applicationError.message);
    } else {
      successDialog.value = true;
      formData.value.wfh_date = null; // Reset the date picker
      sendemail()
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