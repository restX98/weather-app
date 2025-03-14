<script setup lang="ts">
import { ref } from 'vue';
import type { Location } from '@/types';

import SunIcon from '@/assets/icons/1.svg';
import ThunderIcon from '@/assets/icons/2.svg';
import SunCloudIcon from '@/assets/icons/3.svg';
import CloudIcon from '@/assets/icons/4.svg';
import RainSunIcon from '@/assets/icons/5.svg';

const statusIcons: Record<string, string | undefined> = {
  sun: SunIcon,
  'sun-cloud': SunCloudIcon,
  cloud: CloudIcon,
  'rain-sun': RainSunIcon,
  thunder: ThunderIcon,
  unknown: undefined, // no icon
};

const locations = ref<Array<Location>>([]);

const { pending, error } = await useLazyFetch<Array<Location>>('http://localhost:3000/locations', {
    onResponse({ response }) {
        if (response._data) {
            console.log(response);
            locations.value = response._data;
        }
    },
});

const columns = [
    { key: 'name', label: 'Location' },
    { key: 'temperature', label: 'Temperature' },
    { key: 'rain', label: 'Rainfall' },
    { key: 'actions', label: '' },
];

function removeLocation(id: number) {
    locations.value = locations.value.filter((loc) => loc.id !== id);
}

function addLocation() {
    const id = Date.now();
    locations.value.push({
        id,
        name: 'New City',
        temperature: '20°C',
        rain: '0mm',
        status: 'cloud',
    });
}
</script>

<template>
    <div>
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-medium text-white">Locations</h2>
            <UButton icon="i-heroicons-plus" color="white" @click="addLocation"> Add location </UButton>
        </div>

        <UTable
            :loading="pending"
            :loading-state="{ icon: 'i-heroicons-arrow-path-20-solid', label: 'Loading...' }"
            :progress="{ color: 'primary', animation: 'carousel' }"
            :rows="locations"
            :columns="columns"
            class="bg-zinc-700"
        >
            <template #name-data="{ row }">
                <div class="flex items-center gap-2">
                    <img
                        v-if="statusIcons[row.status || 'unknown']"
                        :src="statusIcons[row.status || 'unknown']"
                        alt="status icon"
                        class="w-5 h-5"
                    />
                    <span class="text-white">{{ row.name }}</span>
                </div>
            </template>
            <template #actions-data="{ row }">
                <UButton color="#323232" variant="ghost" icon="i-heroicons-trash" @click="() => removeLocation(row.id)" />
            </template>
        </UTable>
    </div>
</template>
