<template>
  <div>
    <!-- Navbar -->
    <AppNavbar />

    <!-- Main Content -->
    <div class="content-wrapper d-flex justify-content-center align-items-center road-bg">
      <div class="p-4 road-card shadow-lg rounded">
        <h2 class="text-center mb-4 text-white">🚗 ParkEase: Smart Vehicle Parking System</h2>

        <!-- Flash messages -->
        <div v-if="messages.length > 0">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="`alert alert-${message.category} alert-dismissible fade show`"
            role="alert"
          >
            {{ message.text }}
            <button type="button" class="close" @click="closeMessage(index)" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label for="email" class="form-label">📧 Email</label>
            <input
              type="email"
              v-model="email"
              class="form-control road-input"
              id="email"
              placeholder="Enter your email"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">🔐 Password</label>
            <input
              type="password"
              v-model="password"
              class="form-control road-input"
              id="password"
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit" class="btn btn-dark w-100 mt-4">Login</button>
        </form>

        <div class="text-center mt-3">
          <p class="text-white">
            🚙 New to ParkEase?
            <router-link to="/customer_register" class="text-decoration-underline text-white">Register here</router-link>
          </p>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script>
import AppNavbar from '@/components/AppNavbar.vue';
import AppFooter from '@/components/AppFooter.vue';
import instance from '@/axios.js';

export default {
  name: 'AllLogin',
  components: {
    AppNavbar,
    AppFooter,
  },
  data() {
    return {
      email: '',
      password: '',
      messages: [],
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await instance.post('login', {
          email: this.email,
          password: this.password,
        });

        if (response.data.success) {
          this.messages.push({ category: 'success', text: '✅ Login successful!' });

          const role = response.data.role;
          if (role === 'admin') {
            this.$router.push('/admin_dashboard');
          } else if (role === 'customer') {
            localStorage.setItem('customer_email', this.email);
            this.$router.push('/customer_dashboard');
          }
        } else {
          this.messages.push({
            category: 'danger',
            text: '❌ Invalid credentials. Please try again.',
          });
        }
      } catch (error) {
        console.error(error);
        this.messages.push({
          category: 'danger',
          text: '⚠️ An error occurred while logging in. Please try again.',
        });
      }
    },
    closeMessage(index) {
      this.messages.splice(index, 1);
    },
  },
};
</script>

<style scoped>

.content-wrapper {
  min-height: calc(100vh - 120px);
  background-color: #1a2238; /* Dark blue base */
  padding-top: 60px;
}

/* Road background with blue lanes (updated) */
.road-bg {
  background: repeating-linear-gradient(
    to bottom,
    #1a2238, /* deep navy */
    #1a2238 40px,
    #283655 40px,
    #283655 45px
  );
}

/* Card with bluish tint */
.road-card {
  max-width: 420px;
  width: 100%;
  background: #202c4a;
  color: #ffffff;
  border: 2px solid #3a5fcd; /* bluish border */
}

/* Input fields with blue focus */
.road-input {
  background-color: #e3f2fd; /* light blue */
  border: 2px solid #3a5fcd;
  color: #000;
}

.road-input:focus {
  outline: none;
  border-color: #1976d2; /* strong blue */
  box-shadow: 0 0 5px #64b5f6;
}

/* Button styled like a blue vehicle */
button.btn-dark {
  background-color: #0d47a1;
  border: 1px dashed #64b5f6;
  color: #fff;
  transition: background-color 0.3s ease;
}

button.btn-dark:hover {
  background-color: #1565c0;
}

</style>
