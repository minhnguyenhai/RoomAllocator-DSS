"""Add column 'is_smoker' into table 'student_requests'

Revision ID: 25d6a666b398
Revises: d93ae92ce735
Create Date: 2024-12-07 16:25:44.461927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25d6a666b398'
down_revision = 'd93ae92ce735'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_smoker', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student_requests', schema=None) as batch_op:
        batch_op.drop_column('is_smoker')

    # ### end Alembic commands ###