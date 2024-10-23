<template>
  <div class="about">
    <v-row class="fill-height">
      <v-col>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <v-toolbar-title>Team Dashboard</v-toolbar-title>
          <div style="display: flex;">
            <v-select v-if="teamMembers.length > 0" v-model="selectedTeamMember" :items="teamMembers" class="mt-4 w-50" label="Team Member"
              variant="outlined" outlined dense style="max-width: 200px"></v-select>

            <v-select v-model="viewType" :items="viewTypes" label="Select View Type" outlined variant="outlined" dense
              class="mt-4 w-50" style="max-width: 200px; margin-left: 16px;"></v-select>

            <v-select v-model="viewMode" :items="viewModes" label="Select View Mode" outlined variant="outlined" dense
              class="mt-4 w-50" style="max-width: 200px; margin-left: 16px;"></v-select>
          </div>
        </div>

        <v-sheet height="600" class="mt-4">
          <template v-if="viewType === 'Calendar'">
            <v-calendar ref="calendar" v-model="today" :events="filteredEvents" color="primary"
              :type="viewMode" v-if="calendarReady"></v-calendar>
          </template>
          <template v-else>
            <div style="display: flex; flex-direction: column; align-items: center;">
              <v-simple-table class="elevation-1">
                <thead>
                  <tr style="border-bottom: 2px solid #000; background-color: #f5f5f5;">
                    <th style="padding: 8px;">Team Member</th>
                    <th style="padding: 8px;">Location</th>
                    <th style="padding: 8px;">Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="event in filteredEvents" :key="event.empId">
                    <td style="padding: 8px;">{{ event.title }}</td>
                    <td :style="{ color: event.location === 'WFH' ? 'blue' : 'green' }">{{ event.location }}</td>
                    <td style="padding: 8px;">{{ event.start.toLocaleDateString() }}</td>
                  </tr>
                </tbody>
              </v-simple-table>
            </div>
          </template>
        </v-sheet>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

export default {
  name: 'TeamSchedule',
  setup() {
    const today = ref(new Date());
    const events = ref([]);
    const teamMembers = ref([]);
    const selectedTeamMember = ref('All');
    const viewType = ref('Calendar');
    const viewTypes = ref(['Calendar', 'Dashboard']);
    const viewMode = ref('Month');
    const viewModes = ref(['Day', 'Week', 'Month']);
    const calendarReady = ref(false);

    // Function to format event title with location indicator
    function formatEventTitle(event) {
      const location = event.location === 'WFH' ? '(WFH)' : '(Office)';
      return `${event.title} ${location}`;
    }

    // Filter events based on selected team member
    const filteredEvents = computed(() => {
      return events.value
        .map(event => ({
          ...event,
          title: formatEventTitle(event),
          color: event.location === 'WFH' ? 'blue' : 'green', // Highlight location
        }))
        .filter(event =>
          selectedTeamMember.value === 'All' || event.empId === selectedTeamMember.value
        );
    });

    // Watch for changes in selectedTeamMember to fetch specific events
    watch(selectedTeamMember, async (newVal) => {
      if (newVal) {
        await fetchStaffEvents(newVal);
      }
    });

    // Fetch WFH events from backend for a specific manager and team member
    async function fetchStaffEvents(teamMemberID) {
      try {
        if (teamMemberID === 'All') {
          await fetchOverallEvents();
        } else {
          const response = await axios.get(
            `https://scrum-backend.vercel.app/api/wfh_events/${teamMemberID}`
          );
          if (response.data) {
            events.value = response.data.map(event => ({
              title: `${event.fname} ${event.lname}`,
              start: new Date(event.wfh_date),
              end: new Date(event.wfh_date),
              color: event.location === 'WFH' ? 'blue' : 'green',
              allDay: true,
              location: event.location,
              empId: event.empId,
            }));
          }
        }
      } catch (error) {
        console.error(
          'Error fetching WFH events:',
          error.response ? error.response.data : error.message
        );
      }
    }

    // Fetch all events
    async function fetchOverallEvents() {
      try {
        const response = await axios.get(
          `https://scrum-backend.vercel.app/api/all_wfh_events`
        );
        if (response.data) {
          events.value = response.data.map(event => ({
            title: `${event.fname} ${event.lname}`,
            start: new Date(event.wfh_date),
            end: new Date(event.wfh_date),
            color: event.location === 'WFH' ? 'blue' : 'green',
            allDay: true,
            location: event.location,
            empId: event.empId,
          }));
          calendarReady.value = true; // Calendar is now ready to be rendered
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }

    // Fetch team members with improved error handling
    async function fetchTeamMembers() {
      try {
        const response = await axios.get(
          `https://scrum-backend.vercel.app/api/all_employees`
        );
        if (response.data && Array.isArray(response.data)) {
          teamMembers.value = response.data.map(member => ({
            id: member.id,
            name: `${member.fname} ${member.lname}`,
          }));
        } else {
          console.error('Unexpected response structure:', response.data);
        }
      } catch (error) {
        console.error(
          'Error fetching team members:',
          error.response ? error.response.data : error.message
        );
        // Provide fallback data to avoid breaking the UI
        teamMembers.value = [
          { id: '1', name: 'John Doe' },
          { id: '2', name: 'Jane Smith' },
        ];
      }
    }

    // Lifecycle hook for component mount
    onMounted(async () => {
      try {
        await fetchTeamMembers();
        await fetchOverallEvents();
      } catch (e) {
        console.error('Error during component mount:', e.message);
      }
    });

    return {
      today,
      teamMembers,
      selectedTeamMember,
      viewType,
      viewTypes,
      viewMode,
      viewModes,
      filteredEvents,
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
</style>
