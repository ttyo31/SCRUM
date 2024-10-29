<template>
  <v-app>
    <v-main>
      <v-container fluid style="padding: 0px;">
        <v-col class="light-blue">
          <!-- Overview Cards -->
          <v-row style="padding: 0%;">
            <v-col :cols="12">
              <v-card class="white pa-4 text-center">
                <v-card-title class="text-blue responsive-title" style="font-size: 100px;">
                  Welcome, <br /> {{ fname }} {{ lname }}
                </v-card-title>
                <v-card-subtitle class="text-blue" style="font-size: 30px;">
                  Today's date is {{ formattedDate }}
                </v-card-subtitle>
                <div class="go-somewhere__grid p-5 pb-0 mt-5">
                  <div class="go-somewhere__item" @click="this.$router.push('/myschedule')">
                    <i class="fi fi-rr-clock-time-tracking"></i>
                                        Own Schedule
                  </div>
                  <div class="go-somewhere__item" @click="this.$router.push('/TeamSchedule')">
                    <i class="fi fi-rs-employees"></i>
                    Team Schedule
                  </div>
                  <div vv-if="role == '1' || role == '3'" class="go-somewhere__item" @click="this.$router.push('/OverallSchedule')">
                    <i class="fi fi-rr-corporate"></i>
                    Overall Schedule
                  </div>
                  <div v-if="id !== '130002'" class="go-somewhere__item" @click="this.$router.push('/WFHrequestForm')">
                    <i class="fi fi-rr-edit"></i>
                    WFH Request
                  </div>
                </div>
                <v-card-subtitle class="text-blue quote">
                  "{{ dailyQuote }}"
                </v-card-subtitle>
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
import '../../node_modules/@flaticon/flaticon-uicons/css/regular/all.css';

export default defineComponent({
  name: 'HomeView',

  setup() {
    const { fname, lname, id, role } = useUser(); // Define id here
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
      const today = new Date();
      formattedDate.value = today.toLocaleDateString(); // Format date

      // Generate daily quote
      const todayString = today.toDateString();
      const hash = Array.from(todayString).reduce((acc, char) => acc + char.charCodeAt(0), 0);
      dailyQuote.value = quotes[hash % quotes.length];
    });

    return {
      fname,
      lname,
      id, // Return id for use in template
      role,
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

.go-somewhere__grid {
  display: flex;
  justify-content: center;
  padding-bottom: 0px;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
}

.go-somewhere__item {
  background-color: rgb(33, 150, 243);
  width: 200px;
  border-radius: 50px;
  padding: 30px;
  margin: 10px;
  margin-top: 35px;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s ease;
}

.go-somewhere__item i {
  font-size: 80px;
  color: #313131;
}

.go-somewhere__item:hover {
  transform: scale(1.05);
}

.go-somewhere__icon img {
  width: 40px;
  height: 40px;
  margin-bottom: 0.5rem;
}

.go-somewhere__text p {
  font-size: 1rem;
  color: #bbb;
  text-transform: capitalize;
}

.go-somewhere {
  text-align: center;
  padding: 2rem;
  padding-top: 100px;
  color: #fff;
}
</style>
