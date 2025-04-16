"""Database models for the application."""
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey, Enum as SQLEnum,
    DECIMAL, TEXT, BIGINT, TIMESTAMP, Table, MetaData
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, List
from enum import Enum as PyEnum
from .database import Base 
from pydantic import BaseModel, Field

# Define the association table for the Many-to-Many relationship
# between listings and tags using SQLAlchemy Core Table object
listing_tags_association = Table(
    "listing_tags",
    Base.metadata, # Use metadata from the Declarative Base
    Column("listing_order_id", BIGINT, ForeignKey("listings.order_id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True),
)

# --- Lookup Tables Models ---
class PropertyCondition(Base):
    __tablename__ = "property_conditions"

    condition_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    condition_name_he: Mapped[Optional[str]] = mapped_column(String(100))
    condition_name_en: Mapped[Optional[str]] = mapped_column(String(100))

    # Relationship back to listings (optional, if needed)
    listings: Mapped[List["Listing"]] = relationship(back_populates="property_condition")

    def __repr__(self):
        return f"<PropertyCondition(id={self.condition_id}, name_en='{self.condition_name_en}')>"

class Tag(Base):
    __tablename__ = "tags"

    tag_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Many-to-Many relationship to Listings through the association table
    listings: Mapped[List["Listing"]] = relationship(
        secondary=listing_tags_association, back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag(id={self.tag_id}, name='{self.tag_name}')>"

# --- Main Tables Models ---
class Neighborhood(Base):
    __tablename__ = "neighborhoods"

    yad2_hood_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hebrew_name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    english_name: Mapped[Optional[str]] = mapped_column(String(150), unique=True)
    avg_purchase_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(15, 2))
    avg_rent_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2))
    socioeconomic_index: Mapped[Optional[float]] = mapped_column(Float)
    avg_school_rating: Mapped[Optional[float]] = mapped_column(Float)
    general_overview: Mapped[Optional[str]] = mapped_column(TEXT)
    bars_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    restaurants_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    clubs_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    shopping_malls_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    unique_entertainment_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    primary_schools_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    elementary_schools_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    secondary_schools_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    high_schools_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    universities_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    closest_beach_distance_km: Mapped[Optional[float]] = mapped_column(Float)
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    yad2_city_id: Mapped[Optional[int]] = mapped_column(Integer)
    yad2_area_id: Mapped[Optional[int]] = mapped_column(Integer)
    yad2_top_area_id: Mapped[Optional[int]] = mapped_column(Integer)
    yad2_doc_count: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()) # Or rely only on DB trigger

    # One-to-Many relationship to Listings
    listings: Mapped[List["Listing"]] = relationship(back_populates="neighborhood")

    def __repr__(self):
        return f"<Neighborhood(id={self.yad2_hood_id}, name='{self.hebrew_name}')>"


class Listing(Base):
    __tablename__ = "listings"

    order_id: Mapped[int] = mapped_column(BIGINT, primary_key=True) # Use BIGINT
    token: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)

    # Foreign keys
    neighborhood_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("neighborhoods.yad2_hood_id", ondelete="SET NULL"))
    property_condition_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("property_conditions.condition_id", ondelete="SET NULL"))

    # Other fields
    subcategory_id: Mapped[Optional[int]] = mapped_column(Integer)
    category_id: Mapped[Optional[int]] = mapped_column(Integer)
    ad_type: Mapped[Optional[str]] = mapped_column(String(20))
    price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2))
    property_type: Mapped[Optional[str]] = mapped_column(String(50))
    rooms_count: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(3, 1)) # Allows 2.5 etc.
    square_meter: Mapped[Optional[int]] = mapped_column(Integer)
    cover_image_url: Mapped[Optional[str]] = mapped_column(TEXT)
    video_url: Mapped[Optional[str]] = mapped_column(TEXT)
    priority: Mapped[Optional[int]] = mapped_column(Integer)
    city: Mapped[Optional[str]] = mapped_column(String(100))
    area: Mapped[Optional[str]] = mapped_column(String(100))
    neighborhood_text: Mapped[Optional[str]] = mapped_column(String(150)) # Raw text from source
    street: Mapped[Optional[str]] = mapped_column(String(150))
    house_number: Mapped[Optional[str]] = mapped_column(String(20)) # Varchar for '10א' etc.
    floor: Mapped[Optional[int]] = mapped_column(Integer)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()) # Or rely only on DB trigger

    # Many-to-One relationships
    neighborhood: Mapped[Optional["Neighborhood"]] = relationship(back_populates="listings")
    property_condition: Mapped[Optional["PropertyCondition"]] = relationship(back_populates="listings")

    # One-to-Many relationship to Images
    images: Mapped[List["Image"]] = relationship(back_populates="listing", cascade="all, delete-orphan")

    # Many-to-Many relationship to Tags
    tags: Mapped[List["Tag"]] = relationship(
        secondary=listing_tags_association, back_populates="listings"
    )

    def __repr__(self):
        return f"<Listing(order_id={self.order_id}, token='{self.token}')>"


class Image(Base):
    __tablename__ = "images"

    image_id: Mapped[int] = mapped_column(Integer, primary_key=True) # Serial handled by DB
    listing_order_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("listings.order_id", ondelete="CASCADE"), nullable=False)
    image_url: Mapped[str] = mapped_column(TEXT, nullable=False)

    # Many-to-One relationship back to Listing
    listing: Mapped["Listing"] = relationship(back_populates="images")

    def __repr__(self):
        return f"<Image(id={self.image_id}, listing_id={self.listing_order_id})>"

# --- Enums ---
class PaceOfLife(str, PyEnum):
    RELAXED = "relaxed"
    BALANCED = "balanced"
    ENERGETIC = "energetic"

class ParkingImportance(str, PyEnum):
    ESSENTIAL = "essential"
    PREFERABLE = "preferable"
    NOT_IMPORTANT = "not_important"

# הגדירו Enums נוספים לשאר הבחירות בהתאם לצורך
class ImportanceScale(str, PyEnum): # דוגמה לסקאלה משותפת
    NOT_IMPORTANT = "not_important"
    SOMEWHAT = "somewhat"
    VERY = "very"

class YesNoPref(str, PyEnum): # דוגמה לכן/לא/אין העדפה
    YES = "yes"
    NO = "no"
    NO_PREFERENCE = "no_preference"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    firebase_uid: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, index=True, nullable=True)
    # Relationship to preferences
    preferences: Mapped[Optional["UserPreferences"]] = relationship(back_populates="owner")

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False, index=True)

    # Section 1: Lifestyle
    pace_of_life: Mapped[Optional[PaceOfLife]] = mapped_column(SQLEnum(PaceOfLife), nullable=True)
    commute_pref_pt: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    commute_pref_walk: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    commute_pref_bike: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    commute_pref_car: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    commute_pref_wfh: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)

    # Section 2: Location preferences
    proximity_pref_shops: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    proximity_pref_gym: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    max_commute_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # in minutes

    # Section 3: Lifestyle-related needs
    dog_park_nearby: Mapped[Optional[YesNoPref]] = mapped_column(SQLEnum(YesNoPref), nullable=True)
    learning_space_nearby: Mapped[Optional[YesNoPref]] = mapped_column(SQLEnum(YesNoPref), nullable=True)

    # Section 4: Importance ratings
    proximity_beach_importance: Mapped[Optional[ImportanceScale]] = mapped_column(SQLEnum(ImportanceScale), nullable=True)
    safety_importance: Mapped[Optional[ImportanceScale]] = mapped_column(SQLEnum(ImportanceScale), nullable=True)
    green_spaces_importance: Mapped[Optional[ImportanceScale]] = mapped_column(SQLEnum(ImportanceScale), nullable=True)
    medical_center_importance: Mapped[Optional[ImportanceScale]] = mapped_column(SQLEnum(ImportanceScale), nullable=True)
    schools_importance: Mapped[Optional[ImportanceScale]] = mapped_column(SQLEnum(ImportanceScale), nullable=True)

    # Relationship back to User
    owner: Mapped["User"] = relationship(back_populates="preferences")

class QuestionModel(BaseModel):
    category: str
    id: str
    text: str
    type: str
    options: Optional[List[str]] = None
    config: Optional[dict[str,Any]] = None
    conditional: Optional[dict[str,Any]] = None
