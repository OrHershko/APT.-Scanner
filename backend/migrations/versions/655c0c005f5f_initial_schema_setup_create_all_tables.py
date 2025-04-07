"""Initial schema setup create all tables

Revision ID: 655c0c005f5f
Revises: 
Create Date: 2025-04-07 23:14:22.922971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '655c0c005f5f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('firebase_uid', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_firebase_uid'), 'users', ['firebase_uid'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('user_preferences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('pace_of_life', sa.Enum('RELAXED', 'BALANCED', 'ENERGETIC', name='paceoflife'), nullable=True),
    sa.Column('commute_pref_pt', sa.Boolean(), nullable=True),
    sa.Column('commute_pref_walk', sa.Boolean(), nullable=True),
    sa.Column('commute_pref_bike', sa.Boolean(), nullable=True),
    sa.Column('commute_pref_car', sa.Boolean(), nullable=True),
    sa.Column('commute_pref_wfh', sa.Boolean(), nullable=True),
    sa.Column('parking_importance', sa.Enum('ESSENTIAL', 'PREFERABLE', 'NOT_IMPORTANT', name='parkingimportance'), nullable=True),
    sa.Column('max_commute_time', sa.Integer(), nullable=True),
    sa.Column('social_community_importance', sa.Integer(), nullable=True),
    sa.Column('wfh_needs_quiet_area', sa.Boolean(), nullable=True),
    sa.Column('nearby_restaurants_importance', sa.Enum('NOT_IMPORTANT', 'SOMEWHAT', 'VERY', name='importancescale'), nullable=True),
    sa.Column('budget_min', sa.Integer(), nullable=True),
    sa.Column('budget_max', sa.Integer(), nullable=True),
    sa.Column('preferred_size', sa.Integer(), nullable=True),
    sa.Column('pref_apt_type_new', sa.Boolean(), nullable=True),
    sa.Column('pref_apt_type_old', sa.Boolean(), nullable=True),
    sa.Column('pref_apt_type_renovated', sa.Boolean(), nullable=True),
    sa.Column('needs_furnished', sa.Enum('YES', 'NO', 'NO_PREFERENCE', name='yesnopref'), nullable=True),
    sa.Column('needs_balcony', sa.Enum('YES', 'NO', 'NO_PREFERENCE', name='yesnopref'), nullable=True),
    sa.Column('dealbreaker_no_parking', sa.Boolean(), nullable=True),
    sa.Column('dealbreaker_no_elevator_high', sa.Boolean(), nullable=True),
    sa.Column('needs_pet_friendly', sa.Enum('YES', 'NO', 'NO_PREFERENCE', name='yesnopref'), nullable=True),
    sa.Column('proximity_shops_importance', sa.Integer(), nullable=True),
    sa.Column('proximity_beach_importance', sa.Enum('NOT_IMPORTANT', 'SOMEWHAT', 'VERY', name='importancescale'), nullable=True),
    sa.Column('safety_importance', sa.Enum('NOT_IMPORTANT', 'SOMEWHAT', 'VERY', name='importancescale'), nullable=True),
    sa.Column('priority_work', sa.Boolean(), nullable=True),
    sa.Column('priority_price', sa.Boolean(), nullable=True),
    sa.Column('compromise_size_for_location', sa.Enum('YES', 'NO', 'NO_PREFERENCE', name='yesnopref'), nullable=True),
    sa.Column('avoid_construction', sa.Enum('YES', 'NO', 'NO_PREFERENCE', name='yesnopref'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_preferences_id'), 'user_preferences', ['id'], unique=False)
    op.create_index(op.f('ix_user_preferences_user_id'), 'user_preferences', ['user_id'], unique=True)
    op.drop_constraint('images_listing_order_id_image_url_key', 'images', type_='unique')
    op.drop_table_comment(
        'images',
        existing_comment='Stores image URLs associated with listings.',
        schema=None
    )
    op.drop_table_comment(
        'listing_tags',
        existing_comment='Junction table linking listings and tags (Many-to-Many).',
        schema=None
    )
    op.drop_column('listing_tags', 'priority')
    op.alter_column('listings', 'neighborhood_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='FK referencing the neighborhoods table using yad2_hood_id.',
               existing_nullable=True)
    op.alter_column('listings', 'neighborhood_text',
               existing_type=sa.VARCHAR(length=150),
               comment=None,
               existing_comment='The raw neighborhood name text as it appeared in the source listing data.',
               existing_nullable=True)
    op.alter_column('listings', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('listings', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_table_comment(
        'listings',
        existing_comment='Stores individual apartment listings from Yad2.',
        schema=None
    )
    op.alter_column('neighborhoods', 'yad2_doc_count',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Possibly the number of listings found by Yad2 for this neighborhood at the time of mapping.',
               existing_nullable=True)
    op.alter_column('neighborhoods', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('neighborhoods', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_table_comment(
        'neighborhoods',
        existing_comment='Stores detailed information about neighborhoods, linked by Yad2 hood ID.',
        schema=None
    )
    op.drop_table_comment(
        'property_conditions',
        existing_comment='Lookup table for property condition descriptions.',
        schema=None
    )
    op.drop_table_comment(
        'tags',
        existing_comment='Lookup table for unique listing tags.',
        schema=None
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table_comment(
        'tags',
        'Lookup table for unique listing tags.',
        existing_comment=None,
        schema=None
    )
    op.create_table_comment(
        'property_conditions',
        'Lookup table for property condition descriptions.',
        existing_comment=None,
        schema=None
    )
    op.create_table_comment(
        'neighborhoods',
        'Stores detailed information about neighborhoods, linked by Yad2 hood ID.',
        existing_comment=None,
        schema=None
    )
    op.alter_column('neighborhoods', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('neighborhoods', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('neighborhoods', 'yad2_doc_count',
               existing_type=sa.INTEGER(),
               comment='Possibly the number of listings found by Yad2 for this neighborhood at the time of mapping.',
               existing_nullable=True)
    op.create_table_comment(
        'listings',
        'Stores individual apartment listings from Yad2.',
        existing_comment=None,
        schema=None
    )
    op.alter_column('listings', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('listings', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('listings', 'neighborhood_text',
               existing_type=sa.VARCHAR(length=150),
               comment='The raw neighborhood name text as it appeared in the source listing data.',
               existing_nullable=True)
    op.alter_column('listings', 'neighborhood_id',
               existing_type=sa.INTEGER(),
               comment='FK referencing the neighborhoods table using yad2_hood_id.',
               existing_nullable=True)
    op.add_column('listing_tags', sa.Column('priority', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_table_comment(
        'listing_tags',
        'Junction table linking listings and tags (Many-to-Many).',
        existing_comment=None,
        schema=None
    )
    op.create_table_comment(
        'images',
        'Stores image URLs associated with listings.',
        existing_comment=None,
        schema=None
    )
    op.create_unique_constraint('images_listing_order_id_image_url_key', 'images', ['listing_order_id', 'image_url'])
    op.drop_index(op.f('ix_user_preferences_user_id'), table_name='user_preferences')
    op.drop_index(op.f('ix_user_preferences_id'), table_name='user_preferences')
    op.drop_table('user_preferences')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_firebase_uid'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
