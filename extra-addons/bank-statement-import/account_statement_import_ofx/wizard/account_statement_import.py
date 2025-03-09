import io
import logging
import base64

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from ofxparse import OfxParser
except ImportError:
    _logger.debug("ofxparse not found.")
    OfxParser = None


class AccountStatementImport(models.TransientModel):
    _inherit = "account.statement.import"

    def _import_file(self):
        file_extension = self.statement_filename.split('.')[-1]
        if file_extension != 'ofx':
            return super(AccountStatementImport, self)._import_file()
        else:
            data_file = base64.b64decode(self.statement_file)
            corrected_data = data_file.replace(b'ENCODING: UTF - 8', b'ENCODING: UTF-8')
            ofx_data = self._parse_file(corrected_data)
            vals = self._prepare_create_attachment(ofx_data)
            self.env["ir.attachment"].create(vals)
            return ofx_data
    
    @api.model
    def _check_ofx(self, data_file):
        if not OfxParser:
            return False
        try:
            ofx = OfxParser.parse(io.BytesIO(data_file))
        except Exception as e:
            _logger.debug(e)
            return False
        return ofx

    @api.model
    def _prepare_ofx_transaction_line(self, transaction):
        # Since ofxparse doesn't provide account numbers,
        # we cannot provide the key 'bank_account_id',
        # nor the key 'account_number'
        # If you read odoo10/addons/account_bank_statement_import/
        # account_bank_statement_import.py, it's the only 2 keys
        # we can provide to match a partner.
        payment_ref = transaction.payee
        if transaction.checknum:
            payment_ref += " " + transaction.checknum
        if transaction.memo:
            payment_ref += " : " + transaction.memo
        vals = {
            "date": transaction.date,
            "payment_ref": payment_ref,
            "amount": float(transaction.amount),
            "unique_import_id": transaction.id,
        }
        return vals

    def _parse_file(self, data_file):
        ofx = self._check_ofx(data_file)
        if not ofx:
            return super()._parse_file(data_file)

        result = []
        try:
            for account in ofx.accounts:
                transactions = []
                total_amt = 0.00

                if not account.statement.transactions:
                    continue

                for transaction in account.statement.transactions:
                    vals = self._prepare_ofx_transaction_line(transaction)
                    if vals:
                        transactions.append(vals)
                        total_amt += vals["amount"]
                if total_amt:
                    balance = total_amt
                elif account.statement.balance:
                    balance = float(account.statement.balance)
                else:
                    balance = 0
                vals_bank_statement = {
                    "name": account.number,
                    "transactions": transactions,
                    "balance_start": balance - total_amt,
                    "balance_end_real": balance,
                }
                result.append(
                    (account.statement.currency, account.number, [vals_bank_statement])
                )
        except Exception as e:
            raise UserError(
                _(
                    "The following problem occurred during import. "
                    "The file might not be valid.\n\n %s"
                )
                % str(e)
            ) from e
        return result
