# Copyright 2015 Tecnativa - Pedro M. Baeza
# Copyright 2016 Tecnativa - Carlos Dauden
# Copyright 2017 Tecnativa - David Vidal
# Copyright 2017 Tecnativa - Luis M. Ontalba
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import Form, TransactionCase


class TestPaymentReturn(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.journal = cls.env["account.journal"].create(
            {"name": "Test Sales Journal", "code": "tVEN", "type": "sale"}
        )
        cls.account = cls.env["account.account"].create(
            {
                "name": "Test account",
                "code": "TEST",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )
        cls.partner_expense = cls.env["res.partner"].create({"name": "PE"})
        cls.bank_journal = cls.env["account.journal"].create(
            {
                "name": "Test Bank Journal",
                "code": "BANK",
                "type": "bank",
                "default_expense_account_id": cls.account.id,
                "default_expense_partner_id": cls.partner_expense.id,
            }
        )
        cls.account_income = cls.env["account.account"].create(
            {
                "name": "Test income account",
                "code": "INCOME",
                "account_type": "income_other",
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "Test"})
        cls.invoice = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "journal_id": cls.journal.id,
                "company_id": cls.env.user.company_id.id,
                "currency_id": cls.env.user.company_id.currency_id.id,
                "partner_id": cls.partner.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": cls.account_income.id,
                            "name": "Test line",
                            "price_unit": 50,
                            "quantity": 10,
                            "tax_ids": False,
                        },
                    )
                ],
            }
        )
        cls.reason = cls.env["payment.return.reason"].create(
            {"code": "RTEST", "name": "Reason Test"}
        )
        cls.invoice.action_post()
        cls.receivable_line = cls.invoice.line_ids.filtered(
            lambda x: x.account_id.account_type == "asset_receivable"
        )
        # Create payment from invoice
        cls.payment_register_model = cls.env["account.payment.register"]
        payment_register = Form(
            cls.payment_register_model.with_context(
                active_model="account.move", active_ids=cls.invoice.ids
            )
        )
        cls.payment = payment_register.save()._create_payments()
        cls.payment_move = cls.payment.move_id
        cls.payment_line = cls.payment_move.line_ids.filtered(
            lambda x: x.account_id.account_type == "asset_receivable"
        )
        # Create payment return
        cls.payment_return = cls.env["payment.return"].create(
            {
                "journal_id": cls.bank_journal.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": cls.partner.id,
                            "move_line_ids": [(6, 0, cls.payment_line.ids)],
                            "amount": cls.payment_line.credit,
                            "expense_account": cls.account.id,
                            "expense_amount": 10.0,
                            "expense_partner_id": cls.partner.id,
                        },
                    )
                ],
            }
        )

    def test_confirm_error(self):
        self.payment_return.line_ids[0].move_line_ids = False
        with self.assertRaises(UserError):
            self.payment_return.action_confirm()

    def test_onchange_move_line(self):
        record = self.env["payment.return.line"].new()
        record.move_line_ids = self.payment_line.ids
        record._onchange_move_line()
        self.assertEqual(record.amount, self.payment_line.credit)

    def test_payment_return(self):
        self.payment_return.action_cancel()  # No effect
        self.assertEqual(self.invoice.payment_state, "paid")
        self.assertEqual(self.payment_return.state, "cancelled")
        self.payment_return.action_draft()
        self.assertEqual(self.payment_return.state, "draft")
        self.payment_return.line_ids[0].expense_amount = 20.0
        self.payment_return.line_ids[0]._onchange_expense_amount()
        self.payment_return.action_confirm()
        self.assertEqual(self.payment_return.state, "done")
        self.assertEqual(self.invoice.payment_state, "not_paid")
        self.assertEqual(self.invoice.amount_residual, self.receivable_line.debit)
        self.assertFalse(self.receivable_line.reconciled)
        self.assertEqual(
            self.payment_return.line_ids[0].expense_account,
            self.bank_journal.default_expense_account_id,
        )
        self.assertEqual(
            self.payment_return.line_ids[0].expense_partner_id,
            self.bank_journal.default_expense_partner_id,
        )
        self.assertEqual(len(self.payment_return.move_id.line_ids), 4)
        with self.assertRaises(UserError):
            self.payment_return.unlink()
        self.payment_return.action_cancel()
        self.assertEqual(self.payment_return.state, "cancelled")
        self.assertEqual(self.invoice.payment_state, "paid")
        self.assertTrue(self.receivable_line.reconciled)
        self.payment_return.action_draft()
        self.assertEqual(self.payment_return.state, "draft")
        self.payment_return.unlink()

    def test_payment_partial_return(self):
        self.payment_return.line_ids[0].amount = 500.0
        self.assertEqual(self.invoice.payment_state, "paid")
        self.payment_return.action_confirm()
        self.assertEqual(self.invoice.payment_state, "not_paid")
        self.assertEqual(self.invoice.amount_residual, 500.0)
        self.assertFalse(self.receivable_line.reconciled)
        self.payment_return.action_cancel()
        self.assertEqual(self.invoice.payment_state, "paid")
        self.assertTrue(self.receivable_line.reconciled)

    def test_find_match_invoice(self):
        self.payment_return.line_ids.write(
            {
                "partner_id": False,
                "move_line_ids": [(6, 0, [])],
                "amount": 0.0,
                "reference": self.invoice.name,
            }
        )
        self.payment_return.button_match()
        self.assertAlmostEqual(
            self.payment_return.line_ids[0].amount, self.payment_line.credit
        )

    def test_find_match_move_line(self):
        self.payment_line.name = "test match move line 001"
        self.payment_return.line_ids.write(
            {
                "partner_id": False,
                "move_line_ids": [(6, 0, [])],
                "amount": 0.0,
                "reference": self.payment_line.name,
            }
        )
        self.payment_return.button_match()
        self.assertEqual(
            self.payment_return.line_ids[0].partner_id.id,
            self.payment_line.partner_id.id,
        )

    def test_find_match_move(self):
        self.payment_move.name = "TESTMOVEXX01"
        self.payment_return.write(
            {
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": False,
                            "move_line_ids": [(6, 0, [])],
                            "amount": 0.0,
                            "reference": self.payment_move.name,
                        },
                    )
                ]
            }
        )
        with self.assertRaises(ValidationError):
            self.payment_return.button_match()

    def test_duplicate_lines(self):
        line_vals = {
            "partner_id": self.partner.id,
            "move_line_ids": [(6, 0, self.payment_line.ids)],
            "amount": self.payment_line.credit,
        }
        with self.assertRaises(ValidationError):
            self.payment_return.line_ids = [(0, 0, line_vals)]
        self.payment_return.action_confirm()
        with self.assertRaises(ValidationError):
            self.payment_return = self.env["payment.return"].create(
                {"journal_id": self.bank_journal.id, "line_ids": [(0, 0, line_vals)]}
            )

    def test_payments_widget(self):
        widget_vals = self.invoice.invoice_payments_widget
        self.assertEqual(len(widget_vals["content"]), 1)
        self.payment_return.action_confirm()
        info = self.invoice.invoice_payments_widget
        self.assertEqual(len(info["content"]), 2)
        self.assertEqual(info["content"][1]["amount"], -500.0)

    def test_reason_name_search(self):
        reason = self.env["payment.return.reason"]
        line = self.payment_return.line_ids[0]
        line.reason_id = reason.name_search("RTEST")[0]
        self.assertEqual(line.reason_id.name, "Reason Test")
        line.reason_id = reason.name_search("Reason Test")[0]
        self.assertEqual(line.reason_id.code, "RTEST")

    def test_compute_total(self):
        self.assertEqual(self.payment_return.total_amount, 500)
        self.payment_return.write(
            {
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": self.partner.id,
                            "amount": 10.5,
                            "expense_account": self.account.id,
                            "expense_partner_id": self.partner.id,
                        },
                    )
                ]
            }
        )
        self.assertEqual(self.payment_return.total_amount, 510.5)
