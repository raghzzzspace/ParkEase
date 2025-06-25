<template>
  <div>
    <!-- Admin Navbar -->
    <AdminNavbar />

    <div class="container-fluid mb-5">
      <h3 class="text-center mb-4">View/Delete Parking Spot</h3>

      <!-- Parking Spot View Form -->
      <div class="mb-3">
        <label class="form-label fw-bold">ID:</label>
        <input type="text" class="form-control" v-model="spot.id" readonly />
      </div>

      <div class="mb-3">
        <label class="form-label fw-bold">Status:</label><br />
        <span 
          :class="[
            'badge px-3 py-2 fs-6',
            spot.status === 'O' ? 'bg-danger' : 'bg-success',
            'cursor-pointer'
          ]"
          @click="handleStatusClick"
        >
          {{ spot.status === 'O' ? 'Occupied' : 'Available' }}
        </span>
      </div>

      <!-- Show Occupied Info -->
      <div v-if="spot.status === 'O' && showOccupiedDetails" class="alert alert-info">
        <p><strong>Occupied By:</strong> {{ spot.occupiedBy }}</p>
        <p><strong>Start Time:</strong> {{ spot.startTime }}</p>
        <p><strong>Expected End:</strong> {{ spot.expectedEnd }}</p>
      </div>

      <!-- Occupied Note -->
      <div v-if="spot.status === 'O'" class="text-warning mb-3">
        <em>Note: You can't delete an occupied parking spot.</em>
      </div>

      <!-- Buttons -->
      <div class="d-flex justify-content-between">
        <button 
          class="btn btn-danger btn-lg" 
          :disabled="spot.status === 'O'" 
          @click="deleteSpot"
        >
          Delete
        </button>
        <button class="btn btn-secondary btn-lg" @click="$router.push('/admin_dashboard')">
          Close
        </button>
      </div>
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
  name: 'ViewDeletePs',
  components: {
    AdminNavbar,
    AppFooter
  },
  data() {
  return {
    spot: {},
    showOccupiedDetails: false,
    parkingLotId: this.$route.params.lotId,
    spotId: this.$route.params.spotId,
  };
},
mounted() {
  this.fetchSpot();
},
  

  methods: {
  handleStatusClick() {
    if (this.spot.status === 'O') {
      this.$router.push(`/occuspots/${this.parkingLotId}/${this.spot.id}`);
    }
  },

  async fetchSpot() {
    try {
      const res = await instance.get(`/get_spots/${this.parkingLotId}/${this.spotId}`);
      this.spot = res.data;
    } catch (err) {
      console.error("Failed to load spot", err);
      alert("Failed to load parking spot.");
    }
  },

  async deleteSpot() {
    try {
      await instance.delete(`/spots/${this.parkingLotId}/${this.spotId}`);
      alert("Spot deleted successfully!");
      this.$router.push('/admin_dashboard');
    } catch (err) {
      console.error("Deletion failed", err);
      alert("Failed to delete spot.");
    }
  },
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
  background-color: #051c41;
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
}

.form-control {
  background-color: #0a2855;
  color: #e3f2fd;
  border: 1px solid #2196f3;
}

.form-control:read-only {
  background-color: #102c4d;
}

.badge {
  user-select: none;
}

.bg-danger {
  background-color: #d32f2f !important;
}

.bg-success {
  background-color: #388e3c !important;
}

.alert-info {
  background-color: #1565c0;
  color: #e3f2fd;
  border: 1px solid #64b5f6;
}

.text-warning {
  color: #ffcc00 !important;
}

.btn-danger {
  background-color: #e53935;
  border-color: #e53935;
}

.btn-danger:disabled {
  background-color: #b71c1c;
  border-color: #b71c1c;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #546e7a;
  border-color: #546e7a;
}

.btn-secondary:hover {
  background-color: #37474f;
  border-color: #37474f;
}

.cursor-pointer {
  cursor: pointer;
}
</style>
