"""add initial user

Revision ID: initial_user_001
Revises: 7fe88b5fc215
Create Date: 2026-01-21

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'initial_user_001'
down_revision = '7fe88b5fc215'
branch_labels = None
depends_on = None


def upgrade():
    """创建初始用户"""
    # 使用 op.execute 插入初始用户
    op.execute(
        """
        INSERT INTO users (id, username, email, created_at, updated_at)
        VALUES (
            '00000000-0000-0000-0000-000000000001'::uuid,
            'temp_user',
            'temp@example.com',
            NOW(),
            NOW()
        )
        ON CONFLICT (id) DO NOTHING;
        """
    )


def downgrade():
    """删除初始用户"""
    op.execute(
        """
        DELETE FROM users 
        WHERE id = '00000000-0000-0000-0000-000000000001'::uuid;
        """
    )
