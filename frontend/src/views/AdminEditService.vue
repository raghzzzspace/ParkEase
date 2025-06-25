<template>
  <div>
    <!-- Admin Navbar -->
    <AdminNavbar />

    <!-- Edit Parking Lot Section -->
    <div class="container-fluid mb-5">
      <h3 class="text-center mb-4">Edit Parking Lot</h3>

      <!-- Edit Parking Lot Form -->
      <form @submit.prevent="submitForm" class="parking-form">
        <div class="mb-3">
          <label for="location_name" class="form-label">Prime Location Name</label>
          <input
            type="text"
            class="form-control"
            id="location_name"
            v-model="parking.prime_location_name"
            required
          />
        </div>

        <div class="mb-3">
          <label for="address" class="form-label">Address</label>
          <textarea
            class="form-control"
            id="address"
            v-model="parking.address"
            rows="3"
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
            min="1"
          />
        </div>

        <!-- Submit and Cancel Buttons -->
        <div class="d-flex justify-content-between">
          <button type="submit" class="btn btn-primary btn-lg">Update</button>
          <button
            type="button"
            class="btn btn-secondary btn-lg"
            @click="$router.push('/admin_dashboard')"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>

    <!-- App Footer -->
    <AppFooter />
  </div>
</template>

<script>
import AdminNavbar from "@/components/AdminNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";
import instance from '@/axios';

export default {
  components: {
    AdminNavbar,
    AppFooter,
  },
  data() {
    return {
      parking: {
        parking_lot_id: null,
        prime_location_name: '',
        address: '',
        pincode: '',
        price: 0,
        number_of_spots: 0,
      },
      loading: true,
    };
  },
  methods: {
    async submitForm() {
  try {
    const response = await instance.put(`/update_parking_lot/${this.parking.parking_lot_id}`, this.parking);
    alert(response.data.message || "Parking lot updated successfully!");
    this.$router.push("/admin_dashboard");
  } catch (error) {
    console.error("Error updating parking lot:", error.response?.data || error.message);
    alert("Failed to update parking lot.");
  }
}
  },
  
  created() {
    const id = this.$route.params.id;
    this.parking.parking_lot_id = id;

    // Call backend to get parking lot details
    instance.get(`/get_parking_lot/${id}`)
      .then(response => {
        this.parking = response.data;
        this.loading = false;
      })
      .catch(error => {
        console.error("Error fetching parking lot:", error.response?.data || error.message);
        alert("Failed to load parking lot data.");
        this.$router.push("/admin_dashboard");
      });
  }
};
</script>


<style scoped>
.container-fluid {
  max-width: 600px;
  background-color: rgb(5, 28, 65); /* dark blue */
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.7);
  color: #ffffff;
}

.text-center {
  font-weight: 600;
  color: #bbdefb; /* light blue */
}

.form-label {
  color: #cfd8dc; /* light gray */
  font-weight: 500;
}

.form-control {
  width: 100%;
  background-color: rgb(10, 40, 85);
  border: 1.5px solid #90caf9;
  color: #e3f2fd;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #42a5f5;
  background-color: rgb(15, 55, 110);
  color: #fff;
  box-shadow: 0 0 5px #42a5f5;
}

textarea.form-control {
  resize: vertical;
  color: #e3f2fd;
}

.btn-primary {
  background-color: #42a5f5;
  border-color: #42a5f5;
  color: #0d47a1;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #1e88e5;
  border-color: #1e88e5;
  color: #e3f2fd;
}

.btn-secondary {
  background-color: #f44336;
  border-color: #f44336;
  color: #fff;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.btn-secondary:hover {
  background-color: #d32f2f;
  border-color: #d32f2f;
}

.parking-form {
  color: #e3f2fd;
}
</style>
