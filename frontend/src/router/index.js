import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Game from '../views/Game.vue'
import MoleculeLibrary from '../views/MoleculeLibrary.vue'
import PropertiesLibrary from '../views/PropertiesLibrary.vue'
import Synthesis from '../views/Synthesis.vue'
import AutoSynthesis from '../views/AutoSynthesis.vue'
import Simulation from '../views/Simulation.vue'
import MoleculeBuilder from '../views/MoleculeBuilder.vue'
import PlayerSelect from '../views/PlayerSelect.vue'
import { getCurrentSave } from '../services/api.js'

const routes = [
  {
    path: '/player-select',
    name: 'PlayerSelect',
    component: PlayerSelect
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/game',
    name: 'Game',
    component: Game,
    meta: { requiresAuth: true }
  },
  {
    path: '/molecules',
    name: 'MoleculeLibrary',
    component: MoleculeLibrary,
    meta: { requiresAuth: true }
  },
  {
    path: '/properties',
    name: 'PropertiesLibrary',
    component: PropertiesLibrary,
    meta: { requiresAuth: true }
  },
  {
    path: '/synthesis',
    name: 'Synthesis',
    component: Synthesis,
    meta: { requiresAuth: true }
  },
  {
    path: '/auto-synthesis',
    name: 'AutoSynthesis',
    component: AutoSynthesis,
    meta: { requiresAuth: true }
  },
  {
    path: '/simulation',
    name: 'Simulation',
    component: Simulation,
    meta: { requiresAuth: true }
  },
  {
    path: '/builder',
    name: 'MoleculeBuilder',
    component: MoleculeBuilder,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegação - redireciona para seleção de jogador se não houver save ativo
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const response = await getCurrentSave()
      if (response.success) {
        next()
      } else {
        next('/player-select')
      }
    } catch (error) {
      next('/player-select')
    }
  } else {
    next()
  }
})

export default router

