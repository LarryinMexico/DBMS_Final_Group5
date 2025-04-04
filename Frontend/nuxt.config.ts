// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxt/ui','@clerk/nuxt'],
  css: ['~/assets/css/tailwind.css', 'mapbox-gl/dist/mapbox-gl.css'],
})