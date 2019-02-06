// CSS for bootstrap
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Vue from 'vue'
import store from './store/index'
import router from './router/index'
import BootstrapVue from 'bootstrap-vue'
import VueResource from 'vue-resource'

import App from './App.vue'

Vue.use(BootstrapVue)
Vue.use(VueResource)

Vue.config.productionTip = false

import { Navbar } from 'bootstrap-vue/es/components'
Vue.use(Navbar)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
