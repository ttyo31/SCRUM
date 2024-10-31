<template>
  <v-card class="pa-4 ma-16" elevation="7">
    <v-data-table
      v-if="!loading"
      :items="items"
      :headers="headers"
      class="elevation-1"
      :items-per-page="5"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Manager Applications List</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
        </v-toolbar>
      </template>

      <!-- Custom row template -->
      <template v-slot:item="{ item }">
        <tr>
          <!-- <td>{{ item.approval }}</td> -->
          <!-- Display the manager name with the ID -->
          <td>{{ item.mgr_id }} {{ item.manager_name }}</td>
          <!-- Display the staff name with the ID -->
          <td>{{ item.staff_id }} {{ item.staff_name }}</td>
          <td>{{ item.wfh_date }}</td>
          <td>
            <v-btn small color="success" @click="approveApplication(item)">Approve</v-btn>
            <v-btn small color="error" @click="rejectApplication(item)">Reject</v-btn>
          </td>
        </tr>
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

// Use the composable to access user details
const { id, mail } = useUser();
console.log(id);

const items = ref([]);
const loading = ref(true);  // Add loading state
const modalVisible = ref(false);  // Controls the visibility of the modal
const modalTitle = ref("");       // Title for the modal (e.g., Approved/Rejected)
const modalMessage = ref("");     // Message for the modal (e.g., Your request has been approved/rejected)
const headers =[{title: "Approving Manager"}, {title: "Requester"}, {title: "WFH Date"}, {title: "Action"}]

function sendmail(){
 const url = "https://scrumbackend.vercel.app/api/send-email"
  const emailurl = mail.value
  const payload = {
    recipient: emailurl,
    body:"There has been a change to your WFH application"
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

async function fetchApplications(mgr_id) {
  loading.value = true;  // Set loading to true before fetching data
  try {
    const response = await fetch(`https://scrum-backend.vercel.app/api/WFHapplicationsManager/${mgr_id}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    items.value = data;
  } catch (error) {
    console.error("Error fetching applications:", error);
  } finally {
    loading.value = false;  // Set loading to false after data is fetched
  }
}

async function approveApplication(item) {
  try {
    console.log("Approve")
    const staff_id = item.staff_id.split(" ")[0];
    const mgr_id = item.mgr_id.split(" ")[0];
    const response = await fetch('https://scrumbackend.vercel.app/api/approve_application', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        staff_id: staff_id,
        mgr_id: mgr_id,
        wfh_date: item.wfh_date,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    if (result.success) {
      items.value = items.value.filter(app => app.staff_id !== item.staff_id || app.wfh_date !== item.wfh_date);
      modalTitle.value = "Approved";
      modalMessage.value = "The request has been approved successfully.";
      modalVisible.value = true;
      sendmail(staff_id);
      fetchApplications(mgr_id);
    }
  } catch (error) {
    console.error("Error approving application:", error);
  }
}

async function rejectApplication(item) {
  try {
    const staff_id = item.staff_id.split(" ")[0];
    const mgr_id = item.mgr_id.split(" ")[0];
    const response = await fetch('https://scrum-backend.vercel.app/api/reject_application', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        staff_id: staff_id,
        mgr_id: mgr_id,
        wfh_date: item.wfh_date,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    if (result.success) {
      items.value = items.value.filter(app => app.staff_id !== item.staff_id || app.wfh_date !== item.wfh_date);
      modalTitle.value = "Rejected";
      modalMessage.value = "The request has been rejected.";
      modalVisible.value = true;
      sendmail(staff_id);
      fetchApplications(mgr_id);
    }
  } catch (error) {
    console.error("Error approving application:", error);
  }
}

onMounted(() => {
  const mgr_id = id.value;
  fetchApplications(mgr_id);
});
</script>

<style scoped>
.v-btn {
  border-radius: 30px;
  margin-right: 5px;

}

</style>

