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

        <v-select
          v-model="viewMode"
          :items="viewModes"
          label="Select View Mode"
          outlined
          dense
          class="mt-4"
        ></v-select>

        <v-sheet height="600" class="mt-4">
          <template v-if="viewMode === 'Calendar'">
            <v-calendar
              ref="calendar"
              v-model="today"
              :events="filteredEvents"
              color="primary"
              type="month"
            ></v-calendar>
          </template>
          <template v-else>
            <!-- Dashboard view showing employees and their WFH status for the next 7 days -->
            <v-simple-table class="elevation-1">
              <thead>
                <tr style="border-bottom: 2px solid #000; background-color: #f5f5f5;">
                  <th style="padding: 8px; border-right: 1px solid #ddd;">Employee Name</th>
                  <th
                    v-for="day in next7Days"
                    :key="day"
                    style="padding: 8px; border-right: 1px solid #ddd;"
                  >
                    {{ formatDate(day) }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="employee in filteredEmployees"
                  :key="employee.id"
                  style="border: 1px solid #ddd;"
                >
                  <td style="padding: 8px; border-right: 1px solid #ddd;">
                    {{ employee.name }}
                  </td>
                  <td
                    v-for="day in next7Days"
                    :key="day"
                    style="padding: 8px; border-right: 1px solid #ddd; text-align: center;"
                  >
                    <span :style="{ color: 'red' }" v-if="isOnWFH(employee, day)">WFH</span>
                    <span :style="{ color: 'green' }" v-else>Office</span>
                  </td>
                </tr>
              </tbody>
            </v-simple-table>

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
const employees = ref([]) // New state to hold employees data
const selectedDept = ref('All')
const departments = ref(['All', 'HR', 'Engineering', 'Marketing', 'Sales', 'Finance'])
const viewMode = ref('Calendar')
const viewModes = ref(['Calendar', 'Dashboard'])

// Helper function to generate the next 7 days
const next7Days = computed(() => {
  const days = []
  for (let i = 0; i < 7; i++) {
    const date = new Date()
    date.setDate(date.getDate() + i)
    days.push(date)
  }
  return days
})

// Fetch employees and WFH events from the backend
async function fetchOverallEvents() {
  try {

    const eventsResponse = await axios.get(`https://scrum-backend.vercel.app/api/all_wfh_events`)
    const employeesResponse = await axios.get(`https://scrum-backend.vercel.app/api/all_employees`)


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
    }))
  } catch (error) {
    console.error('Error fetching data:', error)
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

// Filter employees based on the selected department
const filteredEmployees = computed(() => {
  if (selectedDept.value === 'All') {
    return employees.value
  } else {
    return employees.value.filter(employee => employee.dept === selectedDept.value)
  }
})

// Helper function to check if an employee is on WFH for a given day
function isOnWFH(employee, day) {
  return events.value.some(event => event.empId === employee.id && event.start.toDateString() === day.toDateString())
}

// Helper function to format date
function formatDate(date) {
  return format(date, 'MMM dd')
}

// On component mount, fetch the events and employees
onMounted(() => {
  fetchOverallEvents()
})
</script>
