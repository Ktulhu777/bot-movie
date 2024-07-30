from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.models import Users, Movie, Admin


async def user_exists(pk_user: int, session: AsyncSession):
    """Проверка наличия пользователя в DB если есть False, если нет True"""
    user = await session.execute(select(Users).where(Users.telegram_user_id == pk_user))
    return False if user.scalar() else True


async def movie_exists(movie_code: int, session: AsyncSession, get_movie: bool = False):
    """Проверка наличия фильма по code в DB если есть False, если нет True"""
    movie = await session.execute(select(Movie).where(Movie.movie_code == movie_code))
    if not get_movie:
        return False if movie.scalar() else True
    return movie.scalar()


async def add_user_in_db(pk_user: int, session: AsyncSession):
    if await user_exists(pk_user, session):
        user = Users(telegram_user_id=pk_user)
        session.add(user)
        await session.commit()
        await session.refresh(user)


async def add_movie_in_db(movie_code: int, title: str, session: AsyncSession):
    if await movie_exists(movie_code=movie_code, session=session):
        movie = Movie(movie_code=movie_code, title=title)
        session.add(movie)
        await session.commit()
        await session.refresh(movie)
        return True
    return False


async def exists_super_user(id_super_user: int, session: AsyncSession) -> bool:
    admin = await session.execute(select(Admin).where(Admin.id_super_user == id_super_user))
    return True if admin.scalar() else False


async def add_super_user(id_super_user: int, session: AsyncSession):
    admin = Admin(id_super_user=id_super_user)
    session.add(admin)
    await session.commit()
    await session.refresh(admin)
