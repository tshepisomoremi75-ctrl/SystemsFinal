from database import get_connection


def total_bookings(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM bookings
    WHERE campus = ?
    """, (campus,))

    total = cursor.fetchone()[0]

    conn.close()

    return total


def compare_campuses():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT campus,
           COUNT(*)
    FROM bookings
    GROUP BY campus
    """)

    data = cursor.fetchall()

    conn.close()

    return data