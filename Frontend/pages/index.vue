<script setup>
//TODO: refactor to use `useUser` from `@clerk/vue`
import { BASE_URL } from '@/constants/index.js'
import { useAuth } from '@clerk/vue'

const { user } = useUser()

const { getToken, isSignedIn } = useAuth()

watch(user, async (newUser) => {
    if (!newUser || !isSignedIn) return

    const token = await getToken.value()
    console.log('👤 使用者 token：', token)
    if (!token) return

    try {
        // 📝 嘗試註冊
        console.log(newUser.id, newUser.fullName, newUser.primaryEmailAddress?.emailAddress)
        await fetch(`${BASE_URL}/users`, {
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

        // ✅ 拿自己資料
        const res = await fetch(`${BASE_URL}/users/me`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })

        const data = await res.json()
        console.log('👤 目前使用者：', data)
    } catch (err) {
        console.error('❌ 使用者處理失敗：', err)
    }
})
</script>

<template>
    <TheHeader />
    <TheMap />
</template>