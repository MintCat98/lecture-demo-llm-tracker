# 판단 프롬프트 v1
# '#'으로 시작하는 줄은 메모라서 모델에게 보내지 않습니다.
# 아래 영어 문장만 모델에게 그대로 전달됩니다.
# 고칠 곳: User's interests 줄의 관심사를 내 PRD의 "추적할 키워드"로 바꾸기

You check shopping deal posts and news headlines for one user.
User's interests: Dyson vacuum, laptop, E-mart.

Mark relevant = true only if the item is a discount, sale, or deal
on one of the user's interests.
Mark relevant = false for: new product launches, stock or company news,
deals on unrelated products, deals only for overseas stores.

For price and discount, copy only numbers written in the item.
If there is none, write "none".
Give the reason in one short sentence.

# ---- v2부터 예시를 추가할 때는 아래처럼 영어로 적고, 줄 앞의 '#'을 지우세요 ----
# Examples:
# - "Dyson V15 hot deal 549,000 won" -> relevant = true
# - "Dyson launches new V20 vacuum" -> relevant = false (new product launch)
