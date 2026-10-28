from database import get_connection


def get_resources(campus):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM resources
    WHERE campus = ?
    """, (campus,))

    resources = cursor.fetchall()

    conn.close()

    return resources