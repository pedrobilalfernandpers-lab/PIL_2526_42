<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const matches = ref([])
const loading = ref(true)

const fetchMatches = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/matches', {
      headers: { Authorization: `Bearer ${token}` }
    })
    matches.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const acceptMatch = async (id) => {
  try {
    const token = localStorage.getItem('token')
    await axios.put(`/api/matches/${id}/accept`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    router.push('/chat')
  } catch (err) {
    alert("Erreur lors de l'acceptation")
  }
}

onMounted(fetchMatches)
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold text-gray-900 mb-2">Mes Recommandations</h1>
    <p class="text-gray-500 mb-8">L'algorithme a trouvé ces profils pour vous.</p>
    
    <div v-if="loading" class="flex justify-center py-20">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500"></div>
    </div>
    
    <div v-else class="space-y-6">
      <div v-for="match in matches" :key="match.id" class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col md:flex-row items-center gap-6">
        <div class="w-20 h-20 bg-green-50 rounded-full flex items-center justify-center text-green-600 font-bold text-xl border-4 border-green-100">
          {{ Math.round(match.score) }}%
        </div>
        <div class="flex-grow text-center md:text-left">
          <h3 class="text-xl font-bold text-gray-900">{{ match.skill_name }}</h3>
          <p class="text-gray-600">Vous avez un match avec un(e) étudiant(e) compatible !</p>
          <div class="mt-2 text-sm text-gray-400">Statut: {{ match.status === 'pending' ? 'En attente' : 'Accepté' }}</div>
        </div>
        <div class="flex gap-3" v-if="match.status === 'pending'">
          <button @click="acceptMatch(match.id)" class="bg-brand text-white px-6 py-2.5 rounded-full font-medium hover:bg-brand-dark transition-colors shadow-sm">
            Accepter & Discuter
          </button>
        </div>
        <div v-else class="text-green-600 font-medium bg-green-50 px-4 py-2 rounded-full">
          Match accepté
        </div>
      </div>
      
      <div v-if="matches.length === 0" class="text-center py-12 bg-white rounded-3xl border border-dashed border-gray-200">
        <p class="text-gray-500">Aucun match trouvé pour le moment. Ajoutez plus de compétences !</p>
      </div>
    </div>
  </div>
</template>