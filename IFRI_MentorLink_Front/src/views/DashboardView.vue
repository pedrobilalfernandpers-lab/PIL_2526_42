<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const user = ref(null)
const loading = ref(true)
const errorMsg = ref('')

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/users/me', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = res.data
  } catch (err) {
    errorMsg.value = "Session expirée. Veuillez vous reconnecter."
    localStorage.removeItem('token')
    setTimeout(() => router.push('/login'), 2000)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-12">
    
    <div v-if="loading" class="flex justify-center py-20">
      <div class="animate-pulse bg-gray-200 h-12 w-48 rounded-lg"></div>
    </div>
    
    <div v-else-if="errorMsg" class="bg-red-50 text-red-600 p-4 rounded-xl text-center">
      {{ errorMsg }}
    </div>
    
    <div v-else-if="user" class="space-y-8">
      
      <!-- En-tête du Dashboard -->
      <div class="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm flex flex-col md:flex-row items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Bonjour, {{ user.first_name }} 👋</h1>
          <p class="text-gray-500">{{ user.field_of_study }} • {{ user.level }}</p>
        </div>
        <div class="mt-4 md:mt-0 flex gap-3">
          <button @click="$router.push('/matches')" class="bg-brand-light text-brand px-6 py-2.5 rounded-xl font-medium hover:bg-blue-100 transition-colors">
            Trouver un mentor
          </button>
          <button @click="$router.push('/posts')" class="bg-brand text-white px-6 py-2.5 rounded-xl font-medium hover:bg-brand-dark transition-colors shadow-sm shadow-blue-500/20">
            Voir les annonces
          </button>
        </div>
      </div>
      
      <!-- Stats / Raccourcis -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div @click="$router.push('/chat')" class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
          <div class="w-10 h-10 bg-blue-50 text-brand rounded-full flex items-center justify-center mb-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"></path></svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-1">Messagerie</h3>
          <p class="text-sm text-gray-500">Gérez vos conversations.</p>
        </div>
        
        <div @click="$router.push('/matches')" class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
          <div class="w-10 h-10 bg-green-50 text-green-600 rounded-full flex items-center justify-center mb-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-1">Mes Recommandations</h3>
          <p class="text-sm text-gray-500">Voir les mentors proposés.</p>
        </div>
        
        <div @click="$router.push('/profile')" class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
          <div class="w-10 h-10 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center mb-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-1">Mon Profil</h3>
          <p class="text-sm text-gray-500">Mettez à jour vos infos.</p>
        </div>
      </div>
      
    </div>
  </div>
</template>