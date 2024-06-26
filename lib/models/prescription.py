# lib/models/prescription.py

from models.__init__ import CURSOR, CONN

class Prescription:
    all = {}

    def __init__(self, prescription_id, patient_id, medicine_id, dosage, frequency):
        self.prescription_id = prescription_id
        self.patient_id = patient_id
        self.medicine_id = medicine_id
        self.dosage = dosage
        self.frequency = frequency

    def __repr__(self):
        return f"Prescription(ID: {self.id}, Patient ID: {self.patient_id}, Doctor ID: {self.doctor_id}, Medicine ID: {self.medicine_id}, Dosage: '{self.dosage}', Frequency: '{self.frequency}')"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS prescriptions(
            id INTEGER PRIMARY KEY,
            patient_id INTEGER,
            doctor_id INTEGER,
            medicine_id INTEGER,
            dosage TEXT,
            frequency TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (doctor_id) REFERENCES doctors (id),
            FOREIGN KEY (medicine_id) REFERENCES medicines (id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS prescriptions;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO prescriptions(patient_id, doctor_id, medicine_id, dosage, frequency)
            VALUES (?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.patient_id, self.doctor_id, self.medicine_id, self.dosage, self.frequency))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, patient_id, medicine_id, dosage, frequency):
        sql = """
            INSERT INTO prescriptions (patient_id, medicine_id, dosage, frequency)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (patient_id, medicine_id, dosage, frequency))
        CONN.commit()
        prescription_id = CURSOR.lastrowid
        return cls(prescription_id, patient_id, medicine_id, dosage, frequency)

    def update(self):
        sql = """
            UPDATE prescriptions
            SET patient_id = ?, doctor_id = ?, medicine_id = ?, dosage = ?, frequency = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.patient_id, self.doctor_id, self.medicine_id, self.dosage, self.frequency, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM prescriptions
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        prescription_id, patient_id, medicine_id, dosage, frequency = row
        return cls(prescription_id, patient_id, medicine_id, dosage, frequency)

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM prescriptions
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM prescriptions
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_patient_id(cls, patient_id):
        sql = """
            SELECT id, patient_id, medicine_id, dosage, frequency
            FROM prescriptions
            WHERE patient_id = ?
        """
        rows = CURSOR.execute(sql, (patient_id,)).fetchall()
        return [cls.instance_from_db(row) for row in rows] if rows else []

    