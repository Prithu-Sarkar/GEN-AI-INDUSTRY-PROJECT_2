
from __future__ import annotations
from repositories.sqlite.base import connect, row_to_dict

class TicketsRepository:
    def create(self,customer_id,subject,description,priority="medium",status="open"):
        with connect() as c:
            cur=c.execute("INSERT INTO tickets (customer_id,subject,description,priority,status) VALUES(?,?,?,?,?)",
                          (customer_id,subject,description,priority,status))
            return row_to_dict(c.execute("SELECT * FROM tickets WHERE id=?",(cur.lastrowid,)).fetchone())
    def list(self,limit=100):
        with connect() as c:
            rows=c.execute("SELECT t.*,cu.email AS customer_email,cu.name AS customer_name,cu.company AS customer_company "
                           "FROM tickets t JOIN customers cu ON cu.id=t.customer_id ORDER BY t.created_at DESC LIMIT ?",(limit,)).fetchall()
            return [dict(r) for r in rows]
    def get_by_id(self,tid):
        with connect() as c:
            row=c.execute("SELECT t.*,cu.email AS customer_email,cu.name AS customer_name,cu.company AS customer_company "
                          "FROM tickets t JOIN customers cu ON cu.id=t.customer_id WHERE t.id=?",(tid,)).fetchone()
            return row_to_dict(row)
    def set_status(self,tid,status):
        with connect() as c:
            c.execute("UPDATE tickets SET status=? WHERE id=?",(status,tid))
            return row_to_dict(c.execute("SELECT * FROM tickets WHERE id=?",(tid,)).fetchone())
    def count_open_for_customer(self,email):
        with connect() as c:
            row=c.execute("SELECT COUNT(*) AS n FROM tickets t JOIN customers cu ON cu.id=t.customer_id "
                          "WHERE cu.email=? AND t.status='open'",(email,)).fetchone()
            return int(row["n"]) if row else 0
