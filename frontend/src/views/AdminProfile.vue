<template>
  <div>
    <AdminNavbar />
    <div class="container my-5 striped-bg py-5 px-4">
      <h3 class="text-center mb-4 road-heading">Admin Profile</h3>

      <div class="card profile-card mx-auto p-4">
        <form @submit.prevent="updateProfile">
          <div class="mb-3">
            <label class="form-label">Email address</label>
            <input
              v-model="admin.email"
              type="email"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">New Password</label>
            <input
              v-model="admin.password"
              type="password"
              class="form-control"
              placeholder="Enter new password"
              required
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
import AdminNavbar from "@/components/AdminNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";
import instance from "@/axios";

export default {
  name: "AdminProfile",
  components: {
    AdminNavbar,
    AppFooter,
  },
  data() {
    return {
      admin: {
        email: "",
        password: "",
      },
    };
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await instance.get(`/admin/profile`);
        this.admin.email = res.data.email;
        
      } catch (err) {
        console.error("Error loading profile:", err.message);
        alert("Failed to load profile.");
      }
    },
    async updateProfile() {
  try {
    await instance.put('/admin/update_profile', {
      email: this.admin.email,
      password: this.admin.password
    });
    alert('Profile updated successfully!');
  } catch (err) {
    console.error('Update failed:', err.message);
    alert('Failed to update profile.');
  }
}
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
