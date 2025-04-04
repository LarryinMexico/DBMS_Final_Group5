<script setup>
import { BASE_URL } from '@/constants/index.js'
import { useAuth, useUser } from '@clerk/vue'
import { watch } from 'vue'

const { user } = useUser()
const { getToken, isSignedIn } = useAuth()

watch(user, async (newUser) => {
  if (!newUser || !isSignedIn.value) return

    const token = await getToken.value()
    console.log('👤 使用者 token：', token)
    if (!token) return

  try {
    // ✅ 先嘗試 GET 自己資料
    const res = await fetch(`api/users/me`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (res.status === 404) {
      // ❌ 未註冊 → 執行 POST 註冊
      console.log('🆕 尚未註冊，用戶 ID:', newUser.id)

      const postRes = await fetch(`api/users`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          clerk_id: newUser.id,
          name: newUser.fullName,
          email: newUser.primaryEmailAddress?.emailAddress
        })
      })

      if (!postRes.ok) throw new Error('無法註冊使用者')
      console.log('✅ 已成功註冊')
    } else if (res.ok) {
      const userData = await res.json()
      console.log('👤 目前使用者：', userData)
    } else {
      throw new Error(`❌ 無法取得使用者資料，狀態碼 ${res.status}`)
    }
  } catch (err) {
    console.error('❌ 使用者處理失敗：', err)
  }
})
</script>

<template>
  <TheHeader />
  <TheMap />
</template>
