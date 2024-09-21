<template>
  <!-- old nav bar code
    <v-card>
    <v-tabs
      v-model="tab"
      bg-color="primary"
    >
    <router-link to="/"><v-tab value="one" class="text-white">Home</v-tab></router-link>
      <router-link to="/about"><v-tab value="one" class="text-white">calendar</v-tab></router-link>
      <v-tab value="three">Item Three</v-tab>
      <router-link to="/test"><v-tab value="one" class="text-white">Submission Test</v-tab> </router-link>
    </v-tabs>
  </v-card> -->
  <v-app>
    <v-main>
      <Navbar />
      <router-view/>
      <!-- this is a sample use case for the supabase retrieval of data -->
      <!-- <ul>
        <li v-for="manager in managers" :key="manager.id">
          {{ manager.fname }} 
        </li>
      </ul> -->
      
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
}
</script>


<script setup>
  import { ref, onMounted } from 'vue';
  import { supabase } from './utils/supabase'
  import Navbar from './components/NavBar.vue'
  const employees = ref([]);
  const managers = ref([]);

async function getEmployees() {
  const { data, error } = await supabase.from('employee').select(); // Query the Employee table
  if (error) {
    console.error('Error fetching employees:', error.message);
  } else {
    employees.value = data;
  }
}

async function getManagers() {
  const { data, error } = await supabase.from('manager').select(); 
  if (error) {
    console.error('Error fetching manager:', error.message);
  } else {
    managers.value = data;
  }
}

onMounted(() => {
  getEmployees(); // Fetch employees when the component is mounted
  getManagers();
});
</script>
<!-- 
<template>
<ul>
  <li v-for="employee in employees" :key="employee.Staff_ID">
    {{ employee.Staff_FName }} {{ employee.Staff_LName }} - {{ employee.Position }} ({{ employee.Dept }})
  </li>
</ul>
</template> -->