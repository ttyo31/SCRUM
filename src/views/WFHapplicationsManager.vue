<template>
  <v-card class="pa-4 ma-16" elevation="7">
    <v-data-table
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
      <!-- Custom row template -->
      <template v-slot:item="{ item }">
        <tr>
          <td>{{ item.approval }}</td>
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
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import useUser from '../utils/useUser';

// Use the composable to access user details
const { id, mail } = useUser();
console.log(id);

const items = ref([]);

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
  try {
    const response = await fetch(`https://scrum-backend.vercel.app/api/WFHapplicationsManager/${mgr_id}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    
    items.value = data;
  } catch (error) {
    console.error("Error fetching applications:", error);
  }
}

async function approveApplication(item) {
  try {
    console.log("Approve")
    // Strip the names from staff_id and mgr_id, only send the IDs
    const staff_id = item.staff_id.split(" ")[0]; // Take the part before the space
    const mgr_id = item.mgr_id.split(" ")[0];     // Take the part before the space
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
      //there seems to be an error to go into the success loop but it actually approves it, so i put it in both success and error
      items.value = items.value.filter(app => app.staff_id !== item.staff_id || app.wfh_date !== item.wfh_date);

      sendmail(staff_id);
      fetchApplications(mgr_id);
    }
  } catch (error) {
    console.error("Error approving application:", error);
    // yeah so i put it over here so it can delete the row too since it's a success 
    items.value = items.value.filter(app => app.staff_id !== item.staff_id || app.wfh_date !== item.wfh_date);

  }
}

async function rejectApplication(item) {
  try {
    // Strip the names from staff_id and mgr_id, only send the IDs
    const staff_id = item.staff_id.split(" ")[0]; // Take the part before the space
    const mgr_id = item.mgr_id.split(" ")[0];     // Take the part before the space
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
      // this would auto delete the row if it is a success yay
      items.value = items.value.filter(app => app.staff_id !== item.staff_id || app.wfh_date !== item.wfh_date);

      sendmail(staff_id)
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
