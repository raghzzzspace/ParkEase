<template>
  <nav class="navbar navbar-expand-lg shadow mb-4" style="background: linear-gradient(to bottom, #0066cc, #004aad);">
    <div class="container-fluid">
      <a class="navbar-brand ms-3" href="#" style="color: #ffffff;">Welcome to Customer</a>
      <div class="collapse navbar-collapse justify-content ms-5">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/customer_dashboard" style="color: #ffffff;">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/customer_summary" style="color: #ffffff;">Summary</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/customer_export" style="color: #ffffff;">Get Details</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/logout" style="color: #ffffff;">Logout</router-link>
          </li>
        </ul>
        <router-link to="/customer_profile" class="btn btn-light ms-auto" style="color: #004aad;" @click="getCustomerProfile">
          Edit Profile
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
import instance from "@/axios.js";

export default {
  name: 'CustomerNavbar',
  data() {
    return {
      customerEmail: ''
    };
  },
  mounted() {
    // Retrieve the customer email from localStorage
    const email = localStorage.getItem('customer_email');
    if (email) {
      this.customerEmail = email; // Set the customer email
    } else {
      console.log('Customer email not found in localStorage');
    }
  },
  methods: {
    getCustomerProfile() {
      if (!this.customerEmail) {
        console.log('Customer email is not available');
        return;
      }

      // Make the Axios request to get the customer profile using the email
      instance.get(`customer/profile?customer_email=${this.customerEmail}`)
        .then(response => {
          console.log('Customer Profile:', response.data);
        })
        .catch(error => {
          console.error('There was an error fetching the customer profile:', error);
        });
    }
  }
};
</script>

<style scoped>
.navbar-nav .nav-link {
  font-size: 16px;
  font-weight: bold;
}

.navbar-nav .nav-link:hover {
  color: #c1c1c1;
}

.btn-light {
  color: #004aad;
  border: 1px solid #004aad;
  border-radius: 5px;
}

.btn-light:hover {
  background-color: #004aad;
  color: white;
}
</style>
