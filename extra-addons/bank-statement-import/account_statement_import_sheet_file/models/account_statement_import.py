# Copyright 2020 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountStatementImport(models.TransientModel):
    _inherit = "account.statement.import"

    def _get_default_mapping_id(self):
        return (
            self.env["account.journal"]
            .browse(self.env.context.get("journal_id"))
            .default_sheet_mapping_id
        )

    sheet_mapping_id = fields.Many2one(
        string="Sheet mapping",
        comodel_name="account.statement.import.sheet.mapping",
        default=_get_default_mapping_id,
    )

    def _parse_file(self, data_file):
        self.ensure_one()
        try:
            if self.sheet_mapping_id:
                filename = self.statement_filename
                file_extension = filename.split('.')[1]
                if file_extension in ['xlsx','csv','txt']:
                    Parser = self.env["account.statement.import.sheet.parser"]
                    parsed_data = Parser.parse(
                        data_file, self.sheet_mapping_id, self.statement_filename
                    )
                    return parsed_data
            return super()._parse_file(data_file)
        except BaseException as exc:
            if self.env.context.get("account_statement_import_sheet_file_test"):
                raise
            _logger.warning("Sheet parser error", exc_info=True)
            raise UserError(_("Bad file/mapping: ") + str(exc)) from exc

    def _create_bank_statements(self, stmts_vals, result):
        """Set balance_end_real if not already provided by the file."""
        res = super()._create_bank_statements(stmts_vals, result)
        statements = self.env["account.bank.statement"].browse(result["statement_ids"])
        for statement in statements:
            if not statement.balance_end_real:
                amount = sum(statement.line_ids.mapped("amount"))
                statement.balance_end_real = statement.balance_start + amount
        return res
