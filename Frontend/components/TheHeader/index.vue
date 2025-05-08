<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import ColorModeButton from "./ColorModeButton.vue";
import AddToiletButton from "./AddToiletButton.vue";
import Profile from "./Profile/index.vue";

const userStore = useUserStore();
const showProfile = ref(false);
</script>

<template>
  <header class="h-16 border-b px-4 flex items-center justify-between">
    <!-- Logo -->
    <NuxtLink to="/" class="text-xl font-bold hover:opacity-80">
      🚽 NCCU Toilet Map
    </NuxtLink>

    <!-- 功能列 -->
    <div class="flex items-center gap-3">
      <!-- 個人資料（帶入使用者 ID）-->

      <div class="flex items-center gap-3">
        <UButton
          icon="i-heroicons-user-circle"
          label="個人資料"
          size="md"
          variant="soft"
          color="info"
          @click="showProfile = true"
        />

        <UModal v-model:open="showProfile">
          <template #content>
        <Profile
          :userId="userStore.id?.toString() || ''"
          @close="showProfile = false"
          />
      </template>
        </UModal>
      </div>
      <AddToiletButton />
      <ColorModeButton />

      <!-- 登入/登出 -->
      <SignedOut>
        <SignInButton
          mode="modal"
          afterSignInUrl="/"
          :appearance="{
            elements: {
              button:
                'bg-green-500 hover:bg-green-600 text-white rounded px-3 py-2',
            },
          }"
        >
          <UButton color="secondary" variant="soft" icon="i-lucide-user">
            登入
          </UButton>
        </SignInButton>
      </SignedOut>
      <SignedIn>
        <UserButton />
      </SignedIn>
    </div>
  </header>
</template>
