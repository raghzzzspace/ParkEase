<template>
  <div>
    <!-- Navbar -->
    <AdminNavbar />


    <!-- Users Table -->
    <div class="container table-wrapper">
    <!-- Page Title -->
    <div class="text-center my-4">
      <h3 class="fw-bold page-heading">📋 Registered Users</h3>
    </div>
      <div class="table-responsive rounded shadow-sm p-3">
        <table class="table table-bordered table-hover align-middle text-center custom-table">
          <thead>
            <tr>
              <th>USER ID</th>
              <th>E-Mail</th>
              <th>Full Name</th>
              <th>Address</th>
              <th>Pin Code</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user) in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.full_name }}</td>
              <td>{{ user.address }}</td>
              <td>{{ user.pin_code }}</td>
            </tr>
            <tr v-if="users.length === 0">
              <td colspan="5" class="text-danger fw-bold">No registered users found.</td>
            </tr>
          </tbody>
        </table>
      </div>
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
  name: "AdminUsers",
  components: {
    AdminNavbar,
    AppFooter,
  },
  data() {
    return {
      users: [],
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await instance.get("/admin_users");
        this.users = response.data.users || [];
        console.log("Fetched users:", this.users);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Background with road-striping effect */
.table-wrapper {
  min-height: calc(100vh - 180px);
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
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
  color: #e0e6f0;
  transition: all 0.3s ease;
  position: relative;
}

/* Dashed lane strip at bottom */
.table-wrapper::after {
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
  margin-top: 30px;
}

/* Table Styling */
.custom-table {
  background-color: #202c4a;
  color: #e0e6f0;
  border-color: #3a5fcd;
}

.custom-table thead {
  background-color: #3a5fcd;
  color: #ffffff;
}

.custom-table th,
.custom-table td {
  border: 1px solid #3a5fcd;
}

.custom-table tbody tr:hover {
  background-color: rgba(100, 181, 246, 0.2);
  transition: background-color 0.3s ease;
}

/* Heading */
.page-heading {
  color:rgb(212, 228, 240);
  font-size: 2rem;
}

/* Responsive Text */
.table {
  font-size: 1rem;
}

th,
td {
  vertical-align: middle;
}
</style>
