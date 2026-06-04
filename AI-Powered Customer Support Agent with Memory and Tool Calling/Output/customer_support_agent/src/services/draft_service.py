
from __future__ import annotations
import json, logging
from repositories.sqlite.customers import CustomersRepository
from repositories.sqlite.drafts    import DraftsRepository
from repositories.sqlite.tickets   import TicketsRepository
from services.copilot_service      import SupportCopilot
logger=logging.getLogger(__name__)

class DraftService:
    def generate_and_store(self,ticket_id,tickets_repo,customers_repo,drafts_repo,copilot):
        """Fetch ticket+customer, call AI copilot, persist draft to DB."""
        ticket=tickets_repo.get_by_id(ticket_id)
        customer=customers_repo.get_by_id(ticket["customer_id"]) if ticket else None
        if not ticket or not customer: return None
        try:
            res=copilot.generate_draft(ticket=ticket,customer=customer)
            text,ctx=self._norm(res)
            return drafts_repo.create(ticket_id=ticket_id,content=text,
                                      context_used=json.dumps(ctx),status="pending")
        except Exception as e:
            logger.exception("Draft failed ticket_id=%s",ticket_id)
            return drafts_repo.create(ticket_id=ticket_id,
                content="Draft generation failed. Please retry.",
                context_used=json.dumps({"errors":[str(e)]}),status="failed")

    def accept_draft(self,draft_id,drafts_repo,copilot,new_content=None):
        """Accept draft: update status, save resolution to memory."""
        info=drafts_repo.get_ticket_and_customer_by_draft(draft_id)
        if not info: return None
        content=new_content or info["draft_content"]
        updated=drafts_repo.update(draft_id,content=content,status="accepted")
        if updated:
            ctx=json.loads(updated.get("context_used") or "{}")
            try:
                copilot.save_accepted_resolution(
                    customer_email=info["customer_email"],
                    customer_company=info.get("customer_company"),
                    ticket_subject=info["subject"],
                    ticket_description=info["description"],
                    draft_content=content,context_used=ctx)
            except Exception as e: logger.warning("Memory save failed: %s",e)
        return updated

    def discard_draft(self,draft_id,drafts_repo):
        return drafts_repo.update(draft_id,status="discarded")

    def serialize_draft(self,draft):
        raw=draft.get("context_used")
        ctx=None
        if raw:
            try: ctx=json.loads(raw)
            except: ctx={"raw":raw}
        return {"id":draft["id"],"ticket_id":draft["ticket_id"],
                "content":draft["content"],"context_used":ctx,
                "status":draft["status"],"created_at":draft["created_at"]}

    @staticmethod
    def _norm(result):
        text=str(result.get("draft") or "").strip()
        ctx=result.get("context_used") or {}
        if not isinstance(ctx,dict): ctx={"raw":str(ctx)}
        if not text:
            text="Thank you for reaching out. We are reviewing your issue."
            ctx.setdefault("errors",[]).append("Empty draft; fallback text used.")
        return text,ctx
