
  <template>
  <!-- Ensure router-view is present to render pages -->
  <v-app>
    <v-main>
      <v-container fluid style="padding: 0px;">
      <v-col class="light-blue">
          <!-- Overview Cards -->
          <v-row style="padding: 0%;"> 
            <v-col cols="9">
              <v-card class="white pa-4">
                <v-card-title class="text-blue" style="font-size: 100px;">Welcome, XXX</v-card-title>
      
                <v-card-subtitle class="text-blue" style="font-size: 30px;">You are currently working from XXX</v-card-subtitle>
                <br>
                <v-card-subtitle class="text-blue" style="font-size: 30px;">Number of Team Members in Office: xxxx</v-card-subtitle>
                <br>
                <v-card-subtitle class="text-blue" style="font-size: 30px;">Number of Team Members at Home: XXX</v-card-subtitle>
                <br>
                <v-card-subtitle class="text-blue" style="font-size: 30px;">You have xxx WFH days this week</v-card-subtitle>
                <br>
                <v-card-subtitle class="text-blue" style="font-size: 30px;">Upcoming WFH dates:</v-card-subtitle>
              </v-card>
            </v-col>
            <v-col cols="3" style="padding-top: 0%;">
              <v-card class="white pa-4">
                <v-card-title class="text-blue" style="font-size: 20px; padding-bottom: 0%;">Apply for Flexible working</v-card-title>
                <v-date-picker>
                </v-date-picker>
                <button>Submit</button>
              </v-card>
            </v-col>
          </v-row>
          <!-- Graphs and Charts -->
          <!-- <v-row>
            <v-col cols="12">
              <v-card class="white pa-4">
                <v-card-title class="text-blue">UpComing Flexible Working Dates</v-card-title>
                
              </v-card>
            </v-col>
          </v-row> -->
        </v-col>
      </v-container>
    </v-main>
  </v-app>
</template>


<script>
import { defineComponent } from 'vue';

// Components

export default defineComponent({
  name: 'HomeView',

  components: {
  },
});
</script>
