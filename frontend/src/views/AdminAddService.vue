<template>
  <div>
    <!-- Admin Navbar -->
    <AdminNavbar />

    <!-- Add New Parking Lot Section -->
    <div class="container-fluid mb-5">
      <h3 class="text-center mb-4">New Parking Lot</h3>

      <!-- Parking Lot Add Form -->
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="location_name" class="form-label">Prime Location Name</label>
          <input 
            type="text" 
            class="form-control" 
            id="location_name" 
            v-model="parking.prime_location_name" 
            required 
            placeholder="Enter location name" 
          />
        </div>

        <div class="mb-3">
          <label for="address" class="form-label">Address</label>
          <textarea 
            class="form-control" 
            id="address" 
            v-model="parking.address" 
            rows="3" 
            placeholder="Enter full address"
          ></textarea>
        </div>

        <div class="mb-3">
          <label for="pin_code" class="form-label">Pin Code</label>
          <input 
            type="text" 
            class="form-control" 
            id="pin_code" 
            v-model="parking.pincode" 
            required 
            placeholder="Enter pin code" 
          />
        </div>

        <div class="mb-3">
          <label for="price_per_hour" class="form-label">Price (per hour)</label>
          <input 
            type="number" 
            class="form-control" 
            id="price_per_hour" 
            v-model="parking.price" 
            required 
            placeholder="Enter hourly rate" 
            min="0" 
          />
        </div>

        <div class="mb-3">
          <label for="max_spots" class="form-label">Maximum Spots</label>
          <input 
            type="number" 
            class="form-control" 
            id="max_spots" 
            v-model="parking.number_of_spots" 
            required 
            placeholder="Enter total spots" 
            min="1" 
          />
        </div>

        <!-- Submit and Cancel Buttons -->
        <div class="d-flex justify-content-between">
          <button type="submit" class="btn btn-primary btn-lg">Add</button>
          <button type="button" class="btn btn-secondary btn-lg" @click="$router.push('/admin_dashboard')">Cancel</button>
        </div>
      </form>
    </div>

    <!-- App Footer -->
    <AppFooter />
  </div>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue';
import AppFooter from '@/components/AppFooter.vue';
import instance from '@/axios.js';

export default {
  name: 'AddParkingLot',
  components: {
    AdminNavbar,
    AppFooter
  },
  data() {
    return {
      parking: {
    prime_location_name: '',
    address: '',
    pincode: '',
    price: 0,
    number_of_spots: 0
      }
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await instance.post('/add_parking_lot', this.parking);
        console.log('Parking Lot Added:', response.data);
        alert('Parking lot added successfully!');
        this.$router.push('/admin_dashboard');
        this.resetForm();
      } catch (error) {
        console.error('Error adding parking lot:', error.response?.data || error.message);
        alert('Failed to add parking lot. Please try again.');
      }
    },
    resetForm() {
      this.parking = {
        location_name: '',
        address: '',
        pin_code: '',
        price_per_hour: 0,
        max_spots: 0
      };
    }
  }
};
</script>

<style scoped>
body {
  background-color: #0d1b2a;
  color: #ffffff;
}

.container-fluid {
  max-width: 600px;
  padding: 2rem;
  background-color: #051c41; /* Dark blue */
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.7);
  color: #ffffff;
}

.text-center {
  font-weight: bold;
  color: #bbdefb;
}

.form-label {
  color: #e0e0e0;
  font-weight: 500;
}

.form-control {
  background-color: #0a2855;
  color: #e3f2fd;
  border: 1px solid #2196f3;
}

.form-control::placeholder {
  color: #90caf9;
  opacity: 0.7;
}

.form-control:focus {
  background-color: #0a2855;
  color: #ffffff;
  border-color: #64b5f6;
  box-shadow: 0 0 5px rgba(100, 181, 246, 0.8);
}

.btn-primary {
  background-color: #1976d2;
  border-color: #1976d2;
}

.btn-primary:hover {
  background-color: #1565c0;
  border-color: #1565c0;
}

.btn-secondary {
  background-color: #ef5350;
  border-color: #ef5350;
}

.btn-secondary:hover {
  background-color: #d32f2f;
  border-color: #d32f2f;
}
</style>
