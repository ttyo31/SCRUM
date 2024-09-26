<template>
  <div class="about">
    <v-row class="fill-height">
      <v-col>
        <v-sheet height="600">
          <v-calendar
            ref="calendar"
            v-model="today"
            :events="events"
            color="primary"
            type="month"
          ></v-calendar>
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import useUser from '../utils/useUser';

// Use the composable to access user details
const { id } = useUser();

const today = ref([new Date()])
const events = ref([])

// Fetch WFH events from Flask backend for a specific manager
async function fetchStaffEvents(userID) {
  try {
    const response = await axios.get(`http://localhost:5000/api/wfh_events/${userID}`)

    // Transform the response data into a format suitable for the calendar
    events.value = response.data.map(event => ({
      title: `${event.fname} ${event.lname}`,
      start: new Date(event.wfh_date),
      end: new Date(event.wfh_date),  // Assuming one-day events
      color: "blue",                  // Optional: color for the event
      allDay: true                    // Mark as an all-day event
    }))
  } catch (error) {
    console.error('Error fetching WFH events:', error)
  }
}

// On component mount, fetch the events for a specific department (e.g., id = "140003")
onMounted(() => {
  const userID = id.value;  // Set id
  fetchStaffEvents(userID)
})
</script>