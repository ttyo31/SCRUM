import { ref } from 'vue';
import { supabase } from '../utils/supabase';

// Create reactive variables for user data
const fname = ref('');
const lname = ref('');
const id = ref(null);
const mail = ref('');
const mgr_id = ref(null);
const dept = ref('');
const role = ref(null);

// Function to fetch user data
const fetchStaffDetails = async (email) => {
  const { data, error } = await supabase
    .from('staff')
    .select('*')
    .eq('mail', email);


  if (data && data.length > 0) {
    // Populate reactive variables with user data
    id.value = data[0].id;
    fname.value = data[0].fname;
    lname.value = data[0].lname;
    mail.value = data[0].mail;
    mgr_id.value = data[0].mgr_id;
    dept.value = data[0].dept;
    role.value = data[0].role;

    console.log('Staff details:', data[0]);
  } else if (error) {
    console.error('Error fetching staff details:', error);
  }
};

// Create a composable for user details
const useUser = () => {
  return {
    id,
    fname,
    lname,
    mail,
    mgr_id,
    dept,
    role,
    fetchStaffDetails
  };
};

export default useUser;
