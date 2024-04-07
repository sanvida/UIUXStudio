from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)

class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_name = Column(String, nullable=False)
    details = Column(JSON)

    user = relationship("User", back_populates="integrations")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)

    user = relationship("User", back_populates="recommendations")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text, nullable=False)
    time = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="reminders")

class Automation(Base):
    __tablename__ = "automations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_name = Column(String, nullable=False)
    details = Column(JSON)

    user = relationship("User", back_populates="automations")

User.integrations = relationship("Integration", back_populates="user")
User.recommendations = relationship("Recommendation", back_populates="user")
User.reminders = relationship("Reminder", back_populates="user")
User.automations = relationship("Automation", back_populates="user")
