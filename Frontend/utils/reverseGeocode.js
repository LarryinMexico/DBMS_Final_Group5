const MAPBOX_TOKEN = 'pk.eyJ1IjoiY2h1YW5nMDkxIiwiYSI6ImNtOTE3NTZldzB2cWYyanNraGh1dGkzdzMifQ.IqUIwZ1dEf7Prbnb4bMeng'

/**
 * 透過 Mapbox API 進行反向地理編碼，取得地址名稱
 * @param {{ lat: number, lng: number }} location
 * @returns {Promise<string|null>} 地址文字（或 null）
 */
export async function reverseGeocode( { lat, lng }) {
  try {
    console.log('🔍 Reverse geocode:', { lat, lng })
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?access_token=${MAPBOX_TOKEN}&language=zh-Hant`

    const res = await fetch(url)
    const data = await res.json()
    console.log('🔍 Reverse geocode response:', data)

    const place = data?.features?.[0]?.place_name
    return place ?? null
  } catch (err) {
    console.error('❌ Reverse geocode error:', err)
    return null
  }
}
