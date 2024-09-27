import { ref } from 'vue';
import { supabase } from '../utils/supabase';

// Create reactive variables for user data
const fname = ref(localStorage.getItem('fname') || '');
const lname = ref(localStorage.getItem('lname') || '');
const id = ref(localStorage.getItem('id') || null);
const mail = ref(localStorage.getItem('mail') || '');
const mgr_id = ref(localStorage.getItem('mgr_id') || null);
const dept = ref(localStorage.getItem('dept') || '');
const role = ref(localStorage.getItem('role') || null);

// Function to fetch user data
const fetchStaffDetails = async (email) => {
  const { data, error } = await supabase
    .from('staff')
    .select('*')
    .eq('mail', email);

  if (data && data.length > 0) {
    const userData = data[0];

    // Store in reactive variables and localStorage
    id.value = userData.id;
    fname.value = userData.fname;
    lname.value = userData.lname;
    mail.value = userData.mail;
    mgr_id.value = userData.mgr_id;
    dept.value = userData.dept;
    role.value = userData.role;

    // Store in localStorage
    localStorage.setItem('id', userData.id);
    localStorage.setItem('fname', userData.fname);
    localStorage.setItem('lname', userData.lname);
    localStorage.setItem('mail', userData.mail);
    localStorage.setItem('mgr_id', userData.mgr_id);
    localStorage.setItem('dept', userData.dept);
    localStorage.setItem('role', userData.role);

    console.log('Staff details:', userData);
  } else if (error) {
    console.error('Error fetching staff details:', error);
  }
};

// Function to clear data from localStorage (e.g., during logout)
const clearUserData = () => {
  localStorage.removeItem('id');
  localStorage.removeItem('fname');
  localStorage.removeItem('lname');
  localStorage.removeItem('mail');
  localStorage.removeItem('mgr_id');
  localStorage.removeItem('dept');
  localStorage.removeItem('role');
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
    fetchStaffDetails,
    clearUserData
  };
};

export default useUser;
