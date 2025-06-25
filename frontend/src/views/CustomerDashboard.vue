<template>
  <div>
    <!-- Customer Navbar -->
    <CustomerNavbar />

    <div class="container-fluid mt-4 mb-5">
      <h4 class="section-title">Recent Parking History</h4>
      <table class="table table-bordered table-striped shadow table-dark table-hover">
        <thead>
          <tr>
            <th>Parking Lot ID</th>
            <th>Parking Spot ID</th>
            <th>Parking Lot Address</th>
            <th>Vehicle Number</th>
            <th>Parking Timestamp</th>
            <th>Leaving Timestamp</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in parkingHistory" :key="entry.id">
            <td>{{ entry.parking_lot_id }}</td>
            <td>{{ entry.parking_spot_id }}</td>
            <td>{{ entry.address }}</td>
            <td>{{ entry.vehicle_number}}</td>
            <td>{{ entry.parking_timestamp }}</td>
            <td>{{ entry.leaving_timestamp || 'Still Parked' }}</td>

            <td>
              <button
                v-if="entry.status === 'O'"
                class="btn btn-danger btn-sm"
                @click="releaseParking(entry)"
              >
                Release
              </button>
              <span v-else class="badge bg-success">Parked Out</span>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="text-center my-4">
        <label for="locationSearch" class="form-label fs-5">Search parking @location/pin code:</label>
        <input
          type="text"
          id="locationSearch"
          class="form-control w-50 mx-auto"
          v-model="searchLocation"
          placeholder="e.g. Dadar Road"
          @keyup.enter="searchParkingLots"
        />
      </div>

      <div v-if="parkingLots.length > 0">
        <h4 class="section-title">Parking Lots @ {{ searchLocation }}</h4>
        <table class="table table-dark table-hover shadow rounded">
          <thead>
            <tr>
              <th>Parking Lot ID</th>
              <th>Parking Spot ID</th>
              <th>Address</th>
              <th>Availability</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in parkingLots" :key="lot.id">
              <td>{{ lot.parking_lot_id }}</td>
              <td>{{ lot.parking_spot_id }}</td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.availability }}</td>
              <td>
              <button
                v-if="lot.availability === 'A'"
                class="btn btn-primary btn-sm"
                @click="bookParking(lot)"
              >
                Book
              </button>

              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="text-center text-muted">
        <p>No parking lots found. Try searching a location.</p>
      </div>
    </div>

    <!-- App Footer -->
    <AppFooter />
  </div>
</template>

<script>
import CustomerNavbar from "@/components/CustomerNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";
import instance from '@/axios.js';

export default {
  components: {
    CustomerNavbar,
    AppFooter,
  },
  data() {
    return {
      parkingHistory: [],
      searchLocation: "",
      parkingLots: [],
    };
  },
  methods: {
  async fetchParkingHistory() {
    try {
      const response = await instance.get('/parking/history');
      this.parkingHistory = response.data;
    } catch (error) {
      console.error('Failed to fetch parking history:', error);
    }
  },

  async searchParkingLots() {
    try {
      const response = await instance.get('/parking/search', {
        params: {
          location: this.searchLocation
        }
      });
      this.parkingLots = response.data;
    } catch (error) {
      console.error('Failed to search parking lots:', error);
      this.parkingLots = [];
    }
  },

  async bookParking(lot) {
    this.$router.push({
      path: '/customer_booking',
      query: {
        lotId: lot.parking_lot_id,
        spotId: lot.parking_spot_id,
        userId: localStorage.getItem('customer_email')
      }
    });
  },

  releaseParking(entry) {
    this.$router.push({
      path: '/customer_release',
      query: {
        lotId: entry.parking_lot_id,
        spotId: entry.parking_spot_id
      }
    });
  }
},
  mounted() {
    this.fetchParkingHistory();
  },
};
</script>



<style scoped>
/* Background and container */
.container-fluid {
  background-color: #1a2238; /* dark navy */
  padding: 2rem;
  border-radius: 20px;
  color: #e0e6f0; /* light text */
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
  min-height: calc(100vh - 150px);
  border: 3px dashed #3a5fcd; /* bright blue border */
  transition: all 0.3s ease;
}

/* Section Titles */
.section-title {
  color: #64b5f6; /* bright blue */
  font-weight: 800;
  font-size: 2rem;
  text-align: center;
  margin-bottom: 1.5rem;
}

/* Table */
.table {
  background-color: #202c4a; /* card blue */
  color: #e0e6f0;
  border: 2px solid #3a5fcd;
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.table th {
  background-color: #283655; /* slightly lighter background for header */
  color: #64b5f6;
  font-weight: 700;
  text-align: center;
  border-bottom: 2px solid #3a5fcd;
}

.table td {
  text-align: center;
  border-top: 1px solid #3a5fcd;
  vertical-align: middle;
  font-weight: 600;
}

/* Table hover */
.table-hover tbody tr:hover {
  background-color: #3a5fcd33; /* translucent bright blue */
  cursor: pointer;
}

/* Buttons */
.btn-primary {
  background-color: #3a5fcd;
  border: 1px solid #64b5f6;
  color: #e0e6f0;
  font-weight: 700;
  border-radius: 30px;
  padding: 5px 15px;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #64b5f6;
  border-color: #3a5fcd;
  color: white;
}

.btn-danger {
  background-color: #e53935;
  border: 1px solid #ef5350;
  color: white;
  font-weight: 700;
  border-radius: 30px;
  padding: 5px 15px;
  transition: background-color 0.3s ease;
}

.btn-danger:hover {
  background-color: #ef5350;
  border-color: #e53935;
  color: white;
}

/* Badge */
.badge.bg-success {
  background-color: #4caf50;
  font-weight: 700;
  font-size: 0.9rem;
  padding: 0.5em 0.8em;
  border-radius: 12px;
  color: white;
}

/* Input */
.form-control {
  background-color: #202c4a;
  color: #e0e6f0;
  border: 2px solid #3a5fcd;
  border-radius: 12px;
  font-weight: 600;
  max-width: 500px;
  margin: 0 auto;
  display: block;
  transition: border-color 0.3s ease;
}

.form-control::placeholder {
  color: #64b5f6;
  opacity: 0.7;
}

.form-control:focus {
  outline: none;
  border-color: #64b5f6;
  box-shadow: 0 0 8px #64b5f6aa;
}

/* Centered label */
label.form-label {
  color: #64b5f6;
  font-weight: 700;
  text-align: center;
  display: block;
  margin-bottom: 0.75rem;
}

/* Text-muted fallback */
.text-muted {
  color: #9e9e9e !important;
  font-style: italic;
  margin-top: 1rem;
  font-weight: 500;
}

/* Responsive tweaks */
@media (max-width: 768px) {
  .form-control {
    width: 90% !important;
  }
}
</style>

