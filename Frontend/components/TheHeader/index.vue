<script setup lang="ts">
import ColorModeButton from './ColorModeButton.vue';
</script>

<template>
  <header class="h-16 border-b px-4 flex items-center justify-between">
    <!-- 左邊：Logo -->
    <NuxtLink to="/" class="text-xl font-bold hover:opacity-80">
      🚽 NCCU Toilet Map
    </NuxtLink>

    <!-- 右邊功能區 -->
    <div class="flex items-center gap-3">
      <!-- 暗色模式切換 -->
      <ColorModeButton />

      <!-- 登入按鈕-->
      <SignedOut>
        <SignInButton mode="modal" afterSignInUrl="/" :appearance="{
          elements: {
            button: 'bg-green-500 hover:bg-green-600 text-white rounded px-3 py-2'
          }
        }">
          <UButton color="secondary" variant="soft" icon="i-lucide-user">登入</UButton>
        </SignInButton>
      </SignedOut>
      <SignedIn>
        <UserButton />
      </SignedIn>
    </div>
  </header>
</template>
