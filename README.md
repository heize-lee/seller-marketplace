# seller-marketplace

Seller Marketplace는 판매자와 구매자를 위한 이커머스 플랫폼입니다. 사용자는 상품을 등록하고, 관리하며, 구매할 수 있습니다.
프로젝트는 Django를 기반으로 개발되었습니다.

## 업무 분담

| 팀원       | 역할                                                                                                                                                               |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **이지현** | 프로젝트 관리, 코드 리뷰, `accounts` 앱 (회원가입, 탈퇴, 로그인, 회원 정보 수정, 프로필 이미지 수정), 배포                                                         |
| **박정현** | `products` 앱 (상품 등록, 수정, 삭제, 목록 조회, 상세 조회, 제품 검색 및 필터링, 카테고리 관리)                                                                    |
| **박룡**   | `orders` 앱 (판매 중인 물건 구매, 주문 생성 및 결제 처리, 주문 내역 조회, 장바구니, 구매 이력 조회)                                                                |
| **문회성** | `reviews` 앱 + `products` 앱 지원 (리뷰 CRUD, 평점, 조회 및 필터링, 제품 검색 및 필터링, 카테고리 관리, 좋아요, 팔로우, 특정 구매자에게만 공개, 새 상품 알림 기능) |
| **윤재웅** | `accounts` 앱 (유저 프로필 이미지 수정, 좋아요, 팔로우), `orders` 앱 (구매 이력 조회)                                                                              |
