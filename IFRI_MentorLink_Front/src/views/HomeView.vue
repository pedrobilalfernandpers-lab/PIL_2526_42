<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Fonctionnalités principales
const stats = [
  { value: '100%', label: 'Gratuit pour les étudiants' },
  { value: '24/7', label: 'Accès à la plateforme' },
  { value: '1', label: 'Seul but : Votre réussite' }
]

// Intersection Observer pour les animations au scroll
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-reveal')
      }
    })
  }, {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
  })

  document.querySelectorAll('.reveal-on-scroll').forEach((el) => {
    observer.observe(el)
  })
})
</script>

<template>
  <div class="bg-gray-50/50 selection:bg-brand selection:text-white overflow-hidden">
    
    <!-- Hero Section -->
    <div class="relative pt-24 pb-32">
      <!-- Background Elements -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[800px] bg-gradient-to-b from-brand/10 to-transparent pointer-events-none blur-3xl"></div>
      
      <!-- Decorative circles -->
      <div class="absolute top-20 left-10 w-64 h-64 bg-blue-400/20 rounded-full blur-3xl animate-blob"></div>
      <div class="absolute top-40 right-10 w-64 h-64 bg-purple-400/20 rounded-full blur-3xl animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-20 left-1/2 w-64 h-64 bg-brand/20 rounded-full blur-3xl animate-blob animation-delay-4000"></div>

      <div class="max-w-7xl mx-auto px-4 relative z-10 text-center reveal-on-scroll delay-100">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-50/80 backdrop-blur text-brand text-sm font-semibold mb-8 border border-blue-100 shadow-sm transition-transform hover:scale-105 cursor-default">
          <span class="w-2 h-2 rounded-full bg-brand animate-ping"></span>
          L'excellence IFRI, par les étudiants
        </div>
        
        <h1 class="text-6xl md:text-8xl font-black text-gray-900 tracking-tight mb-8 leading-[1.1]">
          L'entraide académique,<br/>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand via-blue-600 to-purple-600 animate-gradient">réinventée.</span>
        </h1>
        
        <p class="text-xl md:text-2xl text-gray-500 max-w-3xl mx-auto mb-12 leading-relaxed font-light">
          Débloquez votre potentiel. Trouvez le mentor idéal, partagez vos connaissances et progressez ensemble vers la réussite.
        </p>
        
        <div class="flex flex-col sm:flex-row gap-5 justify-center items-center">
          <button @click="router.push('/register')" class="w-full sm:w-auto bg-brand text-white px-10 py-4 rounded-full text-lg font-bold shadow-xl shadow-blue-500/30 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl hover:bg-brand-dark group">
            Rejoindre l'aventure
            <span class="inline-block transition-transform duration-300 group-hover:translate-x-2">→</span>
          </button>
          <button @click="router.push('/login')" class="w-full sm:w-auto bg-white/80 backdrop-blur hover:bg-white text-gray-700 border-2 border-gray-200 px-10 py-4 rounded-full text-lg font-bold transition-all duration-300 shadow-sm hover:border-gray-300 hover:-translate-y-1">
            Se connecter
          </button>
        </div>
      </div>
    </div>

    <!-- Stats Section -->
    <div class="border-y border-gray-200/60 bg-white/50 backdrop-blur reveal-on-scroll">
      <div class="max-w-7xl mx-auto px-4 py-12">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-gray-200">
          <div v-for="stat in stats" :key="stat.value" class="pt-8 md:pt-0">
            <div class="text-4xl md:text-5xl font-black text-brand mb-2">{{ stat.value }}</div>
            <div class="text-gray-500 font-medium tracking-wide uppercase text-sm">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- About Us Section -->
    <div class="py-32 relative reveal-on-scroll delay-200">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex flex-col lg:flex-row items-center gap-16">
          <div class="lg:w-1/2 relative">
            <div class="absolute inset-0 bg-gradient-to-tr from-brand to-purple-600 rounded-3xl transform -rotate-3 scale-105 opacity-20"></div>
            <img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" alt="Students studying together" class="rounded-3xl shadow-2xl relative z-10 w-full object-cover aspect-square md:aspect-[4/3] border-8 border-white" />
            
            <!-- Badge flottant -->
            <div class="absolute -bottom-8 -right-8 bg-white p-6 rounded-2xl shadow-xl z-20 animate-float border border-gray-100 hidden md:block">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                </div>
                <div>
                  <div class="font-bold text-gray-900">Entraide 100%</div>
                  <div class="text-sm text-gray-500">Garantie</div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="lg:w-1/2">
            <h2 class="text-sm font-bold text-brand uppercase tracking-widest mb-3">À propos de nous</h2>
            <h3 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6 leading-tight">Pour les étudiants,<br/>Par les étudiants.</h3>
            <p class="text-lg text-gray-600 mb-6 leading-relaxed">
              L'Institut de Formation et de Recherche en Informatique (IFRI) rassemble des esprits brillants. Mais parfois, un concept bloque, un projet coince. C'est là que MentorLink intervient.
            </p>
            <p class="text-lg text-gray-600 mb-8 leading-relaxed">
              Notre mission est de casser les barrières académiques en créant un réseau de solidarité. Ceux qui maîtrisent un sujet aident ceux qui ont des difficultés. Tout simplement.
            </p>
            <ul class="space-y-4">
              <li class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-brand-light flex items-center justify-center text-brand flex-shrink-0">✓</div>
                <span class="text-gray-700 font-medium">Développé dans le cadre du Projet Intégrateur</span>
              </li>
              <li class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-brand-light flex items-center justify-center text-brand flex-shrink-0">✓</div>
                <span class="text-gray-700 font-medium">Pensé exclusivement pour les filières de l'IFRI</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Deep Dive Features -->
    <div class="py-32 bg-gray-900 text-white relative overflow-hidden">
      <!-- Noise texture -->
      <div class="absolute inset-0 opacity-5 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')]"></div>
      
      <div class="max-w-7xl mx-auto px-4 relative z-10">
        <div class="text-center mb-24 reveal-on-scroll">
          <h2 class="text-sm font-bold text-brand-light uppercase tracking-widest mb-3">Fonctionnalités</h2>
          <h3 class="text-4xl md:text-5xl font-bold mb-6">Tout ce dont vous avez besoin.</h3>
        </div>

        <!-- Feature 1 -->
        <div class="flex flex-col md:flex-row items-center gap-16 mb-32 reveal-on-scroll">
          <div class="md:w-1/2 order-2 md:order-1">
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-brand flex items-center justify-center mb-6 shadow-lg shadow-brand/30">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
            </div>
            <h4 class="text-3xl font-bold mb-4">Le Mur d'Annonces</h4>
            <p class="text-gray-400 text-lg leading-relaxed">
              Consultez les offres de mentorat ou publiez vos propres demandes d'aide. Le mur centralise tous les besoins de la communauté en temps réel. Filtrez par matière (Python, Algo, IA, etc.) et trouvez chaussure à votre pied en un clic.
            </p>
          </div>
          <div class="md:w-1/2 order-1 md:order-2 w-full">
            <div class="bg-gray-800 rounded-3xl p-4 border border-gray-700 shadow-2xl transform md:rotate-3 transition-transform hover:rotate-0 duration-500">
              <div class="bg-gray-900 rounded-2xl aspect-video p-6 flex flex-col gap-4">
                <div class="w-1/3 h-4 bg-gray-700 rounded-full mb-4"></div>
                <div class="bg-gray-800 p-4 rounded-xl border border-gray-700"><div class="w-24 h-4 bg-blue-500/50 rounded mb-2"></div><div class="w-full h-2 bg-gray-700 rounded mb-1"></div><div class="w-2/3 h-2 bg-gray-700 rounded"></div></div>
                <div class="bg-gray-800 p-4 rounded-xl border border-gray-700"><div class="w-24 h-4 bg-purple-500/50 rounded mb-2"></div><div class="w-full h-2 bg-gray-700 rounded mb-1"></div><div class="w-1/2 h-2 bg-gray-700 rounded"></div></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 2 -->
        <div class="flex flex-col md:flex-row items-center gap-16 reveal-on-scroll">
          <div class="md:w-1/2 w-full">
            <div class="bg-gray-800 rounded-3xl p-4 border border-gray-700 shadow-2xl transform md:-rotate-3 transition-transform hover:rotate-0 duration-500">
              <div class="bg-gray-900 rounded-2xl aspect-video flex overflow-hidden">
                <div class="w-1/3 border-r border-gray-800 p-4 flex flex-col gap-3">
                   <div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full bg-gray-700"></div><div class="flex-1 h-3 bg-gray-700 rounded"></div></div>
                   <div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full bg-blue-500"></div><div class="flex-1 h-3 bg-gray-700 rounded"></div></div>
                </div>
                <div class="flex-1 p-4 flex flex-col justify-end gap-2">
                  <div class="bg-gray-800 w-2/3 self-start p-3 rounded-2xl rounded-tl-sm h-12"></div>
                  <div class="bg-brand w-2/3 self-end p-3 rounded-2xl rounded-tr-sm h-12"></div>
                </div>
              </div>
            </div>
          </div>
          <div class="md:w-1/2">
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center mb-6 shadow-lg shadow-purple-500/30">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
            </div>
            <h4 class="text-3xl font-bold mb-4">La Messagerie Privée</h4>
            <p class="text-gray-400 text-lg leading-relaxed">
              Une fois que vous répondez à une annonce, un Match est créé. Une conversation sécurisée s'ouvre pour vous permettre d'organiser vos sessions d'études, d'échanger des liens ou des fichiers, sans quitter la plateforme.
            </p>
          </div>
        </div>

      </div>
    </div>

    <!-- CTA Section -->
    <div class="py-32 relative overflow-hidden text-center reveal-on-scroll">
      <div class="absolute inset-0 bg-gradient-to-br from-brand to-purple-700"></div>
      <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
      <div class="relative z-10 max-w-4xl mx-auto px-4">
        <h2 class="text-5xl md:text-6xl font-black text-white mb-8">Ne restez pas bloqué sur vos cours.</h2>
        <p class="text-blue-100 text-2xl mb-12 max-w-2xl mx-auto font-light">Le mentorat, c'est l'assurance d'apprendre plus vite, et de consolider ses propres acquis.</p>
        <button @click="router.push('/register')" class="bg-white text-brand px-12 py-5 rounded-full text-xl font-bold shadow-2xl transition-all duration-300 hover:scale-105 hover:shadow-[0_0_40px_rgba(255,255,255,0.3)]">
          Commencer maintenant — c'est gratuit
        </button>
      </div>
    </div>
    
    <!-- Footer -->
    <footer class="bg-gray-950 py-16 border-t border-gray-900">
      <div class="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-brand rounded-lg flex items-center justify-center text-white font-bold">M</div>
          <span class="text-white font-bold text-xl tracking-tight">MentorLink <span class="text-gray-500 font-normal">IFRI</span></span>
        </div>
        <p class="text-gray-500">© 2026 IFRI MentorLink. Projet Intégrateur 2526_42.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* Classes pour l'Intersection Observer */
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 1s cubic-bezier(0.16, 1, 0.3, 1), transform 1s cubic-bezier(0.16, 1, 0.3, 1);
}

.animate-reveal {
  opacity: 1;
  transform: translateY(0);
}

/* Utilitaires de délai */
.delay-100 { transition-delay: 100ms; }
.delay-200 { transition-delay: 200ms; }
.delay-300 { transition-delay: 300ms; }

/* Animations CSS complexes */
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.animate-gradient {
  background-size: 200% auto;
  animation: gradient 4s linear infinite;
}
</style>