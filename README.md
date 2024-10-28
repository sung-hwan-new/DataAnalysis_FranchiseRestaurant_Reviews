# 홍콩반점0410 LLM 리뷰 분석을 통한 위기 대응 전략 제안

![image](https://github.com/user-attachments/assets/81c2115e-a320-43e6-9fe2-cbe364ff576c)

### 목적
최근 ‘백종원 PAIK JONG WON’ 유튜브 채널의 '내꺼내먹 홍콩반점0410' 관련 영상 조회수가 약 1천만회에 이를 정도로 많은 관심이 쏠렸습니다. 홍콩반점0410은 지점마다 맛이 다르다는 지적을 오랫동안 받았기 때문입니다. 그래서 주요 사이트 약 3만개 리뷰를 OpenAI로 긍정/부정을 판단하고, Tf-idf를 통한 최빈 단어 추출로 문제의 원인을 정량적으로 파악하여 대응 전략을 수립했습니다.

### 개요
- 매장 정보 / Review Crawling
  - 홍콩반점0410 서울 소재 지점(90건)
  - 네이버지도(26,192건), 구글맵(4,824건), 카카오맵(1,697건)
- 댓글 Crawling
  - ‘백종원 PAIK JONG WON’ 유튜브 채널 주요 영상 댓글(1,130건)
- ChatGPT API를 통한 긍정/부정 리뷰 판단
- TF-idf / Word2Vec를 통한 키워드 분석
- '점바점' 개선을 위한 해결책 제안
  - 지점 맛/서비스 개선을 위한 서바이벌 프로그램 기획

### 세부 내용
[<img src="https://img.shields.io/badge/Velog-1EBC8F?style=for-the-badge&logo=velog&logoColor=white" />](https://velog.io/@sung_hwan_new/hongkong)
