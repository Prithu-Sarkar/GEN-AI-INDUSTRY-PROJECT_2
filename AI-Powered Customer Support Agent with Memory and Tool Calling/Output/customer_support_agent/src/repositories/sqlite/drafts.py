
from __future__ import annotations
from repositories.sqlite.base import connect, row_to_dict

class DraftsRepository:
    def create(self,ticket_id,content,context_used=None,status="pending"):
        with connect() as c:
            cur=c.execute("INSERT INTO drafts (ticket_id,content,context_used,status) VALUES(?,?,?,?)",
                          (ticket_id,content,context_used,status))
            return row_to_dict(c.execute("SELECT * FROM drafts WHERE id=?",(cur.lastrowid,)).fetchone())
    def get_latest_for_ticket(self,tid):
        with connect() as c:
            return row_to_dict(c.execute("SELECT * FROM drafts WHERE ticket_id=? ORDER BY created_at DESC LIMIT 1",(tid,)).fetchone())
    def get_by_id(self,did):
        with connect() as c: return row_to_dict(c.execute("SELECT * FROM drafts WHERE id=?",(did,)).fetchone())
    def update(self,did,content=None,status=None):
        ups,vals=[],[]
        if content is not None: ups.append("content=?"); vals.append(content)
        if status  is not None: ups.append("status=?");  vals.append(status)
        if not ups: return self.get_by_id(did)
        with connect() as c:
            vals.append(did)
            c.execute(f"UPDATE drafts SET {', '.join(ups)} WHERE id=?",vals)
            return row_to_dict(c.execute("SELECT * FROM drafts WHERE id=?",(did,)).fetchone())
    def get_ticket_and_customer_by_draft(self,did):
        with connect() as c:
            row=c.execute("SELECT d.id AS draft_id,d.ticket_id,d.content AS draft_content,d.status AS draft_status,"
                          "t.subject,t.description,t.status AS ticket_status,"
                          "cu.id AS customer_id,cu.email AS customer_email,cu.name AS customer_name,cu.company AS customer_company "
                          "FROM drafts d JOIN tickets t ON t.id=d.ticket_id JOIN customers cu ON cu.id=t.customer_id "
                          "WHERE d.id=?",(did,)).fetchone()
            return row_to_dict(row)
