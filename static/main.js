import Vue from 'vue';
import App from './App.vue';
import router from './src/router/index';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { axios } from './src/services/axios'
import VueTelInput from 'vue-tel-input';


Vue.use(VueTelInput);

Vue.prototype.$http = axios;

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
