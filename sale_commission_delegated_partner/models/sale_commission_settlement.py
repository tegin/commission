# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models


class SaleCommissionSettlement(models.Model):
    _inherit = "sale.commission.settlement"

    def _prepare_invoice(self, journal, product, date=False):
        vals = super()._prepare_invoice(journal, product, date=date)
        if not self.agent_id.delegated_agent_id:
            return vals
        invoice = self.env["account.move"].new(vals)
        invoice.partner_id = self.agent_id.delegated_agent_id
        invoice._onchange_partner_id()
        invoice._onchange_journal()
        for line in invoice.invoice_line_ids:
            line.name += "\n" + _("Agent: %s") % self.agent_id.display_name
        return invoice._convert_to_write(invoice._cache)
