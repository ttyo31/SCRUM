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
          <v-toolbar-title>Staff Applications List</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
        </v-toolbar>
      </template>

      <!-- Custom row template -->
      <!-- Custom row template -->
      <template v-slot:item="{ item }">
        <tr>
          <td>
            <span
              :style="{
                color: item.approval === 1 ? 'green' : item.approval === 2 ? 'red' : 'orange'
              }"
            >
              {{ item.approval === 1 ? 'Approved' : item.approval === 2 ? 'Rejected' : 'Pending' }}
            </span>
          </td>
          <!-- Display the manager name with the ID -->
          <td>{{ item.mgr_id }} {{ item.manager_name }}</td>
          <!-- Display the staff name with the ID -->
          <td>{{ item.staff_id }} {{ item.staff_name }}</td>
          <td>{{ item.wfh_date }}</td>
          
        </tr>
      </template>

      <!-- Show when there's no data -->
      <template v-slot:no-data>
        <v-alert>No applications available</v-alert>
      </template>

    </v-data-table>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import useUser from '../utils/useUser';

const items = ref([]);
// const headers = [
//   { text: 'Mgr_id', value: 'mgr_id' },
//   { text: 'Staff_id', value: 'staff_id' },
//   { text: 'Wfh_date', value: 'wfh_date' },
//   { text: 'Approval', value: 'approval' }
// ];

const { id } = useUser();

async function fetchApplications(staff_id) {
  try {
    const response = await fetch(`https://scrum-backend-nduvy27uf-riannes-projects.vercel.app/api/WFHapplicationsStaff/${staff_id}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    items.value = data;  // Update your items state
  } catch (error) {
    console.error("Error fetching applications:", error);
  }
}

onMounted(() => {
  const staff_id = id.value; //can put a placeholder here if anyone not sure
  fetchApplications(staff_id);
});
</script>
