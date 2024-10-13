<template>
  <div class="about">
    <v-row class="fill-height">
      <v-col>
        <v-select
          v-model="selectedDept"
          :items="departments"
          label="Filter by Department"
          outlined
          dense
        ></v-select>
        <v-sheet height="600">
          <v-calendar
            ref="calendar"
            v-model="today"
            :events="filteredEvents"
            color="primary"
            type="month"
          ></v-calendar>
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const today = ref([new Date()])
const events = ref([])
const selectedDept = ref('All') // Default selection for all departments
const departments = ref(['All', 'HR', 'Engineering', 'Marketing', 'Sales', 'Finance']) // Add more departments

// Fetch WFH events from Flask backend
async function fetchOverallEvents() {
  try {
    const response = await axios.get(`https://scrum-backend.vercel.app/api/all_wfh_events`)

    // Define a color mapping based on department
    const deptColors = {
      "HR": "blue",
      "Engineering": "green",
      "Marketing": "red",
      "Sales": "orange",
      "Finance": "purple",
      "default": "gray"  // Fallback color if department is not listed
    }

    // Transform the response data into a format suitable for the calendar
    events.value = response.data.map(event => ({
      title: `${event.fname} ${event.lname}`,
      start: new Date(event.wfh_date),
      end: new Date(event.wfh_date),  // Assuming one-day events
      dept: event.dept,               // Store department info for filtering
      color: deptColors[event.dept] || deptColors["default"],  // Assign color based on department
      allDay: true                    // Mark as an all-day event
    }))
  } catch (error) {
    console.error('Error fetching WFH events:', error)
  }
}

// Filter events based on the selected department
const filteredEvents = computed(() => {
  if (selectedDept.value === 'All') {
    return events.value
  } else {
    return events.value.filter(event => event.dept === selectedDept.value)
  }
})

// On component mount, fetch the events
onMounted(() => {
  fetchOverallEvents()
})
</script>