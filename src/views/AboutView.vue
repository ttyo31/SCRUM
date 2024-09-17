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
  },
  {
    title:"Thuya(A)",
    start: new Date(2024,8,22,30),
    end: new Date(2024,8,22,30),
    color:"red",
    allDay:true
  },
  {
    title:"Thuya(A)",
    start: new Date(2024,8,23,30),
    end: new Date(2024,8,23,30),
    color:"red",
    allDay:true
  },
  {
    title:"Henry(A)",
    start: new Date(2024,8,15,30),
    end: new Date(2024,8,15,30),
    color:"blue",
    allDay:true
  },
  {
    title:"Henry(A)",
    start: new Date(2024,8,10,30),
    end: new Date(2024,8,10,30),
    color:"blue",
    allDay:true
  },
  {
    title:"Henry(A)",
    start: new Date(2024,8,12,30),
    end: new Date(2024,8,12,30),
    color:"blue",
    allDay:true
  },
  {
    title:"Rianne(A)",
    start: new Date(2024,8,1,30),
    end: new Date(2024,8,1,30),
    color:"green",
    allDay:true
  },
  {
    title:"Rianne(A)",
    start: new Date(2024,8,2,30),
    end: new Date(2024,8,2,30),
    color:"green",
    allDay:true
  },
  {
    title:"Rianne(A)",
    start: new Date(2024,8,3,30),
    end: new Date(2024,8,3,30),
    color:"green",
    allDay:true
  },
  {
    title:"Keona(A)",
    start: new Date(2024,8,10,30),
    end: new Date(2024,8,10,30),
    color:"purple",
    allDay:true
  },
  {
    title:"Keona(A)",
    start: new Date(2024,8,5,30),
    end: new Date(2024,8,5,30),
    color:"purple",
    allDay:true
  },{
    title:"Reg(A)",
    start: new Date(2024,8,22,30),
    end: new Date(2024,8,22,30),
    color:"teal",
    allDay:true
  },
  {
    title:"Reg(A)",
    start: new Date(2024,8,23,30),
    end: new Date(2024,8,23,30),
    color:"teal",
    allDay:true
  },
  {
    title:"Reg(A)",
    start: new Date(2024,8,24,30),
    end: new Date(2024,8,24,30),
    color:"teal",
    allDay:true
  },{
    title:"Riyas(A)",
    start: new Date(2024,8,29,30),
    end: new Date(2024,8,29,30),
    color:"gray",
    allDay:true
  },
]

function fetchEvents(_events) {
  events.value = _events;  // Assign the events to the reactive events variable
  console.log(events.value)
}

onMounted(() => {
  
  fetchEvents(_events)
})
</script>
