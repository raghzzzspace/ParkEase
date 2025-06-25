<template>
  <div class="container-fluid mb-5">
    <AdminNavbar />
    <div class="row mt-4">
      <!-- Revenue from Each Parking Lot -->
      <div class="col-md-6">
        <div class="card custom-card shadow-lg border-0 rounded-3">
          <div class="card-body" style="min-height: 250px; padding: 1.5rem;">
            <h5 class="card-title mb-4 custom-heading">
              Revenue from Each Parking Lot
            </h5>
            <div class="d-flex justify-content-center">
              <canvas id="revenueChart" width="300" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary of Available and Occupied Lots -->
      <div class="col-md-6">
        <div class="card custom-card shadow-lg border-0 rounded-3">
          <div class="card-body" style="min-height: 250px; padding: 1.5rem;">
            <h5 class="card-title mb-4 custom-heading">
              Summary on Available and Occupied Parking Lots
            </h5>
            <div class="d-flex justify-content-center">
              <canvas id="occupancyChart" width="300" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import Chart from 'chart.js/auto';
import AdminNavbar from '@/components/AdminNavbar.vue';
import AppFooter from '@/components/AppFooter.vue';
import instance from "@/axios.js";

export default {
  components: {
    AdminNavbar,
    AppFooter,
  },
  setup() {
    const revenueData = ref([]);
    const occupancySummary = ref({ available: 0, occupied: 0 });

    const initCharts = () => {
      const ctxRevenue = document.getElementById('revenueChart').getContext('2d');
      new Chart(ctxRevenue, {
        type: 'doughnut',
        data: {
          labels: revenueData.value.map((r) => r.parking_id),
          datasets: [{
            data: revenueData.value.map((r) => r.revenue),
            backgroundColor: ['#5c6bc0', '#42a5f5', '#ffb74d'],
            borderColor: '#ffffff',
            borderWidth: 2,
          }],
        },
        options: {
          plugins: {
            legend: {
              position: 'top',
              labels: { color: '#ffffff' },
            },
            tooltip: {
              callbacks: {
                label: (tooltipItem) => `₹${tooltipItem.raw.toLocaleString()} revenue`,
              },
              backgroundColor: '#222',
              titleColor: '#fff',
              bodyColor: '#fff',
            },
          },
          maintainAspectRatio: false,
        },
      });

      const ctxOccupancy = document.getElementById('occupancyChart').getContext('2d');
      new Chart(ctxOccupancy, {
        type: 'bar',
        data: {
          labels: ['Available', 'Occupied'],
          datasets: [{
            label: 'Parking Slots',
            data: [occupancySummary.value.available, occupancySummary.value.occupied],
            backgroundColor: ['#81c784', '#e57373'],
            borderColor: '#ffffff',
            borderWidth: 2,
          }],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              ticks: { color: '#ffffff' },
              grid: { color: 'rgba(255,255,255,0.2)' },
            },
            x: {
              ticks: { color: '#ffffff' },
              grid: { color: 'rgba(255,255,255,0.2)' },
            },
          },
          plugins: {
            legend: {
              display: false,
              labels: { color: '#ffffff' },
            },
            tooltip: {
              callbacks: {
                label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw} slots`,
              },
              backgroundColor: '#222',
              titleColor: '#fff',
              bodyColor: '#fff',
            },
          },
          maintainAspectRatio: false,
        },
      });
    };

    onMounted(async () => {
      try {
        const revRes = await instance.get('/admin_stats/revenue');
        revenueData.value = revRes.data;

        const occRes = await instance.get('/admin_stats/occupancy');
        occupancySummary.value = occRes.data;

        initCharts();
      } catch (e) {
        console.error('Error fetching stats', e);
      }
    });

    return {}; // Not required unless you expose variables to the template
  },
};
</script>

<style scoped>
.custom-card {
  background-color:rgb(5, 28, 65); /* subtle light blue background */
}

.custom-heading {
  color:rgb(150, 190, 242);
  font-weight: 600;
  font-size: 1.5rem;
}

canvas {
  width: 100% !important;
  height: 300px !important;
}
</style>
