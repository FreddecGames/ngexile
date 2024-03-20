<script setup>

    import { storeToRefs } from 'pinia'
    import { useGameStore } from '~/store/store.js'

    const store = useGameStore()

    try {
    
        const { data } = await useFetch('https://ngexile.freddecgames.com/api/init', {
            method: 'get',
        })
        console.log(data)
    }
    catch (error) {
    
        console.error(error)
    }
    
</script>

<template>

    <NuxtLayout>
        <NuxtPage />
    </NuxtLayout>
    
</template>
