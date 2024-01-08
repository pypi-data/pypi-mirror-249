from clld.db.meta import Base, CustomModelMixin, PolymorphicBaseMixin
from clld.db.models import HasSourceMixin, IdNameDescriptionMixin, common
from clld.db.models.common import Contribution
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Unicode,
    UniqueConstraint,
    orm,
)
from sqlalchemy.orm import backref, relationship
from zope.interface import implementer

from clld_etymology_plugin.interfaces import (
    IBorrowing,
    ICognateset,
    ITree,
    IUnitCognate,
)


@implementer(ICognateset)
class Cognateset(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    @property
    def reflexes(self):
        res = []
        for field in ["units"]:
            res.extend(getattr(self, field))
        return res

    @property
    def languages(self):
        return list(set([reflex.counterpart.language for reflex in self.reflexes]))

    @property
    def form(self):
        from clld_etymology_plugin.util import get_etym_form

        return get_etym_form(self, self.name)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="cognatesets")


@implementer(IUnitCognate)
class UnitCognate(Base):
    cognateset_pk = Column(Integer, ForeignKey("cognateset.pk"))
    cognateset = orm.relationship(Cognateset, backref="units")
    counterpart_pk = Column(Integer, ForeignKey("unit.pk"))
    counterpart = orm.relationship(common.Unit, backref="cognates")
    doubt = Column(Boolean, default=False)
    alignment = Column(Unicode)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="unitcognates")


@implementer(ITree)
class Tree(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
    newick = Column(Unicode)


@implementer(IBorrowing)
class Borrowing(Base, IdNameDescriptionMixin):
    id = Column(String, unique=True)
    # unit_pk = Column(Integer, ForeignKey("unit.pk"), nullable=False)
    recipient_pk = Column(Integer, ForeignKey("unit.pk"))
    donor_pk = Column(Integer, ForeignKey("unit.pk"))
    comment = Column(Unicode)
    # area = Column(Unicode)
    reliability = Column(Unicode)
    # int_reliability = Column(Integer)
    # count_interrel = Column(Integer)
    # count_borrowed = Column(Integer)

    recipient = relationship(
        common.Unit,
        primaryjoin=recipient_pk == common.Unit.pk,
        backref="donor_assocs",
    )
    donor = relationship(
        common.Unit,
        primaryjoin=donor_pk == common.Unit.pk,
        backref="recipient_assocs",
    )
