<template>
  <div class="about">
    <v-row class="fill-height">
      <v-col>
        <div style="padding:10px; position: absolute; display: flex; justify-content: flex-end; align-items: center; width: 100%;">
          <v-select class="mt-4 me-2 w-50" v-model="viewType" :items="viewTypes" label="Select View Mode" outlined variant="outlined"
            dense style="max-width: 200px"></v-select>
        </div>

        <v-sheet height="600" class="mt-4">
          <div id="loading" v-if="!calendarReady" class="d-flex justify-center align-center">
            <v-progress-circular indeterminate color="primary" size="70"></v-progress-circular>
          </div>

          <template v-else>
            <template v-if="viewType === 'Calendar'">
              <v-calendar id="calendar" ref="calendar" v-model="today" :events="events" color="primary"
                type="month" style="padding: 10px; padding-top: 20px;"></v-calendar>
            </template>
            <template v-else>
              <div id="dashboard" style="display: flex; flex-direction: column; align-items: center;">
                <v-text-field v-model="searchQuery" label="Search Team Member" class="mt-4 w-50" outlined dense
                  style="max-width: 300px" />
                <v-simple-table class="elevation-1">
                  <thead>
                    <tr style="border-bottom: 2px solid #000; background-color: #f5f5f5;">
                      <th style="padding: 8px;">Employee Name</th>
                      <th v-for="day in next7Days" :key="day" style="padding: 8px; border-right: 1px solid #ddd;">
                        {{ formatDate(day) }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="employee in filteredEmployees" :key="employee.id" style="border: 1px solid #ddd;">
                      <td style="padding: 8px; border-right: 1px solid #ddd;">{{ employee.name }}</td>
                      <td v-for="day in next7Days" :key="day"
                        style="padding: 8px; border-right: 1px solid #ddd; text-align: center;">
                        <template v-if="day.getDay() === 0 || day.getDay() === 6">
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

<script>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { format } from 'date-fns';
import useUser from '../utils/useUser';

export default {
  name: 'TeamSchedule',
  setup() {
    const today = ref(new Date());
    const events = ref([]);
    const employees = ref([]);
    const viewType = ref('Calendar');
    const viewTypes = ref(['Calendar', 'Dashboard']);
    const searchQuery = ref('');
    const calendarReady = ref(false);
    const { dept } = useUser();

    const next7Days = computed(() => {
      const days = [];
      const startOfWeek = new Date(today.value);
      const dayOfWeek = startOfWeek.getDay();
      startOfWeek.setDate(startOfWeek.getDate() - dayOfWeek + 1);

      for (let i = 0; i < 7; i++) {
        const date = new Date(startOfWeek);
        date.setDate(startOfWeek.getDate() + i);
        days.push(date);
      }
      return days;
    });

    async function fetchTeamEvents() {
      try {
        const eventsResponse = await axios.get(`https://scrum-backend.vercel.app/api/all_wfh_events`);
        const employeesResponse = await axios.get(`https://scrum-backend.vercel.app/api/all_employees`);

        events.value = eventsResponse.data
          .filter(event => event.dept === dept.value)
          .map(event => ({
            title: `${event.fname} ${event.lname}`,
            start: new Date(event.wfh_date),
            end: new Date(event.wfh_date),
            empId: event.empId,
            location: event.location,
            color: 'primary'
          }));

        employees.value = employeesResponse.data
          .filter(employee => employee.dept === dept.value)
          .map(employee => ({
            id: employee.id,
            name: `${employee.fname} ${employee.lname}`,
          }));

        calendarReady.value = true;
      } catch (error) {
        console.error('Error fetching data:', error);
        calendarReady.value = false;
      }
    }

    const filteredEmployees = computed(() => {
      return employees.value.filter(employee =>
        employee.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    function isOnWFH(employee, day) {
      return events.value.some(event => event.empId === employee.id && event.start.toDateString() === day.toDateString());
    }

    function formatDate(date) {
      return format(date, 'MMM dd');
    }

    onMounted(() => {
      fetchTeamEvents();
    });

    return {
      today,
      events,
      viewType,
      viewTypes,
      searchQuery,
      next7Days,
      filteredEmployees,
      isOnWFH,
      formatDate,
      calendarReady,
    };
  },
};
</script>

<style scoped>
.centering {
  display: flex;
  justify-content: center;
  align-items: center;
}

.black-button {
  background-color: white;
  color: black;
  border: solid 1px black;
}

.black-button:hover {
  background-color: black;
  color: white;
}

#loading {
  margin-top: 40vh;
}

@media (max-width: 1200px) {
  #dashboard, #calendar {
    margin-top: 100px;
  }
}
</style>
