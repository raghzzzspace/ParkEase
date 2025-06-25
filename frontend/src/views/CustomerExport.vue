<template>
  <div>
    <CustomerNavbar />

    <div class="container-fluid mt-5 text-center">
      <h2 class="section-title">Export Parking History</h2>

      <!--  Descriptive Paragraph -->
      <p class="info-paragraph">
        Generate and download a detailed CSV report of your parking history. This includes slot details, locations, vehicle numbers, costs, and timestamps — all in one convenient file. Ideal for record-keeping or expense tracking.
      </p>

      <p class="mb-4 text-muted">Click below to generate your parking history report.</p>

      <button class="btn btn-primary px-4 py-2" @click="exportCSV" :disabled="loading">
        {{ loading ? "Generating..." : "Export CSV" }}
      </button>

      <div v-if="exportResult" class="mt-4 text-success fw-bold">
        {{ exportResult.message }} ({{ exportResult.records }} records)
      </div>

      <div v-if="errorMessage" class="mt-3 text-danger fw-bold">
        {{ errorMessage }}
      </div>
    </div>

    <AppFooter />
  </div>
</template>


<script>
import CustomerNavbar from "@/components/CustomerNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";
import instance from "@/axios.js";

export default {
  components: {
    CustomerNavbar,
    AppFooter,
  },
  data() {
    return {
      loading: false,
      exportResult: null,
      errorMessage: "",
      downloadUrl:"",
    };
  },
  methods: {
    async exportCSV() {
  this.loading = true;
  this.downloadUrl = "";
  this.errorMessage = "";
  this.exportResult = null;

  try {
    const triggerResponse = await instance.post("/trigger-export", {
      email: localStorage.getItem("customer_email"),
    });

    const taskId = triggerResponse.data.task_id;
    this.exportResult = {
      message: triggerResponse.data.message,
      records: triggerResponse.data.records
    };

    const checkStatus = async () => {
      const statusRes = await instance.get(`/export-status/${taskId}`);
      if (statusRes.data.status === "ready") {
        this.downloadUrl = statusRes.data.downloadUrl;
        this.loading = false;
        console.log(this.downloadUrl);

        // Auto-download
        const a = document.createElement("a");
        a.href = this.downloadUrl;
        a.setAttribute("download", this.downloadUrl.split('/').pop());
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } else if (statusRes.data.status === "failed") {
        this.loading = false;
        this.errorMessage = "Export failed. Please try again.";
      } else {
        setTimeout(checkStatus, 3000);
      }
    };

    checkStatus();
  } catch (error) {
    console.error("Export error:", error);
    this.errorMessage = "Failed to trigger export.";
    this.loading = false;
  }
}


  }
};
</script>




<style scoped>
.container-fluid {
  background-color: #1a2238;
  padding: 2rem;
  border-radius: 20px;
  color: #e0e6f0;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
  max-width: 600px;
  margin: auto;
  border: 3px dashed #3a5fcd;
  transition: all 0.3s ease;
}

.section-title {
  color: #64b5f6;
  font-weight: 800;
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

.btn-primary {
  background-color: #3a5fcd;
  border: 1px solid #64b5f6;
  color: #fff;
  font-weight: 700;
  border-radius: 30px;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #64b5f6;
  color: #000;
}

.btn-success {
  background-color: #4caf50;
  border: none;
  color: #fff;
  font-weight: 700;
  border-radius: 30px;
  padding: 10px 20px;
}

.text-muted {
  color: #b0bec5;
}

.info-paragraph {
  color: #cfd8dc;
  font-size: 1rem;
  max-width: 540px;
  margin: 0 auto 1rem auto;
  font-style: italic;
  line-height: 1.6;
}

</style>
