import csv
import io
from datetime import datetime
from sqlalchemy.orm import Session
from .. import models


def import_students_from_csv(csv_content: str, db: Session) -> dict:
    """Import students from CSV content"""
    errors = []
    imported_count = 0
    
    try:
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        
        for row_num, row in enumerate(reader, start=2):
            try:
                # Parse date of birth if present
                dob = None
                if row.get('date_of_birth'):
                    try:
                        dob = datetime.strptime(row['date_of_birth'], '%Y-%m-%d').date()
                    except ValueError:
                        try:
                            dob = datetime.strptime(row['date_of_birth'], '%d/%m/%Y').date()
                        except ValueError:
                            pass
                
                # Check if student already exists
                existing = db.query(models.Student).filter(
                    models.Student.student_id == row.get('student_id')
                ).first() if row.get('student_id') else None
                
                if existing:
                    # Update existing student
                    existing.first_name = row.get('first_name', existing.first_name)
                    existing.last_name = row.get('last_name', existing.last_name)
                    existing.date_of_birth = dob or existing.date_of_birth
                    existing.class_name = row.get('class_name', existing.class_name)
                    existing.email = row.get('email', existing.email)
                    existing.phone = row.get('phone', existing.phone)
                    existing.address = row.get('address', existing.address)
                    existing.parent_name = row.get('parent_name', existing.parent_name)
                    existing.parent_email = row.get('parent_email', existing.parent_email)
                    existing.parent_phone = row.get('parent_phone', existing.parent_phone)
                    existing.medical_info = row.get('medical_info', existing.medical_info)
                else:
                    # Create new student
                    student = models.Student(
                        first_name=row.get('first_name', ''),
                        last_name=row.get('last_name', ''),
                        date_of_birth=dob,
                        class_name=row.get('class_name', ''),
                        student_id=row.get('student_id', ''),
                        email=row.get('email', ''),
                        phone=row.get('phone', ''),
                        address=row.get('address', ''),
                        parent_name=row.get('parent_name', ''),
                        parent_email=row.get('parent_email', ''),
                        parent_phone=row.get('parent_phone', ''),
                        medical_info=row.get('medical_info', '')
                    )
                    db.add(student)
                
                imported_count += 1
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Successfully imported {imported_count} students",
            "imported_count": imported_count,
            "errors": errors
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"Failed to import students: {str(e)}",
            "imported_count": 0,
            "errors": [str(e)]
        }


def import_competences_from_csv(csv_content: str, db: Session) -> dict:
    """Import competences from CSV content"""
    errors = []
    imported_count = 0
    
    try:
        csv_file = io.StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        
        for row_num, row in enumerate(reader, start=2):
            try:
                # Check if competence already exists
                existing = db.query(models.Competence).filter(
                    models.Competence.code == row.get('code')
                ).first()
                
                if existing:
                    # Update existing competence
                    existing.name = row.get('name', existing.name)
                    existing.description = row.get('description', existing.description)
                    existing.category = row.get('category', existing.category)
                    existing.level = row.get('level', existing.level)
                else:
                    # Create new competence
                    competence = models.Competence(
                        code=row.get('code', ''),
                        name=row.get('name', ''),
                        description=row.get('description', ''),
                        category=row.get('category', ''),
                        level=row.get('level', '')
                    )
                    db.add(competence)
                
                imported_count += 1
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Successfully imported {imported_count} competences",
            "imported_count": imported_count,
            "errors": errors
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"Failed to import competences: {str(e)}",
            "imported_count": 0,
            "errors": [str(e)]
        }
