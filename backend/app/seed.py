from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models import User, UserPreferences, Student, Competence
from app.models.user import Role
from datetime import date

def init_db():
    """Initialize database with default data"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            # Create admin user
            admin_user = User(
                username="admin",
                email="admin@logisuiel.com",
                hashed_password=get_password_hash("admin"),
                role=Role.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            # Create preferences for admin
            admin_prefs = UserPreferences(user_id=admin_user.id)
            db.add(admin_prefs)
            print("✓ Created admin user (username: admin, password: admin)")
        
        # Check if test teacher user already exists
        test_user = db.query(User).filter(User.username == "test").first()
        if not test_user:
            # Create test teacher user
            test_user = User(
                username="test",
                email="test@logisuiel.com",
                hashed_password=get_password_hash("test"),
                role=Role.TEACHER,
                is_active=True
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            
            # Create preferences for test user
            test_prefs = UserPreferences(user_id=test_user.id)
            db.add(test_prefs)
            print("✓ Created test user (username: test, password: test)")
        
        # Add some sample students
        existing_students = db.query(Student).count()
        if existing_students == 0:
            sample_students = [
                Student(
                    first_name="Jean",
                    last_name="Dupont",
                    class_name="6ème A",
                    student_id="STU001",
                    date_of_birth=date(2010, 5, 15),
                    email="jean.dupont@example.com"
                ),
                Student(
                    first_name="Marie",
                    last_name="Martin",
                    class_name="6ème A",
                    student_id="STU002",
                    date_of_birth=date(2010, 8, 22),
                    email="marie.martin@example.com"
                ),
                Student(
                    first_name="Pierre",
                    last_name="Dubois",
                    class_name="6ème B",
                    student_id="STU003",
                    date_of_birth=date(2010, 3, 10),
                    email="pierre.dubois@example.com"
                ),
            ]
            
            for student in sample_students:
                db.add(student)
            
            print(f"✓ Created {len(sample_students)} sample students")
        
        # Add some sample competences
        existing_competences = db.query(Competence).count()
        if existing_competences == 0:
            sample_competences = [
                Competence(
                    code="MATH-01",
                    name="Résoudre des problèmes",
                    description="Résoudre des problèmes simples",
                    category="Mathématiques",
                    level=1
                ),
                Competence(
                    code="MATH-02",
                    name="Calcul mental",
                    description="Maîtriser le calcul mental",
                    category="Mathématiques",
                    level=1
                ),
                Competence(
                    code="FR-01",
                    name="Lire et comprendre",
                    description="Lire et comprendre un texte",
                    category="Français",
                    level=1
                ),
                Competence(
                    code="FR-02",
                    name="Écrire",
                    description="Écrire un texte cohérent",
                    category="Français",
                    level=1
                ),
            ]
            
            for competence in sample_competences:
                db.add(competence)
            
            print(f"✓ Created {len(sample_competences)} sample competences")
        
        db.commit()
        print("\n✓ Database initialized successfully!")
        
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
