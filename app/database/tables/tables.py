import uuid
import datetime

from sqlalchemy import create_engine, String, ForeignKey, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship

from app.settings import AppSettings

engine = create_engine(
    AppSettings().postgres_url,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    icmp_pings = relationship("IcmpPingConfig", back_populates="owner")
    http_pings = relationship("HttpPingConfig", back_populates="owner")
    kube_metrics = relationship("KubeMetricsConfig", back_populates="owner")


class IcmpPingConfig(Base):
    __tablename__ = "icmp_ping_config"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow  # Set default timestamp
    )
    hostname: Mapped[str] = mapped_column(String(255), nullable=False)
    check_interval: Mapped[int] = mapped_column(Integer, nullable=False)
    is_paused: Mapped[bool] = mapped_column(Boolean, nullable=True)

    owner = relationship("User", back_populates="icmp_pings")


class HttpPingConfig(Base):
    __tablename__ = "http_ping_config"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow  # Set default timestamp
    )
    endpoint_url: Mapped[str] = mapped_column(String(255), nullable=False)
    check_interval: Mapped[int] = mapped_column(Integer, nullable=False)
    is_paused: Mapped[bool] = mapped_column(Boolean, nullable=True)

    owner = relationship("User", back_populates="http_pings")


class KubeMetricsConfig(Base):
    __tablename__ = "kube_metrics_config"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    check_interval: Mapped[int] = mapped_column(Integer, nullable=False)

    owner = relationship("User", back_populates="kube_metrics")
