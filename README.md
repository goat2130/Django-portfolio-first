# __Django-portfolio-first__
## portforio's idea 掲示板
#### 未経験エンジニア転職を望む全てのユーザーが支え合える環境を

<img width="1440" alt="スクリーンショット 2023-06-08 20 59 31" src="https://github.com/goat2130/Django-portfolio-first/assets/124475744/af8af353-cc8e-4624-99af-6e21309a7d51">


## 目次
- [Demo](#Demo)
- [Features](#Features)
- [Usage](#Usage)
- [Requirement](#Requirement)
- [Installation](#Installation)
- [Note](#Note)
- [Autnor](#Author)

 
## Demo
 
## 私自身未経験エンジニア転職をする時、ポートフォリオで何を作るか非常に悩みました。
## 何も知らないからこそアイディアを思いつくのはとても苦労すると感じます。
## 未経験エンジニアがお互いに意見を出し合いより良い選択をできるようこのアプリケーションを作りました。
## あなたのお役に立てると嬉しいです！
 
# Features
## 主な機能は以下の通りです。
 
#### 投稿機能
<img width="1440" alt="スクリーンショット 2023-06-08 19 42 13" src="https://github.com/goat2130/Django-portfolio-first/assets/124475744/9134b551-8264-4401-834f-d92f40d57bbe">

#### ログイン、ログアウト機能
<img width="1440" alt="スクリーンショット 2023-06-08 19 40 16" src="https://github.com/goat2130/Django-portfolio-first/assets/124475744/ce8c0c32-f928-49e0-a272-88c3aeb38bc4">

#### フォロー機能
<img width="1440" alt="スクリーンショット 2023-06-08 20 00 42" src="https://github.com/goat2130/Django-portfolio-first/assets/124475744/227c583e-1384-4aa9-9b87-04908d928fb2">
#### コメント機能

#### いいね機能
<img width="1440" alt="スクリーンショット 2023-06-08 19 42 48" src="https://github.com/goat2130/Django-portfolio-first/assets/124475744/b96cf28c-1137-40b5-959e-539296daefc7">

#### ランキング機能

# Usage
 
#### https://github.com/goat2130/Django-portfolio-first.git
#### python manage.py runserver 0.0.0.0:8000 [runserverでサイトを立ち上げます]
 
# Requirement

### *python 3.11.3
### *Django 4.2
### *pip 22.3.1

# Installation

### Docker を利用しました。以下Dockerfile と　Docker-compose.ymlです。

"""
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
"""

"""
version: '3'

services:
  db:
    image: mysql:5.7
    command: mysqld --character-set-server=utf8 --collation-server=utf8_unicode_ci
    volumes:
      - data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: pass
      MYSQL_DATABASE: mysite
      MYSQL_USER: mysiteuser
      MYSQL_PASSWORD: mysiteuserpass
    restart: always

  web:
    build: .
    command: sh -c "sleep 3; python3.6 manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/root/mysite
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  data:
    driver: local

"""


 
# Note
 
## viewsを記録する際、ページをリロードしてもカウントされること
## アカウントの名前が上書きできないこと
 
# Author
 
# * goat2130 
# * 無所属
# * goat2130@icloud.com
 

