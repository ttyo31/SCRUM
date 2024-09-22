<template>
  <div class="about">
    <router-link to="/"></router-link>
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
const calendar = ref()
const today = ref([new Date()])
const events = ref([])
const _events = [
  {
    title:"Thuya(A)",
    start: new Date(2024,8,20,30),
    end: new Date(2024,8,20,30),
    color:"red",
    allDay:true
  }
]

function fetchEvents(_events) {
  events.value = _events;  // Assign the events to the reactive events variable
  console.log(events.value)
}

onMounted(() => {
  
  fetchEvents(_events)
})
</script>
