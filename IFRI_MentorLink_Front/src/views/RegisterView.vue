<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone_number: '',
  password: '',
  field_of_study: 'Génie Logiciel',
  level: 'Licence 1'
})

const errorMsg = ref('')
const loading = ref(false)

const handleRegister = async () => {
  errorMsg.value = ''
  loading.value = true
  
  try {
    const res = await axios.post('/api/auth/register', form.value)
    localStorage.setItem('token', res.data.access_token)
    router.push('/dashboard')
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      errorMsg.value = err.response.data.detail
    } else {
      errorMsg.value = "Erreur lors de l'inscription."
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex justify-center items-center py-12 px-4">
    <div class="w-full max-w-xl bg-white rounded-3xl shadow-xl shadow-gray-200/50 p-8 border border-gray-100">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-2">Rejoignez-nous ✨</h2>
        <p class="text-gray-500">Créez votre compte IFRI MentorLink.</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="space-y-5">
        <div v-if="errorMsg" class="bg-red-50 text-red-600 p-3 rounded-xl text-sm text-center">
          {{ errorMsg }}
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Prénom</label>
            <input v-model="form.first_name" type="text" required class="w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:border-brand focus:bg-white focus:ring-0 transition-colors">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Nom</label>
            <input v-model="form.last_name" type="text" required class="w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:border-brand focus:bg-white focus:ring-0 transition-colors">
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Email étudiant</label>
          <input v-model="form.email" type="email" required class="w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:border-brand focus:bg-white focus:ring-0 transition-colors">
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Filière</label>
            <select v-model="form.field_of_study" class="w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:border-brand focus:bg-white focus:ring-0 transition-colors appearance-none">
              <option value="Génie Logiciel">Génie Logiciel</option>
              <option value="Sécurité Informatique">Sécurité Informatique</option>
              <option value="Intelligence Artificielle">Intelligence Artificielle</option>
              <option value="Système Embarqué et Internet des Objets">Système Embarqué et Internet des Objets</option>
              <option value="Internet et Multimédia">Internet et Multimédia</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Niveau</label>
            <select v-model="form.level" class="w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:border-brand focus:bg-white focus:ring-0 transition-colors appearance-none">
              <option value="Licence 1">Licence 1</option>
              <option value="Licence 2">Licence 2</option>
              <option value="Licence 3">Licence 3</option>
              <option value="Master 1">Master 1</option>
              <option value="Master 2">Master 2</option>
            </select>
          </div>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Téléphone</label>
            <input v-model="form.phone_number" type="text" class="w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:border-brand focus:bg-white focus:ring-0 transition-colors">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Mot de passe</label>
            <input v-model="form.password" type="password" required class="w-full px-4 py-3 rounded-xl bg-gray-50 border-transparent focus:border-brand focus:bg-white focus:ring-0 transition-colors">
          </div>
        </div>
        
        <button type="submit" :disabled="loading" class="w-full bg-brand hover:bg-brand-dark text-white py-3.5 rounded-xl font-medium shadow-md shadow-blue-500/20 transition-all disabled:opacity-70 mt-4 flex justify-center items-center">
           <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          {{ loading ? 'Création en cours...' : "S'inscrire" }}
        </button>
      </form>
      
      <div class="mt-8 text-center text-sm text-gray-500">
        Déjà un compte ? 
        <router-link to="/login" class="text-brand font-medium hover:underline">Se connecter</router-link>
      </div>
    </div>
  </div>
</template>