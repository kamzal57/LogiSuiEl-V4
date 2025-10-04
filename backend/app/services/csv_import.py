from __future__ import annotations

import csv
from datetime import datetime
from io import StringIO

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Competence, Student
from ..schemas import CSVImportSummary

STUDENT_FIELD_MAPPING = {
    "external_id": ["id", "external_id", "eleve_id"],
    "first_name": ["first_name", "prenom", "first"],
    "last_name": ["last_name", "nom", "last"],
    "class_name": ["classe", "class", "class_name"],
    "birth_date": ["birth_date", "naissance"],
    "email": ["email"],
    "phone": ["phone", "telephone"],
}

COMPETENCE_FIELD_MAPPING = {
    "code": ["code", "competence_code"],
    "title": ["title", "intitule", "competence"],
    "description": ["description", "details"],
}


def _extract_value(row: dict[str, str], keys: list[str]) -> str | None:
    for key in keys:
        if key in row and row[key].strip():
            return row[key].strip()
    return None


async def import_students(file: UploadFile, session: AsyncSession) -> CSVImportSummary:
    raw = await file.read()
    decoded = raw.decode("utf-8-sig")
    reader = csv.DictReader(StringIO(decoded))

    inserted = updated = skipped = 0

    for row in reader:
        external_id = _extract_value(row, STUDENT_FIELD_MAPPING["external_id"]) or None
        first_name = _extract_value(row, STUDENT_FIELD_MAPPING["first_name"])
        last_name = _extract_value(row, STUDENT_FIELD_MAPPING["last_name"])

        if not first_name or not last_name:
            skipped += 1
            continue

        stmt = select(Student)
        if external_id:
            stmt = stmt.where(Student.external_id == external_id)
        else:
            stmt = stmt.where(Student.first_name == first_name, Student.last_name == last_name)
        result = await session.execute(stmt)
        student = result.scalar_one_or_none()

        data = {
            "external_id": external_id,
            "first_name": first_name,
            "last_name": last_name,
            "class_name": _extract_value(row, STUDENT_FIELD_MAPPING["class_name"]),
            "email": _extract_value(row, STUDENT_FIELD_MAPPING["email"]),
            "phone": _extract_value(row, STUDENT_FIELD_MAPPING["phone"]),
        }

        birth_date_raw = _extract_value(row, STUDENT_FIELD_MAPPING["birth_date"])
        if birth_date_raw:
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                try:
                    data["birth_date"] = datetime.strptime(birth_date_raw, fmt).date()
                    break
                except ValueError:
                    continue

        if student:
            for key, value in data.items():
                setattr(student, key, value)
            updated += 1
        else:
            session.add(Student(**data))
            inserted += 1

    await session.commit()

    return CSVImportSummary(inserted=inserted, updated=updated, skipped=skipped)


async def import_competences(file: UploadFile, session: AsyncSession) -> CSVImportSummary:
    raw = await file.read()
    decoded = raw.decode("utf-8-sig")
    reader = csv.DictReader(StringIO(decoded))

    inserted = updated = skipped = 0

    for row in reader:
        code = _extract_value(row, COMPETENCE_FIELD_MAPPING["code"])
        title = _extract_value(row, COMPETENCE_FIELD_MAPPING["title"])
        description = _extract_value(row, COMPETENCE_FIELD_MAPPING["description"]) or ""

        if not code or not title:
            skipped += 1
            continue

        result = await session.execute(select(Competence).where(Competence.code == code))
        competence = result.scalar_one_or_none()
        if competence:
            competence.title = title
            competence.description = description
            updated += 1
        else:
            session.add(Competence(code=code, title=title, description=description))
            inserted += 1

    await session.commit()

    return CSVImportSummary(inserted=inserted, updated=updated, skipped=skipped)
