<template>
  <div>
    <!-- Navbar Component -->
    <AppNavbar />

    <!-- Main content -->
    <div class="content-wrapper d-flex justify-content-center align-items-center road-bg">
      <div class="p-4 road-card shadow-lg rounded">
        <h2 class="text-center mb-4">🚦 Customer Sign Up 🛣️</h2>

        <!-- Flash messages -->
        <div v-if="messages.length > 0">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="`alert alert-${message.category} alert-dismissible fade show`"
            role="alert"
          >
            {{ message.text }}
            <button
              type="button"
              class="close"
              @click="closeMessage(index)"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        </div>

        <!-- Registration Form -->
        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input
              type="email"
              v-model="form.email"
              class="form-control road-input"
              id="email"
              required
            />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              v-model="form.password"
              class="form-control road-input"
              id="password"
              required
            />
          </div>

          <div class="mb-3">
            <label for="fullname" class="form-label">Full Name</label>
            <input
              type="text"
              v-model="form.full_name"
              class="form-control road-input"
              id="fullname"
              required
            />
          </div>

          <div class="mb-3">
            <label for="address" class="form-label">Address</label>
            <input
              type="text"
              v-model="form.address"
              class="form-control road-input"
              id="address"
              required
            />
          </div>

          <div class="mb-3">
            <label for="pincode" class="form-label">Pincode</label>
            <input
              type="text"
              v-model="form.pincode"
              class="form-control road-input"
              id="pincode"
              required
            />
          </div>

          <button type="submit" class="btn btn-dark w-100 mt-4">
            🚗 Register
          </button>
        </form>

        <p class="text-center mt-3">
          <router-link to="/alllogin" class="text-white text-decoration-underline">
            Already parked? 🅿️ Login here
          </router-link>
        </p>
      </div>
    </div>

    <!-- Footer Component -->
    <AppFooter />
  </div>
</template>

<script>
import AppNavbar from "@/components/AppNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";
import instance from "@/axios.js";

export default {
  name: "CustomerRegister",
  components: {
    AppNavbar,
    AppFooter,
  },
  data() {
    return {
      form: {
        email: "",
        password: "",
        full_name: "",
        address: "",
        pincode: "",
      },
      messages: [],
    };
  },
  methods: {
    closeMessage(index) {
      this.messages.splice(index, 1);
    },
    async handleRegister() {
      if (
        this.form.email &&
        this.form.password &&
        this.form.full_name &&
        this.form.address &&
        this.form.pincode
      ) {
        try {
          const response = await instance.post("customer_register", this.form);
          this.messages.push({
            category: "success",
            text: response.data.message,
          });
        } catch (error) {
          const errorMsg = error.response?.data?.error || "Registration failed";
          this.messages.push({
            category: "danger",
            text: errorMsg,
          });
        }
      } else {
        this.messages.push({
          category: "danger",
          text: "Please fill in all required fields.",
        });
      }
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
