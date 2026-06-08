<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token')
})

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <!-- Navbar minimaliste Blanc/Bleu -->
    <header class="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center cursor-pointer" @click="router.push('/')">
            <span class="text-2xl font-bold text-brand">MentorLink</span>
            <span class="ml-2 text-sm font-medium text-gray-500 hidden sm:block">IFRI</span>
          </div>
          
          <div class="flex items-center space-x-4">
            <template v-if="!isAuthenticated">
              <router-link to="/login" class="text-gray-600 hover:text-brand font-medium transition-colors">Connexion</router-link>
              <router-link to="/register" class="bg-brand hover:bg-brand-dark text-white px-5 py-2 rounded-full font-medium transition-colors shadow-sm">S'inscrire</router-link>
            </template>
            <template v-else>
              <router-link to="/dashboard" class="text-gray-600 hover:text-brand font-medium transition-colors">Tableau de bord</router-link>
              <button @click="logout" class="text-red-500 hover:text-red-700 font-medium transition-colors">Déconnexion</button>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow">
      <router-view />
    </main>

    <!-- Footer minimaliste -->
    <footer class="bg-white border-t border-gray-100 py-8 mt-12">
      <div class="max-w-6xl mx-auto px-4 text-center text-gray-400 text-sm">
        &copy; 2026 IFRI MentorLink. Projet Intégrateur.
      </div>
    </footer>
  </div>
</template>