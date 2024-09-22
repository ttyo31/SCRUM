import { ref } from 'vue';
import { supabase } from '../utils/supabase';

// Create reactive variables for user data
const fname = ref('');
const lname = ref('');

// Function to fetch user data
const fetchStaffDetails = async (email) => {
  const { data, error } = await supabase
    .from('staff')
    .select('*')
    .eq('mail', email);

  if (data && data.length > 0) {
    fname.value = data[0].fname;
    lname.value = data[0].lname;
    console.log('Staff details:', data[0]);
  } else if (error) {
    console.error('Error fetching staff details:', error);
  }
};

const useUser = () => {
  return {
    fname,
    lname,
    fetchStaffDetails
  };
};

export default useUser;
