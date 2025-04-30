from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        #   yield обеспечивает закрытие соединения после использования
        yield db
    finally:
        db.close()
