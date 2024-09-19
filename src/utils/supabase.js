import { createClient } from "@supabase/supabase-js";

console.log(process.env);
console.log("Supabase URL:", process.env.VUE_APP_SUPABASE_URL);
console.log("Supabase Key:", process.env.VUE_APP_SUPABASE_KEY);

const supabaseUrl = process.env.VUE_APP_SUPABASE_URL;
const supabaseKey = process.env.VUE_APP_SUPABASE_KEY;

export const supabase = createClient(supabaseUrl, supabaseKey);
        