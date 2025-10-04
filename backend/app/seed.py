from sqlalchemy.orm import Session
from .core.database import SessionLocal, engine, Base
from .core.security import get_password_hash
from . import models
from datetime import datetime, date, timedelta


def init_db():
    """Initialize database with tables and seed data"""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Create admin user
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            admin = models.User(
                username="admin",
                email="admin@logisuiel.fr",
                hashed_password=get_password_hash("admin"),
                role="ADMIN",
                full_name="Administrator",
                is_active=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            
            # Create admin preferences
            admin_prefs = models.UserPreferences(user_id=admin.id)
            db.add(admin_prefs)
        
        # Create teacher user
        teacher = db.query(models.User).filter(models.User.username == "test").first()
        if not teacher:
            teacher = models.User(
                username="test",
                email="test@logisuiel.fr",
                hashed_password=get_password_hash("test"),
                role="TEACHER",
                full_name="Test Teacher",
                is_active=True
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            
            # Create teacher preferences
            teacher_prefs = models.UserPreferences(user_id=teacher.id)
            db.add(teacher_prefs)
        
        # Create sample students
        if db.query(models.Student).count() == 0:
            students = [
                models.Student(
                    first_name="Jean",
                    last_name="Dupont",
                    date_of_birth=date(2010, 5, 15),
                    class_name="6ème A",
                    student_id="S001",
                    email="jean.dupont@example.com"
                ),
                models.Student(
                    first_name="Marie",
                    last_name="Martin",
                    date_of_birth=date(2010, 8, 22),
                    class_name="6ème A",
                    student_id="S002",
                    email="marie.martin@example.com"
                ),
                models.Student(
                    first_name="Pierre",
                    last_name="Bernard",
                    date_of_birth=date(2010, 3, 10),
                    class_name="6ème B",
                    student_id="S003",
                    email="pierre.bernard@example.com"
                ),
            ]
            for student in students:
                db.add(student)
        
        # Create sample competences
        if db.query(models.Competence).count() == 0:
            competences = [
                models.Competence(
                    code="C1.1",
                    name="Comprendre un texte",
                    description="Capacité à comprendre et analyser un texte",
                    category="Français",
                    level="6ème"
                ),
                models.Competence(
                    code="M1.1",
                    name="Calcul mental",
                    description="Maîtriser les opérations de base",
                    category="Mathématiques",
                    level="6ème"
                ),
                models.Competence(
                    code="H1.1",
                    name="Se repérer dans le temps",
                    description="Situer des événements historiques",
                    category="Histoire",
                    level="6ème"
                ),
            ]
            for competence in competences:
                db.add(competence)
        
        # Create sample timetable events
        if db.query(models.TimetableEvent).count() == 0:
            today = datetime.now()
            monday = today - timedelta(days=today.weekday())
            
            events = [
                models.TimetableEvent(
                    title="Mathématiques 6A",
                    start_time=monday.replace(hour=8, minute=0),
                    end_time=monday.replace(hour=9, minute=0),
                    class_name="6ème A",
                    subject="Mathématiques",
                    teacher_id=teacher.id
                ),
                models.TimetableEvent(
                    title="Français 6B",
                    start_time=monday.replace(hour=10, minute=0),
                    end_time=monday.replace(hour=11, minute=0),
                    class_name="6ème B",
                    subject="Français",
                    teacher_id=teacher.id
                ),
            ]
            for event in events:
                db.add(event)
        
        # Create sample reminders
        if db.query(models.Reminder).count() == 0:
            reminders = [
                models.Reminder(
                    title="Réunion parents d'élèves",
                    description="Présenter le programme de l'année",
                    type="REUNION",
                    due_date=datetime.now() + timedelta(days=7),
                    priority="HIGH",
                    teacher_id=teacher.id
                ),
                models.Reminder(
                    title="Correction devoirs",
                    description="Corriger les devoirs de la semaine",
                    type="RAPPEL_DEVOIR",
                    due_date=datetime.now() + timedelta(days=2),
                    priority="NORMAL",
                    teacher_id=teacher.id
                ),
            ]
            for reminder in reminders:
                db.add(reminder)
        
        db.commit()
        print("Database initialized successfully!")
        print("Admin credentials: admin / admin")
        print("Teacher credentials: test / test")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
