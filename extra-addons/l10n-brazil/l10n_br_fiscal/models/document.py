# Copyright (C) 2013  Renato Lima - Akretion
# Copyright (C) 2019  KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from ast import literal_eval

from erpbrasil.base.fiscal.edoc import ChaveEdoc

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from ..constants.fiscal import (
    DOCUMENT_ISSUER,
    DOCUMENT_ISSUER_COMPANY,
    DOCUMENT_ISSUER_DICT,
    DOCUMENT_ISSUER_PARTNER,
    EDOC_PURPOSE,
    EDOC_PURPOSE_NORMAL,
    FISCAL_IN_OUT_DICT,
    MODELO_FISCAL_CTE,
    MODELO_FISCAL_NFCE,
    MODELO_FISCAL_NFE,
    MODELO_FISCAL_NFSE,
    SITUACAO_EDOC,
    SITUACAO_EDOC_AUTORIZADA,
    SITUACAO_EDOC_CANCELADA,
    SITUACAO_EDOC_DENEGADA,
    SITUACAO_EDOC_EM_DIGITACAO,
    SITUACAO_EDOC_INUTILIZADA,
    SITUACAO_FISCAL,
)


class Document(models.Model):
    """Implementação base dos documentos fiscais

    Devemos sempre ter em mente que o modelo que vai usar este módulo abstrato
     tem diversos metodos importantes e a intenção que os módulos da OCA que
     extendem este modelo, funcionem se possível sem a necessidade de
     codificação extra.

    É preciso também estar atento que o documento fiscal tem dois estados:

    - Estado do documento eletrônico / não eletônico: state_edoc
    - Estado FISCAL: state_fiscal

    O estado fiscal é um campo que é alterado apenas algumas vezes pelo código
    e é de responsabilidade do responsável fiscal pela empresa de manter a
    integridade do mesmo, pois ele não tem um fluxo realmente definido e
    interfere no lançamento do registro no arquivo do SPED FISCAL.
    """

    _name = "l10n_br_fiscal.document"
    _inherit = [
        "l10n_br_fiscal.document.mixin.fields",
        "l10n_br_fiscal.document.move.mixin",
        "mail.thread",
    ]
    _description = "Fiscal Document"
    _check_company_auto = True

    name = fields.Char(
        compute="_compute_name",
        store=True,
        index=True,
    )

    state_edoc = fields.Selection(
        selection=SITUACAO_EDOC,
        string="Situação e-doc",
        default=SITUACAO_EDOC_EM_DIGITACAO,
        copy=False,
        required=True,
        readonly=True,
        # tracking=True,
        index=True,
    )

    state_fiscal = fields.Selection(
        selection=SITUACAO_FISCAL,
        string="Situação Fiscal",
        copy=False,
        # tracking=True,
        index=True,
    )

    fiscal_operation_id = fields.Many2one(
        domain="[('state', '=', 'approved'), "
        "'|', ('fiscal_operation_type', '=', fiscal_operation_type),"
        " ('fiscal_operation_type', '=', 'all')]",
    )

    fiscal_operation_type = fields.Selection(
        store=True,
    )

    rps_number = fields.Char(
        string="RPS Number",
        copy=False,
        index=True,
        unaccent=False,
    )

    document_date = fields.Datetime(
        copy=False,
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        index=True,
        default=lambda self: self.env.user,
    )

    operation_name = fields.Char(
        copy=False,
    )

    document_electronic = fields.Boolean(
        related="document_type_id.electronic",
        string="Electronic?",
        store=True,
    )

    date_in_out = fields.Datetime(
        string="Date IN/OUT",
        copy=False,
    )

    document_related_ids = fields.One2many(
        comodel_name="l10n_br_fiscal.document.related",
        inverse_name="document_id",
        string="Fiscal Document Related",
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
    )

    partner_shipping_id = fields.Many2one(
        comodel_name="res.partner",
        string="Shipping Address",
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )

    fiscal_line_ids = fields.One2many(
        comodel_name="l10n_br_fiscal.document.line",
        inverse_name="document_id",
        string="Document Lines",
        copy=True,
        check_company=True,
    )

    edoc_purpose = fields.Selection(
        selection=EDOC_PURPOSE,
        string="Finalidade",
        default=EDOC_PURPOSE_NORMAL,
    )

    document_type = fields.Char(
        string="Document Type Code",
        related="document_type_id.code",
        store=True,
    )

    imported_document = fields.Boolean(string="Imported", default=False)

    xml_error_message = fields.Text(
        readonly=True,
        string="XML validation errors",
        copy=False,
    )

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        compute="_compute_currency_id",
    )

    # this related "state" field is required for the status bar widget
    # while state_edoc avoids colliding with the state field
    # of objects where the fiscal mixin might be injected.
    state = fields.Selection(related="state_edoc", string="State")

    issuer = fields.Selection(
        selection=DOCUMENT_ISSUER,
        default=DOCUMENT_ISSUER_COMPANY,
    )

    document_subsequent_ids = fields.One2many(
        comodel_name="l10n_br_fiscal.subsequent.document",
        inverse_name="source_document_id",
        copy=True,
    )

    document_subsequent_generated = fields.Boolean(
        string="Subsequent documents generated?",
        compute="_compute_document_subsequent_generated",
        default=False,
    )

    transport_modal = fields.Selection(
        selection=[
            ("01", "Rodoviário"),
            ("02", "Aéreo"),
            ("03", "Aquaviário"),
            ("04", "Ferroviário"),
            ("05", "Dutoviário"),
            ("06", "Multimodal"),
        ],
        string="Modal de Transporte",
    )

    service_provider = fields.Selection(
        selection=[
            ("0", "Remetente"),
            ("1", "Expedidor"),
            ("2", "Recebedor"),
            ("3", "Destinatário"),
            ("4", "Outros"),
        ],
        string="Tomador do Serviço",
    )

    @api.constrains("document_key")
    def _check_key(self):
        for record in self:
            if not record.document_key:
                return

            documents = record.env["l10n_br_fiscal.document"].search_count(
                [
                    ("id", "!=", record.id),
                    ("company_id", "=", record.company_id.id),
                    ("issuer", "=", record.issuer),
                    ("document_key", "=", record.document_key),
                    (
                        "document_type",
                        "in",
                        (
                            MODELO_FISCAL_CTE,
                            MODELO_FISCAL_NFCE,
                            MODELO_FISCAL_NFE,
                            MODELO_FISCAL_NFSE,
                        ),
                    ),
                    ("state", "!=", "cancelada"),
                ]
            )

            if documents:
                raise ValidationError(
                    _(
                        "There is already a fiscal document with this " "key: {} !"
                    ).format(record.document_key)
                )
            else:
                ChaveEdoc(chave=record.document_key, validar=True)

    @api.constrains("document_number")
    def _check_number(self):
        for record in self:
            if not record.document_number:
                return
            domain = [
                ("id", "!=", record.id),
                ("company_id", "=", record.company_id.id),
                ("issuer", "=", record.issuer),
                ("document_type_id", "=", record.document_type_id.id),
                ("document_serie", "=", record.document_serie),
                ("document_number", "=", record.document_number),
            ]

            invalid_number = False

            if record.issuer == DOCUMENT_ISSUER_PARTNER:
                domain.append(("partner_id", "=", record.partner_id.id))
            else:
                if record.document_serie_id:
                    invalid_number = record.document_serie_id._is_invalid_number(
                        record.document_number
                    )

            documents = record.env["l10n_br_fiscal.document"].search_count(domain)

            if documents or invalid_number:
                raise ValidationError(
                    _(
                        "There is already a fiscal document with this "
                        "Serie: %(serie)s, Number: %(number)s!",
                        serie=record.document_serie,
                        number=record.document_number,
                    )
                )

    @api.depends("company_id")
    def _compute_currency_id(self):
        for doc in self:
            doc.currency_id = doc.company_id.currency_id or self.env.company.currency_id

    def _compute_document_name(self):
        self.ensure_one()
        name = ""
        type_serie_number = ""

        if self.document_type:
            type_serie_number += self.document_type
        if self.document_serie:
            type_serie_number += "/" + self.document_serie.zfill(3)
        if self.document_number or self.rps_number:
            type_serie_number += "/" + (self.document_number or self.rps_number)

        if self._context.get("fiscal_document_complete_name"):
            name += DOCUMENT_ISSUER_DICT.get(self.issuer, "")
            if self.issuer == DOCUMENT_ISSUER_COMPANY and self.fiscal_operation_type:
                name += "/" + FISCAL_IN_OUT_DICT.get(self.fiscal_operation_type, "")
            name += "/" + type_serie_number
            if self.document_date:
                name += " - " + self.document_date.strftime("%d/%m/%Y")
            if not self.partner_cnpj_cpf:
                name += " - " + _("Unidentified Consumer")
            elif self.partner_legal_name:
                name += " - " + self.partner_legal_name
                name += " - " + self.partner_cnpj_cpf
            else:
                name += " - " + self.partner_name
                name += " - " + self.partner_cnpj_cpf
        elif self._context.get("fiscal_document_no_company"):
            name += type_serie_number
        else:
            name += "{name}/{type_serie_number}".format(
                name=self.company_name or "",
                type_serie_number=type_serie_number,
            )
        return name

    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, record._compute_document_name()))
        return res

    @api.depends(
        "issuer",
        "fiscal_operation_type",
        "document_type",
        "document_serie",
        "document_number",
        "document_date",
        "partner_id",
    )
    def _compute_name(self):
        for r in self:
            r.name = r._compute_document_name()

    @api.depends(
        "fiscal_line_ids.estimate_tax",
        "fiscal_line_ids.price_gross",
        "fiscal_line_ids.amount_untaxed",
        "fiscal_line_ids.amount_tax",
        "fiscal_line_ids.amount_taxed",
        "fiscal_line_ids.amount_total",
        "fiscal_line_ids.financial_total",
        "fiscal_line_ids.financial_total_gross",
        "fiscal_line_ids.financial_discount_value",
        "fiscal_line_ids.amount_tax_included",
        "fiscal_line_ids.amount_tax_not_included",
        "fiscal_line_ids.amount_tax_withholding",
    )
    def _compute_fiscal_amount(self):
        return super()._compute_fiscal_amount()

    def unlink(self):
        forbidden_states_unlink = [
            SITUACAO_EDOC_AUTORIZADA,
            SITUACAO_EDOC_CANCELADA,
            SITUACAO_EDOC_DENEGADA,
            SITUACAO_EDOC_INUTILIZADA,
        ]

        for record in self.filtered(lambda d: d.state_edoc in forbidden_states_unlink):
            raise ValidationError(
                _(
                    "You cannot delete fiscal document number %(number)s with "
                    "the status: %(state)s!",
                    number=record.document_number,
                    state=record.state_edoc,
                )
            )

        return super().unlink()

    def _create_return(self):
        return_docs = self.env[self._name]
        for record in self:
            fsc_op = record.fiscal_operation_id.return_fiscal_operation_id
            if not fsc_op:
                raise ValidationError(
                    _(
                        "The fiscal operation {} has no return Fiscal "
                        "Operation defined"
                    ).format(record.fiscal_operation_id)
                )

            new_doc = record.copy()
            new_doc.fiscal_operation_id = fsc_op
            new_doc._onchange_fiscal_operation_id()

            for line in new_doc.fiscal_line_ids:
                fsc_op_line = line.fiscal_operation_id.return_fiscal_operation_id
                if not fsc_op_line:
                    raise ValidationError(
                        _(
                            "The fiscal operation {} has no return Fiscal "
                            "Operation defined"
                        ).format(line.fiscal_operation_id)
                    )
                line.fiscal_operation_id = fsc_op_line
                line._onchange_fiscal_operation_id()
                line._onchange_fiscal_operation_line_id()

            return_docs |= new_doc
        return return_docs

    def action_create_return(self):
        action = self.env.ref("l10n_br_fiscal.document_all_action").read()[0]
        return_docs = self._create_return()

        if return_docs:
            action["domain"] = literal_eval(action["domain"] or "[]")
            action["domain"].append(("id", "in", return_docs.ids))

        return action

    # the following actions are meant to be implemented in other modules such as
    # l10n_br_fiscal_edi. They are defined here so they can be overriden in modules
    # that don't depend on l10n_br_fiscal_edi (such as l10n_br_account).
    def view_pdf(self):
        pass

    def view_xml(self):
        pass

    def action_document_confirm(self):
        pass

    def action_document_send(self):
        pass

    def action_document_back2draft(self):
        pass

    def action_document_cancel(self):
        pass

    def action_document_invalidate(self):
        pass

    def action_document_correction(self):
        pass

    def exec_after_SITUACAO_EDOC_DENEGADA(self, old_state, new_state):
        # see https://github.com/OCA/l10n-brazil/pull/3272
        pass

    def _get_email_template(self, state):
        self.ensure_one()
        return self.document_type_id.document_email_ids.search(
            [
                "|",
                ("state_edoc", "=", False),
                ("state_edoc", "=", state),
                ("issuer", "=", self.issuer),
                "|",
                ("document_type_id", "=", False),
                ("document_type_id", "=", self.document_type_id.id),
            ],
            limit=1,
            order="state_edoc, document_type_id",
        ).mapped("email_template_id")

    def send_email(self, state):
        self.ensure_one()
        email_template = self._get_email_template(state)
        if email_template:
            email_template.with_context(
                default_attachment_ids=self._get_mail_attachment()
            ).send_mail(self.id)

    def _after_change_state(self, old_state, new_state):
        self.ensure_one()
        result = super()._after_change_state(old_state, new_state)
        self.send_email(new_state)
        return result

    @api.onchange("fiscal_operation_id")
    def _onchange_fiscal_operation_id(self):
        result = super()._onchange_fiscal_operation_id()
        if self.fiscal_operation_id:
            self.fiscal_operation_type = self.fiscal_operation_id.fiscal_operation_type
            self.edoc_purpose = self.fiscal_operation_id.edoc_purpose

        if self.issuer == DOCUMENT_ISSUER_COMPANY and not self.document_type_id:
            self.document_type_id = self.company_id.document_type_id

        subsequent_documents = [(6, 0, {})]
        for subsequent_id in self.fiscal_operation_id.mapped(
            "operation_subsequent_ids"
        ):
            subsequent_documents.append(
                (
                    0,
                    0,
                    {
                        "source_document_id": self.id,
                        "subsequent_operation_id": subsequent_id.id,
                        "fiscal_operation_id": subsequent_id.subsequent_operation_id.id,
                    },
                )
            )
        self.document_subsequent_ids = subsequent_documents
        return result

    def _prepare_referenced_subsequent(self, doc_referenced):
        self.ensure_one()
        return {
            "document_id": self.id,
            "document_related_id": doc_referenced.id,
            "document_type_id": doc_referenced.document_type_id.id,
            "document_serie": doc_referenced.document_serie,
            "document_number": doc_referenced.document_number,
            "document_date": doc_referenced.document_date,
            "document_key": doc_referenced.document_key,
        }

    def _document_reference(self, documents_referenced):
        self.ensure_one()
        for doc_referenced in documents_referenced:
            self.env["l10n_br_fiscal.document.related"].create(
                self._prepare_referenced_subsequent(doc_referenced)
            )

    @api.depends("document_subsequent_ids.subsequent_document_id")
    def _compute_document_subsequent_generated(self):
        for document in self:
            if not document.document_subsequent_ids:
                document.document_subsequent_generated = False
            else:
                document.document_subsequent_generated = all(
                    subsequent_id.operation_performed
                    for subsequent_id in document.document_subsequent_ids
                )

    def _generates_subsequent_operations(self):
        for record in self.filtered(lambda doc: not doc.document_subsequent_generated):
            for subsequent_id in record.document_subsequent_ids.filtered(
                lambda doc_sub: doc_sub._confirms_document_generation()
            ):
                subsequent_id.generate_subsequent_document()

    def cancel_edoc(self):
        self.ensure_one()
        if any(
            doc.state_edoc == SITUACAO_EDOC_AUTORIZADA
            for doc in self.document_subsequent_ids.mapped("document_subsequent_ids")
        ):
            message = _(
                "Canceling the document is not allowed: one or more "
                "associated documents have already been authorized."
            )
            raise UserWarning(message)

    def _get_mail_attachment(self):
        self.ensure_one()
        attachment_ids = []
        if self.state_edoc == SITUACAO_EDOC_AUTORIZADA:
            if self.file_report_id:
                attachment_ids.append(self.file_report_id.id)
            if self.authorization_file_id:
                attachment_ids.append(self.authorization_file_id.id)
        return attachment_ids

    def action_send_email(self):
        """Open a window to compose an email, with the fiscal document_type
        template message loaded by default
        """
        self.ensure_one()
        template = self._get_email_template(self.state)
        compose_form = self.env.ref("mail.email_compose_message_wizard_form", False)
        lang = self.env.context.get("lang")
        if template and template.lang:
            lang = template._render_template(template.lang, self._name, [self.id])
        self = self.with_context(lang=lang)
        ctx = dict(
            default_model="l10n_br_fiscal.document",
            default_res_id=self.id,
            default_use_template=bool(template),
            default_attachment_ids=self._get_mail_attachment(),
            default_template_id=template and template.id or False,
            default_composition_mode="comment",
            model_description=self.document_type_id.name or self._name,
            force_email=True,
        )
        return {
            "name": _("Send Fiscal Document Email Notification"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }
