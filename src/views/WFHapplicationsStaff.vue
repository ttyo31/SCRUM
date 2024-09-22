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
    </v-data-table>
  </v-card>
</template>


<script setup>
import { ref, onMounted } from 'vue';

const items = ref([]);

async function fetchApplications(staff_id) {
  try {
    const response = await fetch(`http://localhost:5000/WFHapplicationsStaff/${staff_id}`);
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
  const staff_id = 150008;  // Replace with the actual manager ID you want to fetch
  fetchApplications(staff_id);
});
</script>