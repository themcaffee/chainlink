import Vue from 'vue'
import Router from 'vue-router'

const PythonRequirements = () => import('@/pages/PythonRequirements')
const Error404 = () => import('@/pages/Error404')

Vue.use(Router)

const routes = [
  { path: '/', name: 'root', component: PythonRequirements },
  { path: '*', component: Error404 }
]

const router = new Router({
  mode: 'history',
  routes
})

export default router
