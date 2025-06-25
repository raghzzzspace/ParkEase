import { createApp } from 'vue';
import App from './App.vue';


// Import the router
import router from './router';

// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';

// Import Bootstrap JavaScript (optional if you're using Bootstrap's JS components)
import 'bootstrap';

// Import Bootstrap Icons
import 'bootstrap-icons/font/bootstrap-icons.css';


// Create and mount the Vue app, with the router attached
createApp(App)
  .use(router)  // Attach the router to the app
  .mount('#app');
