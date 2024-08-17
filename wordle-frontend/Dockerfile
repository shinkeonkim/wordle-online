# Node.js를 기반으로 하는 이미지를 사용
FROM node:16-alpine

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 파일들을 복사하고, 의존성을 설치
COPY package.json ./
COPY yarn.lock ./
RUN yarn install

# 애플리케이션 소스 코드를 복사
COPY . .

# React 애플리케이션을 빌드
RUN yarn build

# 빌드된 애플리케이션을 서빙하기 위해 serve 패키지를 설치
RUN yarn global add serve

# 컨테이너가 시작될 때 빌드된 애플리케이션을 서빙
CMD ["serve", "-s", "build"]

# 컨테이너에서 노출될 포트를 설정
EXPOSE 3000
