<script setup lang="ts">
import Header from '@/components/Header.vue';
import LocationTable from '@/components/LocationTable.vue';

definePageMeta({
    colorMode: 'light',
});
</script>


<template>
    <div class="min-h-screen bg-zinc-900 py-4 px-20">
        <Header />

        <LocationTable />
    </div>
</template>