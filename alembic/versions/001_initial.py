# revision identifiers, used by Alembic.
revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # This migration will be empty since we're using SQLAlchemy's create_all
    # to create the initial tables in main.py
    pass


def downgrade() -> None:
    # This is the initial migration, so nothing to downgrade
    pass
