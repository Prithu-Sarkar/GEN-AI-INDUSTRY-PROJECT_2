
from repositories.sqlite.base      import init_db
from repositories.sqlite.customers import CustomersRepository
from repositories.sqlite.tickets   import TicketsRepository
from repositories.sqlite.drafts    import DraftsRepository
_c=CustomersRepository(); _t=TicketsRepository(); _d=DraftsRepository()
def create_or_get_customer(e,n=None,co=None): return _c.create_or_get(e,n,co)
def get_customer_by_id(i):    return _c.get_by_id(i)
def create_ticket(ci,s,d,p="medium",st="open"): return _t.create(ci,s,d,p,st)
def list_tickets(l=100):      return _t.list(l)
def get_ticket_by_id(i):      return _t.get_by_id(i)
def set_ticket_status(i,s):   return _t.set_status(i,s)
def create_draft(ti,c,ctx=None,s="pending"): return _d.create(ti,c,ctx,s)
def get_latest_draft(ti):     return _d.get_latest_for_ticket(ti)
def update_draft(di,c=None,s=None): return _d.update(di,c,s)
def get_ticket_and_customer_by_draft(di): return _d.get_ticket_and_customer_by_draft(di)
