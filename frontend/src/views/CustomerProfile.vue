<template>
  <div>
    <CustomerNavbar />
    <div class="container my-5 striped-bg py-5 px-4">
      <h3 class="text-center mb-4 road-heading">Customer Profile</h3>

      <div class="card profile-card mx-auto p-4">
        <form @submit.prevent="updateProfile">
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input
              v-model="customer.full_name"
              type="text"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Email address</label>
            <input
              v-model="customer.email"
              type="email"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Address</label>
            <input
              v-model="customer.address"
              type="text"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Pincode</label>
            <input
              v-model="customer.pincode"
              type="text"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">New Password</label>
            <input
              v-model="customer.password"
              type="password"
              class="form-control"
              placeholder="Enter new password"
              
            />
          </div>

          <button type="submit" class="btn btn-primary w-100">
            Update Profile
          </button>
        </form>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script>
import CustomerNavbar from "@/components/CustomerNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";
import instance from "@/axios";

export default {
  name: "CustomerProfile",
  components: {
    CustomerNavbar,
    AppFooter,
  },
  data() {
    return {
      customer: {
        email: "",
        password: "",
        full_name: "",
        address: "",
        pincode: "",
      },
    };
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await instance.get(`/customer/profile`);
        this.customer = {
          email: res.data.email,
          full_name: res.data.full_name,
          address: res.data.address,
          pincode: res.data.pincode,
          password: "", // blank for new input
        };
      } catch (err) {
        console.error("Error loading profile:", err.message);
        alert("Failed to load profile.");
      }
    },
    async updateProfile() {
      try {
        await instance.put(`/customer/update_profile`, {
          email: this.customer.email,
          full_name: this.customer.full_name,
          address: this.customer.address,
          pincode: this.customer.pincode,
          password: this.customer.password,
        });
        alert("Profile updated successfully!");
        this.$router.push('/customer_dashboard');
      } catch (err) {
        console.error("Update failed:", err.message);
        alert("Failed to update profile.");
      }
    },
  },
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
  padding: 30px;
  border: 3px dashed #3a5fcd;
  color: #e0e6f0;
}

.road-heading {
  color: #64b5f6;
  font-weight: 800;
  font-size: 2.2rem;
}

.profile-card {
  max-width: 500px;
  background: #202c4a;
  border: 2px solid #3a5fcd;
  border-radius: 20px;
  color: #e0e6f0;
}

.form-label {
  color: #b0bec5;
}

.form-control {
  background-color: #1a2238;
  color: #e0e6f0;
  border: 1px solid #3a5fcd;
}

.form-control:focus {
  border-color: #64b5f6;
  box-shadow: none;
}

.btn-primary {
  background-color: #0d47a1;
  border: none;
  font-weight: 700;
}

.btn-primary:hover {
  background-color: #1565c0;
}
</style>
