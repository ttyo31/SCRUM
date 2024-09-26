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
      <template v-slot:item="{ item }">
        <tr>
          <td>{{ item.approval }}</td>
          <td>{{ item.mgr_id }}</td>
          <td>{{ item.staff_id }}</td>
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
const { id } = useUser();
console.log(id);

const items = ref([]);

async function fetchApplications(mgr_id) {
  try {
    const response = await fetch(`http://localhost:5000/WFHapplicationsManager/${mgr_id}`);
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
    const response = await fetch('http://localhost:5000/approve_application', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        staff_id: item.staff_id,
        mgr_id: item.mgr_id,
        wfh_date: item.wfh_date,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    if (result.success) {
      // Optionally, you can refresh the list of applications after approval
      fetchApplications(item.mgr_id);
    }
  } catch (error) {
    console.error("Error approving application:", error);
  }
}

async function rejectApplication(item) {
  try {
    const response = await fetch('http://localhost:5000/reject_application', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        staff_id: item.staff_id,
        mgr_id: item.mgr_id,
        wfh_date: item.wfh_date,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    if (result.success) {
      // Optionally, you can refresh the list of applications after approval
      fetchApplications(item.mgr_id);
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
