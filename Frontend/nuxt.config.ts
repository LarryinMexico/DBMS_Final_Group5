// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxt/ui','@clerk/nuxt','@pinia/nuxt'],
  css: ['~/assets/css/tailwind.css', 'mapbox-gl/dist/mapbox-gl.css'],
  app: {
    rootAttrs: {
      'data-vaul-drawer-wrapper': '',
      'class': 'bg-default'
    }
  }
})