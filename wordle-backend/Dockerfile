# Python 3.9 이미지 기반으로 설정
FROM python:3.9-slim

# MySQL client 및 필요한 툴 설치
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && apt-get clean

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치를 위한 requirements.txt 파일 복사
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/logs

# 애플리케이션 소스 코드를 복사
COPY . .

# Flask 환경변수 설정
ENV FLASK_APP=app.py

# Flask 디버그 모드 설정

# Flask 서버 실행 명령
CMD ["flask", "run", "--host=0.0.0.0", "--port=5555"]

# 컨테이너에서 노출할 포트 설정
EXPOSE 5555
