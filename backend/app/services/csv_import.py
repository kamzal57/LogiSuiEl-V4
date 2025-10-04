import csv
import io
from typing import List, Dict, Any
from datetime import datetime
from fastapi import UploadFile

async def parse_students_csv(file: UploadFile) -> List[Dict[str, Any]]:
    """Parse students CSV file and return list of student dictionaries"""
    content = await file.read()
    decoded = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(decoded))
    
    students = []
    for row in csv_reader:
        student_data = {
            'first_name': row.get('first_name', row.get('prenom', '')),
            'last_name': row.get('last_name', row.get('nom', '')),
            'class_name': row.get('class_name', row.get('classe', '')),
            'student_id': row.get('student_id', row.get('id_eleve', '')),
            'email': row.get('email', ''),
            'phone': row.get('phone', row.get('telephone', '')),
            'date_of_birth': row.get('date_of_birth', row.get('date_naissance', '')),
            'address': row.get('address', row.get('adresse', '')),
            'parent_name': row.get('parent_name', row.get('nom_parent', '')),
            'parent_email': row.get('parent_email', row.get('email_parent', '')),
            'parent_phone': row.get('parent_phone', row.get('telephone_parent', '')),
        }
        
        # Parse date if provided
        if student_data['date_of_birth']:
            try:
                student_data['date_of_birth'] = datetime.strptime(
                    student_data['date_of_birth'], '%Y-%m-%d'
                ).date()
            except ValueError:
                student_data['date_of_birth'] = None
        else:
            student_data['date_of_birth'] = None
            
        students.append(student_data)
    
    return students

async def parse_competences_csv(file: UploadFile) -> List[Dict[str, Any]]:
    """Parse competences CSV file and return list of competence dictionaries"""
    content = await file.read()
    decoded = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(decoded))
    
    competences = []
    for row in csv_reader:
        competence_data = {
            'code': row.get('code', ''),
            'name': row.get('name', row.get('nom', '')),
            'description': row.get('description', ''),
            'category': row.get('category', row.get('categorie', '')),
            'level': row.get('level', row.get('niveau', '')),
        }
        
        # Parse level as integer
        if competence_data['level']:
            try:
                competence_data['level'] = int(competence_data['level'])
            except ValueError:
                competence_data['level'] = None
        else:
            competence_data['level'] = None
            
        competences.append(competence_data)
    
    return competences
