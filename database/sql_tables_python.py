from sqlalchemy import create_engine, Integer, String, Float, MetaData, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship, registry, Mapped, mapped_column

status_enum = Enum('Planned', 'In-progress', 'Completed', name='status_enum')

metadata = MetaData()

type_annotation_map = {
    str: String().with_variant(String(255), "mysql", "mariadb"),
    int: Integer,
    float: Float,
}
mapper_registry = registry(type_annotation_map = type_annotation_map)

class Base(DeclarativeBase):
    metadata = metadata 
    type_annotation_map = type_annotation_map
    mapper_registry = mapper_registry

class Users(Base):
    __tablename__ = 'Users'
    user_id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    Username: Mapped[str] = mapped_column(String(255), unique = True, nullable = False)
    Email: Mapped[str] = mapped_column(String(255), unique = True, nullable = False)
    Password: Mapped[str] = mapped_column(String(255), nullable = False)

    user_trackers = relationship('User_Trackers', back_populates='user')

class Shows(Base):
    __tablename__ = 'Shows'
    show_id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(255))
    episodes: Mapped[int] = mapped_column(Integer)
    genres: Mapped[str] = mapped_column(String(255))
    backdrop: Mapped[str] = mapped_column(String(255))
    returnEnded: Mapped[str] = mapped_column(String(255))

    show_trackers = relationship('User_Trackers', back_populates='show')

class User_Trackers(Base):
    __tablename__ = 'User_Trackers'
    tracker_id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.user_id'), nullable = False)
    show_id: Mapped[int] = mapped_column(Integer, ForeignKey('Shows.show_id'), nullable = False)
    status: Mapped[str] = mapped_column(status_enum, nullable = False)
    progress: Mapped[int] = mapped_column(Integer, default = 0)

    __table_args__ = (UniqueConstraint('user_id', 'show_id', name='uq_user_show_tracker'),)

    user = relationship('Users', back_populates = 'user_trackers')
    show = relationship('Shows', back_populates = 'show_trackers')