<template>
  <v-app>
    <v-main>
      <v-container fluid style="padding: 0px;">
        <v-col class="light-blue">
          <!-- Overview Cards -->
          <v-row style="padding: 0%;">
            <v-col :cols="isUserValid ? 8 : 12" :class="{ 'text-center': !isUserValid }">
              <v-card class="white pa-4">
                <v-card-title class="text-blue responsive-title" style="font-size: 100px;">
                  Welcome, <br/> {{ fname }} {{ lname }}
                </v-card-title>
                <v-card-subtitle class="text-blue" style="font-size: 30px;">
                  Today's date is {{ formattedDate }}
                </v-card-subtitle>
                <v-card-subtitle class="text-blue quote">
                  "{{ dailyQuote }}"
                </v-card-subtitle>
              </v-card>
            </v-col>
            <!-- Conditionally render based on userId -->
            <v-col :cols="isUserValid ? 4 : 12" :md="4" style="padding-top: 0%;">
              <v-card class="white pa-4" v-if="isUserValid">
                <!-- Using WFHrequestForm component here -->
                <WFHrequestForm />
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import useUser from '../utils/useUser';
import WFHrequestForm from './WFHrequestForm.vue'; // Correct import statement

export default defineComponent({
  name: 'HomeView',

  components: {
    WFHrequestForm, // Register the component
  },

  setup() {
    const { fname, lname, id } = useUser();
    const isUserValid = ref(false);
    const formattedDate = ref('');
    const dailyQuote = ref('');

    const quotes = [
      "The only way to do great work is to love what you do. – Steve Jobs",
      "Success is not the key to happiness. Happiness is the key to success. – Albert Schweitzer",
      "Don’t watch the clock; do what it does. Keep going. – Sam Levenson",
      "You are never too old to set another goal or to dream a new dream. – C.S. Lewis",
      "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
      "It does not matter how slowly you go as long as you do not stop. – Confucius",
      "Everything you can imagine is real. – Pablo Picasso",
      "The best way to predict the future is to create it. – Peter Drucker",
    ];

    onMounted(() => {
      // Check userId when component is mounted
      isUserValid.value = id.value !== '130002';

      // Format today's date
      const today = new Date();
      formattedDate.value = today.toLocaleDateString(); // You can customize the format if needed

      // Get a daily quote based on the current date
      const todayString = today.toDateString();
      const hash = Array.from(todayString).reduce((acc, char) => acc + char.charCodeAt(0), 0);
      dailyQuote.value = quotes[hash % quotes.length];
    });

    return {
      fname,
      lname,
      isUserValid,
      formattedDate,
      dailyQuote,
    };
  },
});
</script>

<style scoped>
.text-blue {
  text-wrap: nowrap;
  text-overflow: unset;
}

.quote {
  margin-top: 160px;
  font-size: 20px;
}

.responsive-title {
  font-size: calc(100px - 1vw); 
  white-space: normal;          
  word-break: break-word;       
  overflow-wrap: break-word;    
}
</style>
