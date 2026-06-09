<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref(null)
const skills = ref([])
const allSkills = ref([])
const loading = ref(true)
const editMode = ref(false)

const editData = ref({
  first_name: '',
  last_name: '',
  field_of_study: ''
})

const newSkill = ref({ skill_id: '', proficiency: 'weak' })

const getToken = () => localStorage.getItem('token')

const fetchData = async () => {
  const token = getToken()
  const headers = { Authorization: `Bearer ${token}` }
  try {
    const [userRes, skillsListRes] = await Promise.all([
      axios.get('/api/users/me', { headers }),
      axios.get('/api/skills')
    ])
    user.value = userRes.data
    skills.value = userRes.data.skills || []
    allSkills.value = skillsListRes.data
    
    // Remplir les données d'édition
    editData.value = {
      first_name: user.value.first_name,
      last_name: user.value.last_name,
      field_of_study: user.value.field_of_study
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const updateProfile = async () => {
  try {
    const token = getToken()
    await axios.put('/api/users/me', editData.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    editMode.value = false
    fetchData()
  } catch (err) {
    console.error(err)
    alert("Erreur lors de la mise à jour du profil.")
  }
}

const handleFileUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  
  if (!file.type.startsWith('image/')) {
    alert("Veuillez sélectionner une image.")
    return
  }

  const reader = new FileReader()
  reader.onload = (event) => {
    const img = new Image()
    img.onload = () => {
      // Redimensionnement à 300x300 max pour éviter d'exploser la DB
      const canvas = document.createElement('canvas')
      const MAX_SIZE = 300
      let width = img.width
      let height = img.height

      if (width > height) {
        if (width > MAX_SIZE) {
          height *= MAX_SIZE / width
          width = MAX_SIZE
        }
      } else {
        if (height > MAX_SIZE) {
          width *= MAX_SIZE / height
          height = MAX_SIZE
        }
      }

      canvas.width = width
      canvas.height = height
      const ctx = canvas.getContext('2d')
      ctx.drawImage(img, 0, 0, width, height)
      
      // Conversion en base64 (qualité 0.8)
      editData.value.profile_photo = canvas.toDataURL('image/jpeg', 0.8)
    }
    img.src = event.target.result
  }
  reader.readAsDataURL(file)
}

const addSkill = async () => {
  if (!newSkill.value.skill_id) return
  try {
    const token = getToken()
    await axios.post('/api/users/me/skills', newSkill.value, {
      headers: { Authorization: `Bearer ${token}` }
    })
    newSkill.value.skill_id = ''
    fetchData()
  } catch (err) {
    console.error(err)
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Mon Profil</h1>
    
    <div v-if="loading" class="animate-pulse bg-white h-64 rounded-3xl"></div>
    
    <div v-else class="space-y-6">
      <div class="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm relative">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold">Informations personnelles</h2>
          <button v-if="!editMode" @click="editMode = true" class="text-brand text-sm font-medium hover:underline">Modifier</button>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-8 items-start">
          
          <!-- Photo de profil -->
          <div class="flex-shrink-0 flex flex-col items-center gap-3">
            <div class="w-32 h-32 rounded-full bg-gray-100 overflow-hidden border-4 border-white shadow-lg flex items-center justify-center relative">
              <img v-if="editMode && editData.profile_photo" :src="editData.profile_photo" class="w-full h-full object-cover" />
              <img v-else-if="!editMode && user.profile_photo" :src="user.profile_photo" class="w-full h-full object-cover" />
              <span v-else class="text-4xl font-bold text-gray-300">
                {{ user.first_name.charAt(0) }}{{ user.last_name.charAt(0) }}
              </span>
              
              <!-- Overlay Edit -->
              <label v-if="editMode" class="absolute inset-0 bg-black/40 flex items-center justify-center cursor-pointer opacity-0 hover:opacity-100 transition-opacity">
                <span class="text-white text-xs font-bold">Changer</span>
                <input type="file" accept="image/*" class="hidden" @change="handleFileUpload" />
              </label>
            </div>
            <p v-if="editMode" class="text-xs text-gray-400 text-center">Format carré<br>Max 1 Mo</p>
          </div>

          <!-- Formulaire / Infos -->
          <div class="flex-grow w-full">
            <form v-if="editMode" @submit.prevent="updateProfile" class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm text-gray-500 mb-1">Prénom</label>
                  <input v-model="editData.first_name" required class="w-full px-4 py-2 bg-gray-50 rounded-xl" />
                </div>
                <div>
                  <label class="block text-sm text-gray-500 mb-1">Nom</label>
                  <input v-model="editData.last_name" required class="w-full px-4 py-2 bg-gray-50 rounded-xl" />
                </div>
              </div>
              <div>
                <label class="block text-sm text-gray-500 mb-1">Filière</label>
                <input v-model="editData.field_of_study" required class="w-full px-4 py-2 bg-gray-50 rounded-xl" />
              </div>
              <div class="flex gap-3 pt-2">
                <button type="button" @click="editMode = false" class="px-6 py-2 bg-gray-100 text-gray-600 rounded-xl hover:bg-gray-200">Annuler</button>
                <button type="submit" class="px-6 py-2 bg-brand text-white rounded-xl hover:bg-brand-dark">Enregistrer</button>
              </div>
            </form>

            <div v-else class="grid grid-cols-2 gap-6 text-gray-700 mt-2">
              <div><span class="text-gray-400 text-sm block mb-1">Prénom</span> <span class="font-medium text-gray-900">{{ user.first_name }}</span></div>
              <div><span class="text-gray-400 text-sm block mb-1">Nom</span> <span class="font-medium text-gray-900">{{ user.last_name }}</span></div>
              <div><span class="text-gray-400 text-sm block mb-1">Email</span> <span class="font-medium text-gray-900">{{ user.email }}</span></div>
              <div><span class="text-gray-400 text-sm block mb-1">Filière</span> <span class="font-medium text-gray-900">{{ user.field_of_study }}</span></div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Mes Compétences</h2>
        
        <form @submit.prevent="addSkill" class="flex gap-4 mb-6">
          <select v-model="newSkill.skill_id" class="flex-1 px-4 py-2 bg-gray-50 rounded-xl border-transparent focus:border-brand focus:ring-0" required>
            <option value="" disabled>Sélectionner une matière...</option>
            <option v-for="s in allSkills" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
          <select v-model="newSkill.proficiency" class="px-4 py-2 bg-gray-50 rounded-xl border-transparent focus:border-brand focus:ring-0">
            <option value="weak">À améliorer (Besoin d'aide)</option>
            <option value="strong">Fort (Je peux aider)</option>
          </select>
          <button type="submit" class="bg-brand text-white px-6 py-2 rounded-xl hover:bg-brand-dark transition-colors">Ajouter</button>
        </form>

        <div class="flex flex-wrap gap-3">
          <div v-for="s in skills" :key="s.skill_id" class="px-4 py-2 rounded-full text-sm font-medium border"
               :class="s.proficiency === 'strong' ? 'bg-green-50 text-green-700 border-green-200' : (s.proficiency === 'weak' ? 'bg-orange-50 text-orange-700 border-orange-200' : 'bg-blue-50 text-blue-700 border-blue-200')">
            {{ s.skill_name }}
          </div>
          <div v-if="skills.length === 0" class="text-gray-400 italic">Aucune compétence ajoutée.</div>
        </div>
      </div>
    </div>
  </div>
</template>