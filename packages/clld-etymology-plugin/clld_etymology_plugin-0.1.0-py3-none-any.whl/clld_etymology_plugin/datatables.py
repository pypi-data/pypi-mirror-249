from clld.db.models.common import Contribution, Language, Source, Unit
from clld.db.util import get_distinct_values, icontains
from clld.web.datatables.base import Col, DataTable, LinkCol
from clld.web.util.helpers import (
    JS_CLLD,
    JSDataTable,
    button,
    external_link,
    icon,
    link,
    linked_references,
)
from clld.web.util.htmllib import HTML, literal
from sqlalchemy.orm import aliased, joinedload

from clld_etymology_plugin.models import Borrowing


class Cognatesets(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name"), Col(self, "description")]


def includeme(config):
    config.register_datatable("cognatesets", Cognatesets)


class EtymologyCol(Col):
    def format(self, item):
        from clld_cognateset_plugin import util as cogutil

        return cogutil.etym_link(self.dt.req, item)

    def search(self, qs):
        return False
        return icontains(self.dt.donor.name, qs)

    def order(self):
        return 1
        return self.dt.donor.name


class Units(DataTable):
    __constraints__ = [Contribution, Language, Source]

    def base_query(self, query):
        query = super().base_query(query)
        # query = query.join(Contribution).options(joinedload(Word.contribution))
        if self.source:
            query = query.filter(Unit.source == self.source)
        if self.contribution:
            query = query.filter(Unit.contribution == self.contribution)
        if self.language:
            query = query.filter(Unit.language == self.language)
        return query

    def col_defs(self):
        base = [
            LinkCol(self, "name"),
        ]
        if not self.language:
            base.append(
                LinkCol(
                    self,
                    "language",
                    model_col=Language.name,
                    get_obj=lambda i: i.language,
                )
            )
        base.append(
            Col(
                self,
                "meaning",
                get_obj=lambda i: i.description,
            )
        )
        base.append(
            EtymologyCol(
                self,
                "etymology",
                # model_col=Word.name,
                # get_obj=lambda i: i.donor_assocs[0].donor,
            )
        )
        return base


class DonorCol(LinkCol):
    def get_obj(self, item):
        return item.donor.language

    def search(self, qs):
        return icontains(self.dt.donor.name, qs)

    def order(self):
        return self.dt.donor.name


class SourceCol(LinkCol):
    def get_obj(self, item):
        return item.donor


class RecipientCol(LinkCol):
    def get_obj(self, item):
        return item.recipient.language

    def search(self, qs):
        return icontains(self.dt.recipient.name, qs)

    def order(self):
        return self.dt.recipient.name


class TargetCol(LinkCol):
    def get_obj(self, item):
        return item.recipient


class DetailsRowCol(Col):

    """Render a button to open a details row on the fly.

    .. seealso:: http://www.datatables.net/examples/api/row_details.html
    """

    __kw__ = {
        "bSearchable": False,
        "bSortable": False,
        "sClass": "center",
        "sType": "html",
        "sTitle": "Details",
        "button_text": "more",
    }

    def format(self, item):
        return HTML.a(
            icon("info-sign"),
            title="More",
            href=self.dt.req.resource_url(self.get_obj(item)),
            class_="btn",
        )


class Borrowings(DataTable):
    def __init__(self, *args, **kw):
        super(Borrowings, self).__init__(*args, **kw)
        self.donor = aliased(Language)
        self.recipient = aliased(Language)

    def base_query(self, query):
        return query.join(self.donor, self.donor.pk == Borrowing.donor_pk).join(
            self.recipient, self.recipient.pk == Borrowing.recipient_pk
        )

    def col_defs(self):
        return [
            DonorCol(self, "donor", sTitle="Donor language"),
            SourceCol(self, "donor", sTitle="Source Form"),
            RecipientCol(self, "recipient", sTitle="Recipient language"),
            TargetCol(self, "donor", sTitle="Target form"),
            DetailsRowCol(self, "d"),
        ]
