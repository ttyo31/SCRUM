<template>
  <div class="about">
    <v-row class="fill-height">
      <v-col>
        <div style="padding: 10px; position: absolute; display: flex; justify-content: flex-end; align-items: center; width: 100%;">
          <v-select v-model="selectedDept" :items="departments" class="mt-4 me-2 w-50" label="Filter by Department"
            variant="outlined" outlined dense style="max-width: 200px"></v-select>

          <v-select v-model="viewMode" :items="viewModes" label="Select View Mode" outlined variant="outlined" dense
            class="mt-4 w-50 me-2" style="max-width: 200px"></v-select>
        </div>

        <v-sheet height="600" class="mt-4">
          <div id="loading" v-if="!calendarReady" class="d-flex justify-center align-center">
            <v-progress-circular indeterminate color="primary" size="70"></v-progress-circular>
          </div>

          <template v-else>
            <template v-if="viewMode === 'Calendar'">
              <v-calendar id="calendar" ref="calendar" v-model="today" :events="filteredEvents" color="primary"
                type="month" style="padding: 10px; padding-top: 20px;"></v-calendar>
            </template>
            <template v-else>
              <div id="dashboard" style="display: flex; flex-direction: column; align-items: center;">
                <v-text-field v-model="searchQuery" label="Search Employee Name" class="mt-4 w-50" outlined dense
                  style="max-width: 300px" />

                <v-simple-table class="elevation-1">
                  <thead>
                    <tr style="border-bottom: 2px solid #000; background-color: #f5f5f5;">
                      <th style="padding: 8px; border-right: 1px solid #ddd;">Employee Name</th>
                      <th v-for="day in next7Days" :key="day" style="padding: 8px; border-right: 1px solid #ddd;">
                        {{ formatDate(day) }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="employee in filteredEmployees" :key="employee.id" style="border: 1px solid #ddd;">
                      <td style="padding: 8px; border-right: 1px solid #ddd;">
                        {{ employee.name }}
                      </td>
                      <td v-for="day in next7Days" :key="day"
                        style="padding: 8px; border-right: 1px solid #ddd; text-align: center;">
                        <template v-if="day.getDay() === 0 || day.getDay() === 6">
                          <!-- Check for Sunday (0) or Saturday (6) -->
                          <span :style="{ color: 'orange' }">Weekend</span>
                        </template>
                        <template v-else>
                          <span :style="{ color: 'red' }" v-if="isOnWFH(employee, day)">WFH</span>
                          <span :style="{ color: 'green' }" v-else>Office</span>
                        </template>
                      </td>
                    </tr>
                  </tbody>
                </v-simple-table>
              </div>
            </template>
          </template>
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { format } from 'date-fns' // Import date-fns for date formatting

const today = ref(new Date())
const events = ref([])
const employees = ref([])
const selectedDept = ref('All')
const departments = ref(['All', 'HR', 'Engineering', 'Marketing', 'Sales', 'Finance'])
const viewMode = ref('Calendar')
const viewModes = ref(['Calendar', 'Dashboard'])
const calendarReady = ref(false)
const searchQuery = ref(''); // New search query reactive variable

const next7Days = computed(() => {
  const days = []
  const startOfWeek = new Date(today.value)
  const dayOfWeek = startOfWeek.getDay() // Get the current day of the week (0-6)
  startOfWeek.setDate(startOfWeek.getDate() - dayOfWeek + 1) // Set to the last Sunday

  for (let i = 0; i < 7; i++) {
    const date = new Date(startOfWeek)
    date.setDate(startOfWeek.getDate() + i)
    days.push(date)
  }
  return days
})


async function fetchOverallEvents() {
  try {
    const eventsResponse = await axios.get(`https://scrumbackend.vercel.app/api/all_wfh_events`)
    const employeesResponse = await axios.get(`https://scrumbackend.vercel.app/api/all_employees`)

    const deptColors = {
      "HR": "blue",
      "Engineering": "green",
      "Marketing": "red",
      "Sales": "orange",
      "Finance": "purple",
      "default": "gray"
    }

    events.value = eventsResponse.data.map(event => ({
      title: `${event.fname} ${event.lname}`,
      start: new Date(event.wfh_date),
      end: new Date(event.wfh_date),
      dept: event.dept,
      empId: event.empId,
      color: deptColors[event.dept] || deptColors["default"],
      allDay: true
    }))

    employees.value = employeesResponse.data.map(employee => ({
      id: employee.id,
      name: `${employee.fname} ${employee.lname}`,
      dept: employee.dept
      
    }
  ))
  
  calendarReady.value = true; // Set calendar ready after data is successfully fetched

  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const filteredEvents = computed(() => {
  if (selectedDept.value === 'All') {
    return events.value
  } else {
    return events.value.filter(event => event.dept === selectedDept.value)
  }
})

// Filter employees based on the selected department and search query
const filteredEmployees = computed(() => {
  return employees.value.filter(employee => {
    const isDeptMatch = selectedDept.value === 'All' || employee.dept === selectedDept.value;
    const isSearchMatch = employee.name.toLowerCase().includes(searchQuery.value.toLowerCase());
    return isDeptMatch && isSearchMatch;
  });
});

function isOnWFH(employee, day) {
  return events.value.some(event => event.empId === employee.id && event.start.toDateString() === day.toDateString())
}

function formatDate(date) {
  return format(date, 'MMM dd')
}

onMounted(() => {
  fetchOverallEvents()
})
</script>

<style scoped>
#loading {
  margin-top: 40vh;
}

@media (max-width: 1200px) {
  #dashboard, #calendar{
    margin-top: 100px;
  }

}
</style>
