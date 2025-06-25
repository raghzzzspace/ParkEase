<template>
  <div>
    <!-- Navbar Component -->
    <CustomerNavbar />

    <div class="container-fluid my-5">
      <div class="row justify-content-center">
        <!-- Summary Chart Box -->
        <div class="col-md-4">
          <div class="summary-box">
            <div class="chart-container">
              <canvas id="serviceHistoryChart"></canvas>
            </div>
            <p class="chart-caption">Summary on already used parking spots</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Component -->
    <AppFooter />
  </div>
</template>

<script>
import instance from '@/axios.js';
import Chart from 'chart.js/auto';
import CustomerNavbar from "@/components/CustomerNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";

export default {
  components: {
    CustomerNavbar,
    AppFooter
  },
  data() {
    return {
      usageData: [],
  chartInstance: null
    }
  },
  mounted() {
  this.fetchParkingUsageSummary();
},
  methods: {
    fetchParkingUsageSummary() {
  instance.get('/parking-usage-summary')
    .then(response => {
      this.usageData = response.data;
      this.$nextTick(() => this.createUsageChart());
    })
    .catch(error => {
      console.error("Error fetching parking usage summary:", error);
    });
}
,
    createUsageChart() {
  const ctx = document.getElementById('serviceHistoryChart').getContext('2d');
  if (this.chartInstance) this.chartInstance.destroy();

  const labels = this.usageData.map(item => item.lot_name);
  const data = this.usageData.map(item => item.count);

  this.chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Usage Count',
        data: data,
        backgroundColor: ['#4A90E2', '#357ABD', '#2C5AA0'],
        borderRadius: 8,
        borderSkipped: false
      }]
    },
    options: {
      responsive: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#004aad',
          callbacks: {
            label: tooltipItem => `${tooltipItem.label}: ${tooltipItem.raw}`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,
            font: {
              size: 12,
              weight: 'bold'
            }
          },
          grid: {
            drawBorder: false,
            color: '#eee'
          }
        },
        x: {
          ticks: {
            font: {
              size: 12,
              weight: 'bold'
            }
          },
          grid: {
            display: false
          }
        }
      }
    }
  });
}

  }
};
</script>

<style scoped>
/* Container and overall layout */
.container-fluid.my-5 {
  background-color: #f8f9fa; /* light subtle gray background */
  padding: 2rem 1rem;
  min-height: 350px;
  border-radius: 1rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Summary Box with soft shadows and rounded corners */
.summary-box {
  background: #ffffff;
  border-radius: 1.5rem;
  padding: 1.5rem 2rem;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
  max-width: 360px;
  margin: 0 auto;
  transition: transform 0.3s ease;
}
.summary-box:hover {
  transform: translateY(-6px);
}

/* Chart Container - centered flexbox */
.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 260px;
}

/* Canvas with fixed size and smooth edges */
canvas {
  width: 320px !important;
  height: 260px !important;
  border-radius: 1rem;
}

/* Caption below the chart with subtle styling */
.chart-caption {
  font-size: 1rem;
  margin-top: 1rem;
  color: #555555;
  font-style: italic;
  font-weight: 500;
  user-select: none;
  letter-spacing: 0.02em;
}
.summary-wrapper {
  background: repeating-linear-gradient(
    to bottom,
    #1a2238,
    #1a2238 40px,
    #283655 40px,
    #283655 45px
  );
  padding: 2rem 1rem;
  min-height: 400px;
  border-radius: 1.5rem;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
  border: 3px dashed #3a5fcd;
  color: #e0e6f0;
}

.summary-wrapper::after {
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

.summary-box {
  background: linear-gradient(145deg, #1c253b, #232f4d);
  border-radius: 1.5rem;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  border: 2px solid #3a5fcd;
  transition: transform 0.3s ease;
  max-width: 480px;
}

.summary-box:hover {
  transform: translateY(-6px);
}

.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 260px;
}

canvas {
  width: 320px !important;
  height: 260px !important;
  background: #ffffff;
  border-radius: 1rem;
}

.chart-caption {
  font-size: 1rem;
  margin-top: 1.2rem;
  color: #64b5f6;
  font-style: italic;
  font-weight: 500;
  user-select: none;
  letter-spacing: 0.03em;
}


</style>
