# 베이스 이미지 설정
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY web /app/

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Django 환경 설정
EXPOSE 8000

# 명령어 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

