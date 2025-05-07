import { ref } from "vue";
import { BASE_URL } from "@/constants";
import { useUserStore } from "@/stores/user";

interface Review {
  id: number;
  user_id: number;
  rating: number;
  comment: string;
  updateAt: string;
  isOwner: boolean;
}

interface Reaction {
  id: number;
  user_id: number;
}

interface UserInfo {
  name: string;
  avatarUrl: string;
}

export const useReviews = (toiletId: number) => {
  const reviews = ref<Review[]>([]);
  const reactions = ref<Record<number, Reaction[]>>({});
  const userInfoMap = ref<Record<number, UserInfo>>({});

  const user = useUserStore();
  const toast = useToast();

  const fetchUserInfo = async (userId: number) => {
    if (userInfoMap.value[userId]) return;
    try {
      const res = await fetch(`${BASE_URL}/users/${userId}`);
      const data = await res.json();
      userInfoMap.value[userId] = {
        name: data.name,
        avatarUrl: data.avatarUrl,
      };
    } catch (err) {
      console.warn(`❌ 無法取得使用者 ${userId} 資訊`, err);
    }
  };

  const fetchReactionsByReview = async (reviewId: number) => {
    try {
      const res = await fetch(`${BASE_URL}/reactions/review/${reviewId}`);
      if (!res.ok) throw new Error("無法取得 reaction");
      const data = await res.json();
      reactions.value[reviewId] = data;
    } catch (err) {
      console.error(`❌ reaction 載入失敗（review ${reviewId}）`, err);
    }
  };

  const fetchReviews = async () => {
    try {
      const res = await fetch(`${BASE_URL}/reviews/toilet/${toiletId}`);
      if (!res.ok) throw new Error("無法取得評論");
      const fetched = await res.json();
      reviews.value = fetched.map(
        (review: { id: number; user_id: number | null }) => {
          if (review.user_id && !userInfoMap.value[review.user_id]) {
            fetchUserInfo(review.user_id);
          }
          fetchReactionsByReview(review.id);
          return {
            ...review,
            isOwner: review.user_id === user.id,
          };
        },
      );
    } catch (err) {
      console.error("❌ 評論載入失敗", err);
    }
  };

  const toggleReaction = async (reviewId: number) => {
    const existingList = reactions.value[reviewId] || [];
    const existing = existingList.find((r) => r.user_id === user.id);

    try {
      if (existing) {
        const res = await fetch(`${BASE_URL}/reactions/${existing.id}`, {
          method: "DELETE",
        });
        if (!res.ok) throw new Error("取消失敗");
        reactions.value[reviewId] = existingList.filter(
          (r) => r.id !== existing.id,
        );
      } else {
        const res = await fetch(`${BASE_URL}/reactions/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            review_id: reviewId,
            user_id: user.id,
            is_liked: true,
          }),
        });
        if (!res.ok) throw new Error("送出失敗");
        const newReaction = await res.json();
        reactions.value[reviewId] = [...existingList, newReaction];
      }
    } catch (err) {
      toast.add({ title: "Reaction 更新失敗", color: "error" });
    }
  };

  const hasReacted = (reviewId: number) => {
    return (reactions.value[reviewId] || []).some((r) => r.user_id === user.id);
  };

  const reactionCount = (reviewId: number) => {
    return reactions.value[reviewId]?.length || 0;
  };

  return {
    reviews,
    reactions,
    userInfoMap,
    fetchReviews,
    fetchUserInfo,
    fetchReactionsByReview,
    toggleReaction,
    hasReacted,
    reactionCount,
  };
};
