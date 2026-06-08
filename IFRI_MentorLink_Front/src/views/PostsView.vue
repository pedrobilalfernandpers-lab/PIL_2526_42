<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const posts = ref([])
const skills = ref([])
const loading = ref(true)

const showModal = ref(false)

const filterType = ref('')
const filterSkill = ref('')

const getEmptyPost = () => ({
  type: 'request',
  skill_id: '',
  description: '',
  mode: 'online',
  availabilities: []
})

const newPost = ref(getEmptyPost())

const getToken = () => localStorage.getItem('token')

const fetchData = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterType.value) params.type = filterType.value
    if (filterSkill.value) params.skill_id = filterSkill.value

    const [postsRes, skillsRes] = await Promise.all([
      axios.get('/api/posts', { 
        headers: { Authorization: `Bearer ${getToken()}` },
        params: params 
      }),
      axios.get('/api/skills')
    ])
    posts.value = postsRes.data
    skills.value = skillsRes.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Relancer fetchData quand un filtre change
import { watch } from 'vue'
watch([filterType, filterSkill], () => {
  fetchData()
})

const addAvailability = () => {
  newPost.value.availabilities.push({
    day_of_week: 'Monday',
    start_time: '08:00:00',
    end_time: '10:00:00'
  })
}

const removeAvailability = (index) => {
  newPost.value.availabilities.splice(index, 1)
}

const createPost = async () => {
  if (!newPost.value.skill_id || !newPost.value.description) return
  
  const payload = {
    ...newPost.value,
    availabilities: newPost.value.availabilities.map(a => ({
      ...a,
      start_time: a.start_time.length === 5 ? `${a.start_time}:00` : a.start_time,
      end_time: a.end_time.length === 5 ? `${a.end_time}:00` : a.end_time
    }))
  }
  
  try {
    await axios.post('/api/posts', payload, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
    showModal.value = false
    newPost.value = getEmptyPost()
    fetchData() 
  } catch (err) {
    console.error(err)
    alert("Erreur lors de la création de l'annonce. Vérifiez que l'heure de fin est bien après l'heure de début.")
  }
}

import { useRouter } from 'vue-router'
const router = useRouter()

const applyToPost = async (postId) => {
  try {
    const res = await axios.post(`/api/posts/${postId}/apply`, {}, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
    alert(res.data.message)
    router.push('/chat')
  } catch (err) {
    if (err.response && err.response.data) {
      alert(err.response.data.detail)
    } else {
      console.error(err)
      alert("Erreur lors de la candidature.")
    }
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-12 relative">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Mur des Annonces</h1>
      
      <!-- Filtres -->
      <div class="flex gap-3 w-full md:w-auto">
        <select v-model="filterType" class="px-4 py-2.5 bg-white border border-gray-200 rounded-full text-sm font-medium focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent text-gray-700 shadow-sm flex-1 md:flex-none min-w-[140px]">
          <option value="">Tous les types</option>
          <option value="offer">Offres de Mentorat</option>
          <option value="request">Demandes d'Aide</option>
        </select>
        
        <select v-model="filterSkill" class="px-4 py-2.5 bg-white border border-gray-200 rounded-full text-sm font-medium focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent text-gray-700 shadow-sm flex-1 md:flex-none min-w-[140px]">
          <option value="">Toutes les matières</option>
          <option v-for="s in skills" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>

        <button @click="showModal = true" class="bg-brand text-white px-6 py-2.5 rounded-full font-medium hover:bg-brand-dark shadow-sm flex-shrink-0">
          + Nouvelle
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="flex justify-center py-20">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-brand"></div>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="post in posts" :key="post.id" class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col">
        <div class="flex justify-between items-start mb-4">
          <span class="px-3 py-1 text-xs font-bold rounded-full"
                :class="post.type === 'offer' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'">
            {{ post.type === 'offer' ? 'OFFRE MENTORAT' : 'DEMANDE AIDE' }}
          </span>
          <span class="text-gray-400 text-xs">{{ new Date(post.created_at).toLocaleDateString() }}</span>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">{{ post.skill_name }}</h3>
        <p class="text-gray-600 text-sm mb-4 flex-grow">{{ post.description }}</p>
        
        <!-- Créneaux -->
        <div v-if="post.availabilities && post.availabilities.length > 0" class="mb-4">
          <div class="text-xs text-gray-400 mb-1 uppercase font-bold tracking-wider">Disponibilités</div>
          <div class="flex flex-wrap gap-2">
            <span v-for="avail in post.availabilities" :key="avail.id" class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-md">
              {{ avail.day_of_week.substring(0,3) }}. {{ avail.start_time.substring(0,5) }}-{{ avail.end_time.substring(0,5) }}
            </span>
          </div>
        </div>

        <div class="flex justify-between items-center mt-auto">
          <div class="text-sm text-gray-500 bg-gray-50 px-3 py-2 rounded-xl">
            📍 {{ post.mode === 'online' ? 'En ligne' : (post.mode === 'offline' ? 'Présentiel' : 'Les deux') }}
          </div>
          <button @click="applyToPost(post.id)" class="text-brand font-medium text-sm hover:underline flex items-center gap-1">
            Répondre
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
          </button>
        </div>
      </div>
      <div v-if="posts.length === 0" class="col-span-full text-center py-12 text-gray-500">
        Aucune annonce pour le moment.
      </div>
    </div>

    <!-- Modal Nouvelle Annonce -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center z-50 p-4">
      <div class="bg-white p-8 rounded-3xl w-full max-w-lg shadow-2xl max-h-[90vh] overflow-y-auto">
        <h2 class="text-2xl font-bold mb-6">Créer une annonce</h2>
        <form @submit.prevent="createPost" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Type d'annonce</label>
              <select v-model="newPost.type" class="w-full px-4 py-3 bg-gray-50 rounded-xl">
                <option value="request">Je demande de l'aide</option>
                <option value="offer">Je propose mon aide</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Mode</label>
              <select v-model="newPost.mode" class="w-full px-4 py-3 bg-gray-50 rounded-xl">
                <option value="online">En ligne</option>
                <option value="offline">En présentiel</option>
                <option value="both">Les deux (Hybride)</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Matière / Compétence</label>
            <select v-model="newPost.skill_id" required class="w-full px-4 py-3 bg-gray-50 rounded-xl">
              <option value="" disabled>Choisir...</option>
              <option v-for="s in skills" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea v-model="newPost.description" required rows="2" class="w-full px-4 py-3 bg-gray-50 rounded-xl" placeholder="Décrivez votre besoin ou votre offre..."></textarea>
          </div>

          <!-- Section Horaires -->
          <div class="bg-blue-50/50 p-4 rounded-2xl border border-blue-100">
            <div class="flex justify-between items-center mb-3">
              <label class="block text-sm font-medium text-gray-700">Créneaux horaires (Optionnel)</label>
              <button type="button" @click="addAvailability" class="text-brand text-sm font-bold bg-white px-3 py-1 rounded-lg shadow-sm hover:shadow transition">+ Ajouter</button>
            </div>
            
            <div v-for="(avail, index) in newPost.availabilities" :key="index" class="flex items-center gap-2 mb-2 bg-white p-2 rounded-xl border border-gray-100">
              <select v-model="avail.day_of_week" class="bg-transparent text-sm p-1 outline-none">
                <option value="Monday">Lundi</option>
                <option value="Tuesday">Mardi</option>
                <option value="Wednesday">Mercredi</option>
                <option value="Thursday">Jeudi</option>
                <option value="Friday">Vendredi</option>
                <option value="Saturday">Samedi</option>
                <option value="Sunday">Dimanche</option>
              </select>
              <input type="time" v-model="avail.start_time" class="bg-gray-50 rounded p-1 text-sm outline-none w-24">
              <span class="text-gray-400">à</span>
              <input type="time" v-model="avail.end_time" class="bg-gray-50 rounded p-1 text-sm outline-none w-24">
              <button type="button" @click="removeAvailability(index)" class="ml-auto text-red-500 hover:text-red-700 p-1">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </div>
            <div v-if="newPost.availabilities.length === 0" class="text-sm text-gray-400 italic">
              Aucun créneau spécifié.
            </div>
          </div>

          <div class="flex gap-3 pt-4">
            <button type="button" @click="showModal = false" class="flex-1 bg-gray-100 text-gray-700 py-3 rounded-xl font-medium hover:bg-gray-200 transition">Annuler</button>
            <button type="submit" class="flex-1 bg-brand text-white py-3 rounded-xl font-medium hover:bg-brand-dark transition shadow-sm">Publier</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>