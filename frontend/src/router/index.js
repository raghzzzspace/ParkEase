import { createRouter, createWebHistory } from 'vue-router';
import BaseLayout from '@/layout/BaseLayout.vue';
import AllLogin from '@/views/AllLogin.vue';
import CustomerRegister from '@/views/CustomerRegister.vue';
import CustomerDashboard from '@/views/CustomerDashboard.vue';
import CustomerProfile from '@/views/CustomerProfile.vue';
import CustomerSummary from '@/views/CustomerSummary.vue';
import AdminAddService from '@/views/AdminAddService.vue';
import AdminDashboard from '@/views/AdminDashboard.vue';
import AdminEditService from '@/views/AdminEditService.vue';
import AdminSearch from '@/views/AdminSearch.vue';
import AdminSummary from '@/views/AdminSummary.vue';
import AdminUsers from '@/views/AdminUsers.vue';
import ViewdeletePs from '@/views/ViewdeletePspot.vue';
import OccuSpot from '@/views/OccuSpot.vue';
import CustomerBook from '@/views/CustomerBook.vue';
import CustomerRelease from '@/views/CustomerRelease.vue';
import AdminProfile from '@/views/AdminProfile.vue';
import CustomerExport from '@/views/CustomerExport.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: BaseLayout,
  },
  {
    path: '/alllogin',
    name: 'login',
    component: AllLogin
  },
  {
    path: '/customer_register',
    name: 'customer_register',
    component: CustomerRegister
  },
  {
    path: '/customer_dashboard',
    name: 'customer_dashboard',
    component: CustomerDashboard
  },
  {
    path: '/customer_profile',
    name: 'customer_profile',
    component: CustomerProfile
  },
  {
    path: '/customer_summary',
    name: 'customer_summary',
    component: CustomerSummary
  },
  {
    path: '/customer_booking',
    name: 'customer_book',
    component: CustomerBook
  },
  {
    path: '/customer_release',
    name: 'customer_release',
    component: CustomerRelease
  },
  {
    path: '/logout',
    name: 'logout',
    component: AllLogin
  },
  {
    path: '/admin_users',
    name: 'admin_users',
    component: AdminUsers
  }
  ,
  {
    path: '/admin_add_service',
    name: 'admin_add_service',
    component: AdminAddService
  },
  {
    path: '/admin_dashboard',
    name: 'admin_dashboard',
    component: AdminDashboard
  },
  {
    path: '/admin_edit_service/:id',
    name: 'admin_edit_service',
    component: AdminEditService
  },
  {
    path: '/admin_search',
    name: 'admin_search',
    component: AdminSearch
  },
  {
    path: '/admin_summary',
    name: 'admin_summary',
    component: AdminSummary
  },
  {
    path: '/ViewDeletePs/:lotId/:spotId',
    name: 'viewdeletePs',
    component: ViewdeletePs
  },
  {
    path: '/occuspots/:lotId/:spotId',
    name: 'occuspots',
    component: OccuSpot
  },
  {
    path: '/admin_profile',
    name: 'admin_profile',
    component: AdminProfile
  },
  {
    path: '/customer_export',
    name: 'customer_export',
    component: CustomerExport
  }

];

// Create a router instance
const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  
export default router;