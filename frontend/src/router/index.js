import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Game from '../views/Game.vue'
import MoleculeLibrary from '../views/MoleculeLibrary.vue'
import Synthesis from '../views/Synthesis.vue'
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
    path: '/synthesis',
    name: 'Synthesis',
    component: Synthesis,
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

