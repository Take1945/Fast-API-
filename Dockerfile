
FROM python:3.12-slim

WORKDIR /app

# FastAPIとUvicorn（標準パック）をインストール
RUN pip install --no-cache-dir fastapi[standard]

# 1. 依存関係パッケージ（requirements.txt）をコピー
COPY requirements.txt .

# 2. requirements.txt に書かれたライブラリを一括インストール（ここを修正）
RUN pip install --no-cache-dir -r requirements.txt

# ローカルのソースコードをコンテナ内にコピー
COPY . .

# Uvicornサーバーを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
