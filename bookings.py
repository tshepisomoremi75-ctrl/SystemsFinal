from database import get_connection


# ==========================================
# BOOKING CLASS
# ==========================================

class Booking:

    def __init__(
            self,
            lecturer,
            resource_code,
            booking_date,
            start_time,
            duration,
            campus):

        self.lecturer = lecturer
        self.resource_code = resource_code
        self.booking_date = booking_date
        self.start_time = start_time
        self.duration = duration
        self.campus = campus

    # ==================================
    # CHECK FOR OVERLAPPING BOOKINGS
    # ==================================

    def booking_exists(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM bookings
        WHERE resource_code = ?
        AND booking_date = ?
        AND start_time = ?
        """,
        (
            self.resource_code,
            self.booking_date,
            self.start_time
        ))

        booking = cursor.fetchone()

        conn.close()

        return booking is not None

    # ==================================
    # SAVE BOOKING
    # ==================================

    def save(self):

        if self.booking_exists():
            return False

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO bookings(
            lecturer,
            resource_code,
            booking_date,
            start_time,
            duration,
            campus
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            self.lecturer,
            self.resource_code,
            self.booking_date,
            self.start_time,
            self.duration,
            self.campus
        ))

        conn.commit()
        conn.close()

        return True


# ==================================
# GET ALL BOOKINGS FOR LECTURER
# ==================================

def get_lecturer_bookings(lecturer):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM bookings
    WHERE lecturer = ?
    ORDER BY booking_date,
             start_time
    """,
    (lecturer,))

    bookings = cursor.fetchall()

    conn.close()

    return bookings


# ==================================
# GET SINGLE BOOKING
# ==================================

def get_booking_by_id(booking_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM bookings
    WHERE id = ?
    """,
    (booking_id,)
    )

    booking = cursor.fetchone()

    conn.close()

    return booking


# ==================================
# CANCEL BOOKING
# ==================================

def cancel_booking(booking_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM bookings
    WHERE id = ?
    """,
    (booking_id,)
    )

    conn.commit()
    conn.close()

    return True


# ==================================
# UPDATE BOOKING
# ==================================

def update_booking(
        booking_id,
        booking_date,
        start_time,
        duration):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE bookings
    SET booking_date = ?,
        start_time = ?,
        duration = ?
    WHERE id = ?
    """,
    (
        booking_date,
        start_time,
        duration,
        booking_id
    ))

    conn.commit()
    conn.close()

    return True


# ==================================
# GET BOOKINGS BY CAMPUS
# ==================================

def get_bookings_by_campus(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM bookings
    WHERE campus = ?
    ORDER BY booking_date,
             start_time
    """,
    (campus,))

    bookings = cursor.fetchall()

    conn.close()

    return bookings


# ==================================
# GET ALL BOOKINGS
# ==================================

def get_all_bookings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM bookings
    ORDER BY booking_date,
             start_time
    """)

    bookings = cursor.fetchall()

    conn.close()

    return bookings


# ==================================
# TOTAL BOOKINGS
# ==================================

def total_bookings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM bookings
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result


# ==================================
# BOOKINGS PER CAMPUS
# ==================================

def campus_booking_count(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM bookings
    WHERE campus = ?
    """,
    (campus,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ==================================
# AVERAGE BOOKING DURATION
# ==================================

def average_booking_duration(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(duration)
    FROM bookings
    WHERE campus = ?
    """,
    (campus,))

    result = cursor.fetchone()[0]

    conn.close()

    if result is None:
        return 0

    return round(result, 2)


# ==================================
# MOST USED RESOURCE
# ==================================

def most_used_resource(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT resource_code,
           COUNT(*)
    FROM bookings
    WHERE campus = ?
    GROUP BY resource_code
    ORDER BY COUNT(*) DESC
    LIMIT 1
    """,
    (campus,))

    result = cursor.fetchone()

    conn.close()

    return result