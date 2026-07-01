import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Categorias from '../views/Categorias.vue'
import Votar from '../views/Votar.vue'
import Resultados from '../views/Resultados.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/categorias', component: Categorias },
  { path: '/votar/:id', name: 'Votar', component: Votar, props: true },
  { path: '/resultados', component: Resultados },
]

export default createRouter({ history: createWebHistory(), routes })
