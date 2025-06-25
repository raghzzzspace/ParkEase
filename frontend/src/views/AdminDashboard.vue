<template>
  <div>
    <AdminNavbar />
    <div class="container my-5 striped-bg py-5 px-4">
      <h3 class="text-center mb-4 road-heading">Parking Lots</h3>

      <!-- Parking Lot Cards -->
      <div class="row">
        <div class="col-md-4 mb-4" v-for="lot in parkingLots" :key="lot.id">
          <div class="lot-card shadow">
            <h5 class="lot-title">
              Parking#{{ lot.id }}
              <small class="ms-2">
                <a class="edit-link" @click="editLot(lot.id)">Edit</a> |
                <a class="delete-link" @click="deleteLot(lot.id)">Delete</a>
              </small>
            </h5>
            <p class="occupancy">(Occupied: {{ lot.occupied }}/{{ lot.total }})</p>

            <!-- Slot Grid -->
            <div class="slot-grid">
  <div
    v-for="slot in lot.slots"
    :key="slot.parking_spot_id"
    :class="['slot', slot.status === 'A' ? 'available' : 'occupied']"
    @click="goToViewDeletePs(lot.id, slot.parking_spot_id)"
  >
    {{ slot.status }}
  </div>
</div>

          </div>
        </div>
      </div>

      <!-- Add Lot Button -->
      <div class="text-center mt-4">
        <button class="add-lot-btn" @click="goToAddLot">+ Add Lot</button>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue';
import AppFooter from '@/components/AppFooter.vue';
import instance from '@/axios';

export default {
  name: 'AdminDashboard',
  components: {
    AdminNavbar,
    AppFooter
  },
  data() {
    return {
      parkingLots: []
    };
  },
  mounted() {
  this.fetchParkingLots();
},
  methods: {
    goToAddLot() {
      this.$router.push('/admin_add_service');
    },
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
    goToViewDeletePs(parkingLotId, spotId) {
      this.$router.push(`/ViewDeletePs/${parkingLotId}/${spotId}`);
    },
    async fetchParkingLots() {
    try {
      const response = await instance.get('/get_all_parking_lots');
      this.parkingLots = response.data;
    } catch (error) {
      console.error('Failed to fetch parking lots:', error);
      alert('Error loading parking lots.');
    }
  }
  }
};
</script>

<style scoped>
.striped-bg {
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

.striped-bg::after {
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

.road-heading {
  color: #64b5f6;
  font-weight: 800;
  font-size: 2.2rem;
}

.lot-card {
  background: #202c4a;
  border-radius: 20px;
  padding: 1.5rem;
  color: #e0e6f0;
  border: 2px solid #3a5fcd;
  min-height: 250px;
  box-shadow: 0 6px 15px rgba(0,0,0,0.3);
}

.lot-title {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #64b5f6;
}

.edit-link {
  color: #64b5f6;
  cursor: pointer;
  transition: color 0.3s ease;
}

.edit-link:hover {
  color: #a2d2ff;
}

.delete-link {
  color: #ef5350;
  cursor: pointer;
  transition: color 0.3s ease;
}

.delete-link:hover {
  color: #ff8a80;
}

.occupancy {
  font-size: 1rem;
  color: #81c784;
  margin-bottom: 1.2rem;
  font-weight: 600;
}

.slot-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.slot {
  width: 36px;
  height: 36px;
  text-align: center;
  line-height: 36px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, background-color 0.3s ease;
  user-select: none;
}

.slot:hover {
  transform: scale(1.1);
}

.available {
  background-color: #4caf50;
  color: white;
  
}

.occupied {
  background-color: #e53935;
  color: white;
  
}

.add-lot-btn {
  background-color: #0d47a1;
  border: 1px dashed #64b5f6;
  padding: 12px 28px;
  color: white;
  font-weight: 800;
  font-size: 1.1rem;
  border-radius: 30px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-lot-btn:hover {
  background-color: #1565c0;
}
</style>
