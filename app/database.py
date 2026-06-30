from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./finance.db"

# Главный вход в базу. Создаем объект, который умеет подключаться к БД,
# выполнять SQL-запросы и управлять соединениями
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Фабрика сессий, Создаем сессию. Сессия - это рабочая область, где мы создаем,
# изменяем и удаляем объекты, а потом сохраняем их
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Фабрика базового класса для моделей. От этого мы будем наследовать
# все свои таблицы
Base = declarative_base()
