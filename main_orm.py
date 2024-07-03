from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, select
from sqlalchemy.orm import registry, declarative_base, DeclarativeBase, as_declarative, mapped_column, Mapped, Session

engine = create_engine("sqlite:///:memory:", echo=True)
# mapper_registry = registry()
# print(mapper_registry)
# print(mapper_registry.metadata)
# Base = mapper_registry.generate_base()


class AbstractModel(DeclarativeBase):
    __allow_unmapped__ = True
    # id = Column(Integer, primary_key=True, autoincrement=True)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class UserModel(AbstractModel):
    __tablename__ = "users"
    # username = Column(String(50), unique=True, nullable=False)
    # fullname = Column(String)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    fullname: Mapped[str] = mapped_column()


class AddressModel(AbstractModel):
    __tablename__ = "addresses"
    # user_id = Column(ForeignKey("users.id"))
    user_id = mapped_column(ForeignKey("users.id"))


print(UserModel.__table__.__dict__)
print(AddressModel.__tablename__)


with Session(engine) as session:
    with session.begin():
        AbstractModel.metadata.create_all(engine)
        user = UserModel(username='Max', fullname='Max Payne')
        session.add(user)
    with session.begin():
        query_res = session.execute(select(UserModel).where(UserModel.username == 'Max'))
        user = query_res.scalar()
        print(user.fullname)
