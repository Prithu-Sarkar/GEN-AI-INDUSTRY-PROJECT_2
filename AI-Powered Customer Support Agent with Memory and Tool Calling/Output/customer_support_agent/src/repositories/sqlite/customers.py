
from __future__ import annotations
from repositories.sqlite.base import connect, row_to_dict

class CustomersRepository:
    def create_or_get(self,email,name=None,company=None):
        """Upsert customer by email; backfill name/company if blank."""
        with connect() as c:
            row=c.execute("SELECT * FROM customers WHERE email=?",(email,)).fetchone()
            if row:
                ups,vals=[],[]
                if name and not row["name"]: ups.append("name=?"); vals.append(name)
                if company and not row["company"]: ups.append("company=?"); vals.append(company)
                if ups:
                    vals.append(email)
                    c.execute(f"UPDATE customers SET {', '.join(ups)} WHERE email=?",vals)
                return row_to_dict(c.execute("SELECT * FROM customers WHERE email=?",(email,)).fetchone())
            c.execute("INSERT INTO customers (email,name,company) VALUES(?,?,?)",(email,name,company))
            return row_to_dict(c.execute("SELECT * FROM customers WHERE email=?",(email,)).fetchone())
    def get_by_id(self,cid):
        with connect() as c: return row_to_dict(c.execute("SELECT * FROM customers WHERE id=?",(cid,)).fetchone())
    def get_by_email(self,email):
        with connect() as c: return row_to_dict(c.execute("SELECT * FROM customers WHERE email=?",(email,)).fetchone())
