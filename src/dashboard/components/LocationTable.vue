<script setup lang="ts">
import { ref } from 'vue';
import type { Location } from '@/types';

const locations = ref<Array<Location>>([
    { id: 1, location: 'Rome', temperature: '23°C', rainfall: '12mm' },
    { id: 2, location: 'Dublin', temperature: '17°C', rainfall: '35mm' },
    { id: 3, location: 'Madrid', temperature: '29°C', rainfall: '5mm' },
]);

const columns = [
    { key: 'location', label: 'Location' },
    { key: 'temperature', label: 'Temperature' },
    { key: 'rainfall', label: 'Rainfall' },
    { key: 'actions', label: '' },
];

function removeLocation(id: number) {
    locations.value = locations.value.filter((loc) => loc.id !== id);
}

function addLocation() {
    const id = Date.now();
    locations.value.push({
        id,
        location: 'New City',
        temperature: '20°C',
        rainfall: '0mm',
    });
}
</script>

<template>
    <div>
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-medium text-white">Locations</h2>
            <UButton icon="i-heroicons-plus" color="white" @click="addLocation"> Add location </UButton>
        </div>

        <UTable :rows="locations" :columns="columns" class="bg-zinc-700">
            <template #actions-data="{ row }">
                <UButton color="#323232" variant="ghost" icon="i-heroicons-trash" @click="removeLocation(row.id)" />
            </template>
        </UTable>
    </div>
</template>
