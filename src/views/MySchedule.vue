<template>
  <div style="padding: 10px">
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
import { ref, onMounted } from 'vue';
import { supabase } from '../utils/supabase';
import useUser from '../utils/useUser';

// Access user details from the composable
const { id: userId } = useUser();

const calendar = ref();
const today = ref([new Date()]);
const events = ref([]);

// Function to fetch events for the logged-in user
async function fetchUserEvents() {
  try {
    const { data, error } = await supabase
      .from('staff_wfh')
      .select('wfh_date')
      .eq('staff_id', userId.value); // Use staff_id to match the logged-in user

    if (error) {
      console.error('Error fetching events:', error);
      return;
    }

    // Map the fetched data into the format expected by the calendar
    events.value = data.map(event => ({
      title: 'WFH',
      start: new Date(event.wfh_date),
      end: new Date(event.wfh_date),
      color: 'blue',
      allDay: true,
    }));

    console.log('Fetched events:', events.value);
  } catch (error) {
    console.error('Unexpected error fetching events:', error);
  }
}

onMounted(() => {
  fetchUserEvents();
});
</script>