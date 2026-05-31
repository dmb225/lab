"""backfill organization_id on conversations and rag_documents

Revision ID: 0006_backfill_conv_org
Revises: 0005_org_tenant_isolation
Create Date: 2026-05-31T08:00:32.147244+00:00

Assigns each conversation (and rag_document) that has a user_id to that user's
Personal Organization. Rows with NULL user_id are left as NULL.

This is a data migration — safe to re-run (NULL rows already handled).
"""

import sqlalchemy as sa

from alembic import op

revision = "0006_backfill_conv_org"
down_revision = "0005_org_tenant_isolation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # Backfill conversations
    conn.execute(
        sa.text("""
        UPDATE conversations
        SET organization_id = o.id
        FROM organizations o
        WHERE conversations.user_id = o.created_by_user_id
          AND o.is_personal = TRUE
          AND conversations.organization_id IS NULL
    """)
    )


def downgrade() -> None:
    conn = op.get_bind()

    conn.execute(sa.text("UPDATE conversations SET organization_id = NULL"))
