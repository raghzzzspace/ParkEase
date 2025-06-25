<template>
  <nav class="navbar navbar-expand-lg shadow mb-4" style="background: linear-gradient(to bottom, #0066cc, #004aad);">
    <div class="container-fluid">
      <a class="navbar-brand ms-3" href="#" style="color: #ffffff;">Welcome to Admin Dashboard</a>

      <div class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto ms-5">
          <li class="nav-item">
            <router-link class="nav-link" to="/admin_dashboard">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin_users">Users</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin_search">Search</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin_summary">Summary</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/logout">Logout</router-link>
          </li>
        </ul>

        <!-- Right-aligned Profile Option -->
        <ul class="navbar-nav ms-auto me-3">
          <li class="nav-item">
            <router-link class="nav-link" to="/admin_profile">
              <i class="fas fa-user-circle"></i> Edit Profile
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

  
  <script>
  export default {
    name: 'AdminNavbar'
  };
  </script>
  
 <style scoped>
.navbar {
  background: linear-gradient(to bottom, #0066cc, #004aad);
}

.navbar-brand {
  color: #ffffff;
}

.nav-link {
  color: #ffffff !important;
}

.nav-link:hover {
  color: #d6d6d6 !important;
}
</style>
