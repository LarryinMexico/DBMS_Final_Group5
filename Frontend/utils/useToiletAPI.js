// utils/useToiletAPI.js
import { useAuth } from '@clerk/vue'
import { BASE_URL } from '@/constants'

export function useToiletAPI() {
  const { getToken } = useAuth()

  async function postToilet(toiletData) {
    const token = await getToken.value()
    if (!token) throw new Error('No token found')

    const res = await fetch(`${BASE_URL}/toilets/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(toiletData),
    })

    if (!res.ok) {
      const errText = await res.text()
      throw new Error(`Failed to create toilet: ${res.status} - ${errText}`)
    }

    return await res.json()
  }

  return {
    postToilet,
  }
}
