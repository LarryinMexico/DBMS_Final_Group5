from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import sys
import os

# 將專案根目錄加入 sys.path，確保 app 模組可用
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 匯入資料模型
from app.db.base import Base
from app import models  # 確保 app/models/__init__.py 有導入所有 models

# 印出目前追蹤到的資料表（可選）
print("👀 Base.metadata.tables:", Base.metadata.tables.keys())

# Alembic 設定
config = context.config

# 設定 logging（可選）
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 設定 metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """以 'offline' 模式執行 migration（例如產生 SQL 檔用）"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """以 'online' 模式執行 migration（直接操作資料庫）"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True  # 比較欄位型別變化
        )

        with context.begin_transaction():
            context.run_migrations()


# 根據執行模式選擇 migration 流程
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()