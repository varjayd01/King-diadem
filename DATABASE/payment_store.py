from DATABASE.db import get_conn

def payment_exists(payment_id):

    conn=get_conn()
    c=conn.cursor()

    c.execute("SELECT id FROM payments WHERE id=?", (payment_id,))
    row=c.fetchone()

    conn.close()

    return row is not None


def record_payment(payment_id):

    conn=get_conn()
    c=conn.cursor()

    c.execute(
        "INSERT INTO payments(id) VALUES(?)",
        (payment_id,)
    )

    conn.commit()
    conn.close()
