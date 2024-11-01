<template>
  <v-card class="pa-4 ma-16" elevation="7">
    <v-data-table v-if="!loading" :items="items" :headers="headers" class="elevation-1" :items-per-page="5">
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>My Applications</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
        </v-toolbar>
      </template>

      <!-- Custom row template -->
      <template v-slot:item="{ item }">
        <tr class="hover-row">

          <td>{{ item.date_of_application }}</td>
          <!-- Display the manager name with the ID -->
          <td>{{ item.mgr_id }}</td>
          <!-- Display the staff name with the ID -->
          <td>{{ item.staff_id }}</td>
          <td>{{ item.wfh_date }}</td>
          <td>
            <span :style="{
              color: item.approval === 1 ? 'green' : item.approval === 2 ? 'red' : 'orange'
            }">
              {{ item.approval === 1 ? 'Approved' : item.approval === 2 ? 'Rejected' : 'Pending' }}
            </span>
          </td>


          <td>
            <v-btn color="warning" v-if="item.approval === 1" @click="removeWfh(item.wfh_date, item.staff_id)">
              Withdraw
            </v-btn>
            <v-btn color="warning" v-else-if="item.approval === 0"
              @click="withdraw_application(item.wfh_date, item.staff_id)" class="withdraw">
              Withdraw
            </v-btn>
          </td>

        </tr>
      </template>

      <!-- Show when there's no data -->
      <template v-slot:no-data>
        <v-alert>No applications available</v-alert>
      </template>

    </v-data-table>

    <!-- Display loading spinner while data is being fetched -->
    <v-container v-if="loading" class="d-flex justify-center align-center" style="height: 200px;">
      <v-progress-circular indeterminate color="primary" size="70"></v-progress-circular>
    </v-container>

    <!-- Modal for Approval/Rejection Notification -->
    <v-dialog v-model="modalVisible" max-width="400">
      <v-card>
        <v-card-title class="headline">{{ modalTitle }}</v-card-title>
        <v-card-text>{{ modalMessage }}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="modalVisible = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import useUser from '../utils/useUser';

const headers = [{ title: 'Application Date' }, { title: 'Approving Manager' }, { title: 'Requester' }, { title: 'WFH Date' }, { title: 'Status' }, { title: 'Action' }]
const items = ref([]);
const modalVisible = ref(false);  // Controls the visibility of the modal
const modalTitle = ref("");       // Title for the modal 
const modalMessage = ref("");     // Message for the modal
const loading = ref(true);  // Add loading state

const { id, mail } = useUser();

function sendmail() {
  const url = "https://scrumbackend.vercel.app/api/send-email"
  const emailurl = mail.value
  const payload = {
    recipient: emailurl,
    body: "Your WFH date has been changed"
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
}

async function fetchApplications(staff_id) {
  try {
    items.value = [];
    const response = await fetch(`https://scrum-backend.vercel.app/api/WFHapplicationsStaff/${staff_id}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    items.value = data;  // Update your items state
  } catch (error) {
    console.error("Error fetching applications:", error);
  } finally {
    loading.value = false;  // Set loading to false after data is fetched
  }
}
function removeWfh(date, id) {
  console.log("this is to remove")
  console.log(date)
  console.log(id.split(" ")[0]) //this is coz staff_id returns id then the name
  // Now need to call applicationstatus.py one of the functions. which will remove it.
  const url = "https://scrumbackend.vercel.app/api/remove_wfh"
  const payload = {
    id: id.split(" ")[0],
    wfh_date: date,
  };
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

    // Show the modal with the success message
    modalTitle.value = "Removed";
    modalMessage.value = "The request has been removed successfully.";
    modalVisible.value = true;


    sendmail()
    // auto remove the row after clicking on remove yay
    const index = items.value.findIndex(item => item.wfh_date === date && item.staff_id.split(" ")[0] === id.split(" ")[0]);
    if (index !== -1) {
      items.value.splice(index, 1);  // Remove the item from the array
    }
    return response.json();
  })
    .then(data => {

      console.log('POST request successful:', data);
    })
    .catch(error => {
      console.error('Error with POST request:', error);
    });
}

function withdraw_application(date, id) {
  const url = "https://scrum-backend.vercel.app/api/withdraw_application"
  const payload = {
    id: id.split(" ")[0],
    wfh_date: date,
  };
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

    // Show the modal with the success message
    modalTitle.value = "Withdrawn";
    modalMessage.value = "The request has been withdrawn successfully.";
    modalVisible.value = true;


    sendmail()
    // auto remove the row after withdraw is clicked woohoo
    const index = items.value.findIndex(item => item.wfh_date === date && item.staff_id.split(" ")[0] === id.split(" ")[0]);
    if (index !== -1) {
      items.value.splice(index, 1);  // Remove the item from the array
    }
    return response.json();

  })
    .then(data => {

      console.log('POST request successful:', data);
    })
    .catch(error => {
      console.error('Error with POST request:', error);
    });
}




onMounted(() => {
  const staff_id = id.value; //can put a placeholder here if anyone not sure
  fetchApplications(staff_id);
});


</script>

<style scoped>
.v-btn {
  border-radius: 30px;
}

.remove:hover {
  background-color: rgba(255, 0, 0, 0.4);
  border: solid 2px rgba(135, 206, 250, 0.1);
}

.remove {
  border: solid 2px red;
}

.withdraw:hover {
  background-color: rgba(255, 165, 0, 0.5);
  border: solid 2px rgba(135, 206, 250, 0.1);
}

.hover-row:hover {
  background-color: rgba(135, 206, 250, 0.1);
}
</style>