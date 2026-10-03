from scraper.db.base import Base, engine
from scraper.db import models


def main() -> None:
    print("🔧 Создаю таблицы...")
    Base.metadata.create_all(engine)
    print("✅ Готово. Таблицы:")
    for table_name in Base.metadata.tables:
        print(f"   - {table_name}")


if __name__ == "__main__":
    main()
