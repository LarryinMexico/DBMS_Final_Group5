// utils/useUserRegister.js
import { watch } from "vue";
import { useUser, useAuth } from "@clerk/vue";
import { BASE_URL } from "@/constants";
import { useUserStore } from "@/stores/userStore";

export function useUserRegister() {
  const { user } = useUser();
  const { getToken, isSignedIn } = useAuth();
  const userStore = useUserStore();

  watch(user, async (newUser) => {
    if (!newUser || !isSignedIn.value) return;

    const token = await getToken.value();
    if (!token) return;

    try {
      // 先嘗試 GET 自己資料
      const res = await fetch(`${BASE_URL}/users/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.status === 404) {
        // 尚未註冊，執行 POST 註冊

        const postRes = await fetch(`${BASE_URL}/users/`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            clerk_id: newUser.id,
            name: newUser.fullName,
            email: newUser.primaryEmailAddress?.emailAddress,
            avatarUrl: newUser.imageUrl,
          }),
        });

        if (!postRes.ok) throw new Error("無法註冊使用者");

        const userData = await postRes.json();
        userStore.setUser({ ...userData, avatar: newUser.imageUrl });
      } else if (res.ok) {
        const userData = await res.json();
        userStore.setUser({ ...userData, avatar: user.value.imageUrl });
      } else {
        throw new Error(`❌ 無法取得使用者資料，狀態碼 ${res.status}`);
      }
    } catch (err) {
      console.error("❌ 使用者處理失敗：", err);
    }
  });
}
