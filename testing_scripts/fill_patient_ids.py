import asyncio
import re
from datetime import datetime

from sqlalchemy.future import select

# Import the AsyncSession factory from your database module.
from app.database.db import SessionLocal
# Import the models.
from app.models.fax_file import FaxFile
from app.models.patient import Patient


def parse_name_and_dob(ocr_text: str):
    """
    Attempts to extract a patient's first name, last name, and date of birth from OCR text.

    It first searches for lines starting with "Patient:" and "DOB:" or "Date of Birth:".
    If not found, it falls back to a pattern that looks for a two-word name near a DOB marker.

    Returns a tuple: (first_name, last_name, dob) where dob is a datetime.date object or None.
    """
    import re
    from datetime import datetime

    first_name = None
    last_name = None
    dob = None

    # Primary pattern: Look for "Patient:" followed by the name and a separate DOB marker.
    name_match = re.search(r"Patient:\s*(.+)", ocr_text, re.IGNORECASE)
    dob_match = re.search(r"(DOB|Date of Birth):\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})", ocr_text, re.IGNORECASE)

    if name_match and dob_match:
        # Use the first line that starts with "Patient:" for the name.
        full_name = name_match.group(1).strip()
        # Assume the first two words are the first and last names.
        name_parts = full_name.split()
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = name_parts[1]
        elif name_parts:
            first_name = name_parts[0]
            last_name = ""
        # Extract DOB string.
        dob_str = dob_match.group(2).strip()
        try:
            # Try parsing with '/' as delimiter.
            if len(dob_str.split('/')[-1]) == 4:
                dob = datetime.strptime(dob_str, "%m/%d/%Y").date()
            else:
                dob = datetime.strptime(dob_str, "%m/%d/%y").date()
        except Exception as e:
            try:
                # If that fails, try with '-' as delimiter.
                if len(dob_str.split('-')[-1]) == 4:
                    dob = datetime.strptime(dob_str, "%m-%d-%Y").date()
                else:
                    dob = datetime.strptime(dob_str, "%m-%d-%y").date()
            except Exception as e:
                print("Error parsing DOB:", e)

    else:
        # Fallback pattern: search for any two-word name near a DOB marker.
        fallback_match = re.search(
            r"([A-Za-z]+\s+[A-Za-z]+).*?(DOB|Date of Birth):\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})",
            ocr_text,
            re.IGNORECASE | re.DOTALL
        )
        if fallback_match:
            full_name = fallback_match.group(1).strip()
            name_parts = full_name.split()
            if len(name_parts) >= 2:
                first_name = name_parts[0]
                last_name = name_parts[1]
            elif name_parts:
                first_name = name_parts[0]
                last_name = ""
            dob_str = fallback_match.group(3).strip()
            try:
                if len(dob_str.split('/')[-1]) == 4:
                    dob = datetime.strptime(dob_str, "%m/%d/%Y").date()
                else:
                    dob = datetime.strptime(dob_str, "%m/%d/%y").date()
            except Exception as e:
                try:
                    if len(dob_str.split('-')[-1]) == 4:
                        dob = datetime.strptime(dob_str, "%m-%d-%Y").date()
                    else:
                        dob = datetime.strptime(dob_str, "%m-%d-%y").date()
                except Exception as e:
                    print("Fallback error parsing DOB:", e)

    return first_name, last_name, dob

async def fill_patient_ids():
    async with SessionLocal() as session:
        # Get all fax records that do not have a patient_id assigned
        result = await session.execute(select(FaxFile).where(FaxFile.patient_id.is_(None)))
        fax_files = result.scalars().all()

        updated_count = 0

        for fax in fax_files:
            if not fax.ocr_text:
                # Skip if no OCR text is present.
                continue

            # Parse the OCR text for name and DOB.
            first_name, last_name, dob = parse_name_and_dob(fax.ocr_text)
            if first_name and last_name and dob:
                # Search for a matching patient by name and DOB.
                result_patient = await session.execute(
                    select(Patient).where(
                        Patient.first_name == first_name,
                        Patient.last_name == last_name,
                        Patient.date_of_birth == dob
                    )
                )
                patient = result_patient.scalar_one_or_none()

                if patient:
                    fax.patient_id = patient.id
                    session.add(fax)
                    updated_count += 1
                    print(f"Updated fax id {fax.id} with patient id {patient.id}")
                else:
                    print(f"No matching patient found for fax id {fax.id} (Name: {first_name} {last_name}, DOB: {dob})")
            else:
                print(f"Could not parse name or DOB for fax id {fax.id}")

        # Commit all updates.
        await session.commit()
        print(f"Total fax records updated: {updated_count}")


if __name__ == "__main__":
    asyncio.run(fill_patient_ids())