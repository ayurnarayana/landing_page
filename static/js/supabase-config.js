// supabase-config.js
// Supabase Configuration for Ayur Narayana

// Replace these with your actual Supabase project credentials
// You can find these in your Supabase project settings
const SUPABASE_URL = 'https://gcgagxgapkeigwbwvnpx.supabase.co'; // e.g., 'https://your-project.supabase.co'
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjZ2FneGdhcGtlaWd3Ynd2bnB4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0MTg2MTQsImV4cCI6MjA5MTk5NDYxNH0.VZ4KnkLElyxN9kAIRghxiAexfi0HpQbEpbd64Imt9gk'; // Your public anon key

// Initialize Supabase client
const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Export for use in other files
window.supabaseClient = supabaseClient;

console.log('Supabase client initialized');
