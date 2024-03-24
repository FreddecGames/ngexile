export default defineNuxtConfig({
    
    ssr: true,
    
    devtools: { enabled: false },
    
    app: {
        head: {
            title: 'FG Exile',
            meta: [
                { charset: 'utf-8' },
                { name: 'viewport', content: 'width=device-width, initial-scale=1' },
                { hid: 'description', name: 'description', content: '' },
            ],
            link: [
                { rel: 'icon', href: '/logo.png' },
            ],
        },
    },
    
    css: [ 'bootstrap/dist/css/bootstrap.min.css', '@fortawesome/fontawesome-svg-core/styles.css', '@/styles/main.css' ],
    
    modules: [ '@pinia/nuxt', '@nuxtjs/i18n', ],
    
    i18n: {
        lazy: true,
        legacy: false,
        langDir: 'locales',
        defaultLocale: 'en',
        detectBrowserLanguage: {            
            useCookie: true,
            redirectOn: 'root',
            fallbackLocale: 'en',
        },
        locales: [
            { code:'en', file:'en.json',  },
        ],
    },
})
