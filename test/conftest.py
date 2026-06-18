import os
import sys
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(app_dir)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from schemas import Base, Item
from main import app          # FastAPIアプリ
from database import get_db   # dependency injection用の関数


@pytest.fixture()
def session_fixture():
    engine = create_engine(
        url="sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        item1 = Item(name="PC1", price=10000, description="test1", user_id="1")
        item2 = Item(name="PC2", price=10000, description="test2", user_id="2")
        db.add(item1)
        db.add(item2)
        db.commit()
        yield db
    finally:
        db.close()


# ↓ これを追記する
@pytest.fixture()
def client_fixture():
    engine = create_engine(
        url="sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 本番のDBセッションをテスト用に差し替え
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()  # テスト後にリセット