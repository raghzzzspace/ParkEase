<template>
  <div>
    <!-- Admin Navbar -->
    <AdminNavbar />

    <!-- Road-styled wrapper -->
    <div class="container my-5 main-wrapper">
      <h2 class="text-center mb-4 main-heading">🔍 Search Parking Lots</h2>

      <form @submit.prevent="submitSearch" class="mb-4">
        <div class="row justify-content-center mb-3">
          <div class="col-md-4">
            <label for="searchBy" class="form-label text-light">Search By</label>
            <select v-model="searchBy" class="form-select" id="searchBy">
              <option value="user_id">User ID</option>
              <option value="location">Location</option>
              <option value="parking_id">Parking Spot ID</option>
            </select>
          </div>
          <div class="col-md-4">
            <label for="searchText" class="form-label text-light">Search Text</label>
            <input
              v-model="searchText"
              type="text"
              class="form-control"
              id="searchText"
              required
            />
          </div>
          <div class="col-md-2 d-flex align-items-end">
            <button type="submit" class="btn custom-btn w-100">Search</button>
          </div>
        </div>

        <p class="text-center text-muted fw-medium">
          <span v-if="searchBy === 'user_id'">Search by User ID.</span>
          <span v-else-if="searchBy === 'location'">Search by Parking Lot Location (e.g., Velachery).</span>
          <span v-else>Search by Parking Spot ID (e.g., Parking#12).</span>
        </p>
      </form>

      <!-- Search Results -->
      <div class="row">
        <div v-for="lot in searchResults" :key="lot.parking_id" class="col-md-4 mb-4">
          <div class="card custom-card shadow p-3 rounded-4">
            <h5 class="text-center text-primary">Parking#{{ lot.parking_id }}</h5>
            <div class="text-center mb-2">
              <a class="text-warning me-2" @click="editLot(lot.parking_id)">Edit</a> |
              <a class="text-danger ms-2" @click="deleteLot(lot.parking_id)">Delete</a>
            </div>
            <p class="text-success text-center fw-bold">
              Occupied: {{ lot.occupied }} / {{ lot.capacity }}
            </p>
            <div class="d-flex flex-wrap justify-content-center">
              <span
                v-for="(slot, index) in lot.slots"
                :key="index"
                :class="['badge', slot === 'A' ? 'bg-success' : 'bg-danger']"
                class="slot-badge"
              >
                {{ slot }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <p v-if="searchResults.length === 0 && searchDone" class="text-center text-warning mt-4">
        No results found for your query.
      </p>
    </div>

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script>
import instance from "@/axios.js";
import AdminNavbar from "@/components/AdminNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";

export default {
  components: {
    AdminNavbar,
    AppFooter,
  },
  data() {
    return {
      searchBy: "user_id",
      searchText: "",
      searchResults: [],
      searchDone: false,
    };
  },
  methods: {
    editLot(id) {
      this.$router.push(`/admin_edit_service/${id}`);
    },
    async deleteLot(id) {
      try {
        await instance.delete(`/admin_delete_service/${id}`);
        this.parkingLots = this.parkingLots.filter(lot => lot.id !== id);
        alert(`Parking Lot #${id} deleted.`);
      } catch (error) {
        console.error('Delete failed:', error.message);
        alert('Failed to delete parking lot.');
      }
    },
    async submitSearch() {
      try {
        const response = await instance.get("admin_search", {
          params: {
            by: this.searchBy,
            text: this.searchText,
          },
        });
        this.searchResults = response.data.results || [];
        this.searchDone = true;
      } catch (error) {
        console.error("Error fetching search results:", error);
        this.searchDone = true;
      }
    },
  },
  watch: {
    searchBy() {
      this.searchResults = [];
      this.searchText = "";
      this.searchDone = false;
    },
  },
};
</script>

<style scoped>
/* ParkEase-style themed styling */

.main-wrapper {
  min-height: calc(100vh - 150px);
  background: repeating-linear-gradient(
    to bottom,
    #1a2238,
    #1a2238 40px,
    #283655 40px,
    #283655 45px
  );
  border-radius: 20px;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
  padding: 30px;
  border: 3px dashed #3a5fcd;
  transition: all 0.3s ease;
  position: relative;
  color: #e0e6f0;
}

.main-wrapper::after {
  content: '';
  display: block;
  height: 6px;
  width: 100%;
  background-image: repeating-linear-gradient(
    to right,
    #3a5fcd 0,
    #3a5fcd 30px,
    transparent 30px,
    transparent 60px
  );
  margin-top: 40px;
}

.main-heading {
  color: #64b5f6;
  font-weight: 800;
  font-size: 2.2rem;
}

.custom-card {
  background: #202c4a;
  border-radius: 20px;
  overflow: hidden;
  border: 2px solid #3a5fcd;
  color: #e0e6f0;
}

.slot-badge {
  margin: 4px;
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.custom-btn {
  border-radius: 30px;
  font-size: 1.1rem;
  padding: 10px 25px;
  border: none;
  background-color: #0d47a1;
  border: 1px dashed #64b5f6;
  color: #fff;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.custom-btn:hover {
  background-color: #1565c0;
}
</style>
