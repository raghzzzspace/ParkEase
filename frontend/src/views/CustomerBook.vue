<template>
<!-- Navbar Component -->
    <CustomerNavbar />
  <div class="booking-container">
    
    <!-- Heading -->
    <h2 class="booking-title">Book the parking spot</h2>

    <!-- Booking Form -->
    <form @submit.prevent="submitBooking" class="booking-form">
      <!-- Pre-filled Fields -->
      <div class="form-group">
        <label for="spotId">Spot ID:</label>
        <input type="text" id="spotId" v-model="form.spotId" readonly />
      </div>

      <div class="form-group">
        <label for="lotId">Lot ID:</label>
        <input type="text" id="lotId" v-model="form.lotId" readonly />
      </div>

      <div class="form-group">
        <label for="userId">User:</label>
        <input type="text" id="userId" v-model="form.userId" readonly />
      </div>

      <!-- Editable Fields -->
      <div class="form-group">
        <label for="vehicleNumber">Vehicle Number:</label>
        <input
          type="text"
          id="vehicleNumber"
          v-model="form.vehicleNumber"
          placeholder="Enter your vehicle number"
          required
        />
      </div>

      <!-- Buttons -->
      <div class="button-group">
        <button type="submit" class="btn reserve">Reserve</button>
        <button type="button" class="btn cancel" @click="resetForm">Cancel</button>
      </div>
    </form>

    <!-- Footer Component -->
  </div>
  <AppFooter />
</template>

<script>
import CustomerNavbar from "@/components/CustomerNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";
import instance from '@/axios.js';

export default {
  name: 'CustomerBook',
  components: {
    CustomerNavbar,
    AppFooter
  },
  data() {
    return {
      form: {
        spotId: this.$route.query.spotId,
        lotId: this.$route.query.lotId,
        userId: this.$route.query.userId,
        vehicleNumber: ''
      }
    };
  },
  methods: {
    async submitBooking() {
  try {
    const response = await instance.post('/reserve', {
      spotId: this.form.spotId,
      userId: this.form.userId,
      vehicleNumber: this.form.vehicleNumber
    });
    alert("Parking spot booked successfully!");
    console.log(response.data);
    this.$router.push('/customer_dashboard');
  } catch (error) {
    console.error("Booking error:", error.response?.data || error.message);
    alert("Booking failed: " + (error.response?.data?.message || "Unknown error"));
  }
},
resetForm() {
  this.form.vehicleNumber = '';
  this.$router.push('/customer_dashboard');
}

  }
};
</script>

<style scoped>
.booking-container {
  max-width: 420px;
  margin: 3rem auto;
  padding: 2rem 2.5rem;
  background: #202c4a; /* same dark blue background as lot cards */
  border-radius: 20px; /* rounded like lot cards */
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
  border: 2px solid #3a5fcd; /* same border color as lot cards */
  color: #e0e6f0; /* light text color */
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  user-select: none;
}

.booking-title {
  background-color: #283655; /* close to your striped-bg darker shade */
  padding: 1rem 0;
  border-radius: 20px;
  text-align: center;
  font-size: 1.8rem;
  font-weight: 800;
  color: #64b5f6;
  margin-bottom: 2rem;
  box-shadow: 0 4px 10px rgba(58, 95, 205, 0.6);
}

.booking-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.4rem;
}

label {
  flex: 1;
  font-weight: 700;
  color: #64b5f6;
  font-size: 1.1rem;
}

input {
  flex: 2;
  padding: 0.5rem 0.75rem;
  border: 2px solid #3a5fcd;
  border-radius: 12px;
  font-size: 1rem;
  color: #202c4a; /* dark text for inputs */
  background-color: #e0e6f0; /* light input background */
  transition: border-color 0.3s ease;
  user-select: text;
}

input:focus {
  outline: none;
  border-color: #64b5f6;
  box-shadow: 0 0 8px #64b5f6;
}

input[readonly] {
  background-color: #283655;
  color: #9bb9e8;
  font-style: italic;
  user-select: none;
  border-color: #283655;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.65rem 2.4rem;
  font-weight: 700;
  font-size: 1.1rem;
  border-radius: 30px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  user-select: none;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.reserve {
  background-color: #3a5fcd;
  color: #e0e6f0;
  border-color: #64b5f6;
}

.reserve:hover {
  background-color: #64b5f6;
  color: #202c4a;
  border-color: #3a5fcd;
  box-shadow: 0 0 15px #64b5f6;
}

.cancel {
  background-color: transparent;
  color: #ef5350; /* red for cancel to differentiate */
  border: 2px solid #ef5350;
}

.cancel:hover {
  background-color: #ef5350;
  color: #fff;
  box-shadow: 0 0 15px #ef5350;
}


</style>
