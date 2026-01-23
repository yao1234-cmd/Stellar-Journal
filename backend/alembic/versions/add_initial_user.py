"""add initial user

Revision ID: initial_user_001
Revises: 7fe88b5fc215
Create Date: 2026-01-21

"""
from alembic import op
import sqlalchemy as sa
import os

# revision identifiers
revision = 'initial_user_001'
down_revision = '7fe88b5fc215'
branch_labels = None
depends_on = None


def upgrade():
    """创建初始占位用户（用于数据库结构完整性）"""
    # 注意：此迁移不应再用于创建测试/开发用户
    # 开发环境的种子数据请使用 backend/scripts/seed_dev_user.py
    pass


def downgrade():
    """回滚初始用户创建"""
    pass
