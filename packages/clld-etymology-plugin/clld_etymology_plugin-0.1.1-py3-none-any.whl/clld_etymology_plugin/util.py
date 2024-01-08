import copy
from io import StringIO

from Bio import Phylo
from clld.db.meta import DBSession
from clld.db.models.common import Language, Parameter, Value
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML, literal

from clld_etymology_plugin import models

TREE = None
trees = list(DBSession.query(models.Tree))
if len(trees) > 0:
    ref_tree = trees[0]
    TREE = Phylo.read(
        StringIO(ref_tree.newick),
        format="newick",
    )
else:
    TREE = None


def iter_tree(clade, depth=0):
    if len(clade.get_terminals()) > 1:
        depth += 1
        yield (clade, False, depth)
        for child in clade.clades:
            for x in iter_tree(child, depth):
                yield x
    elif clade.is_terminal():
        depth -= 1
        yield (clade, True, depth)
    else:
        depth -= 1
        yield (clade, True, depth)


def lfts(request, form, lng=True, ftr=True, src=True, pre_f=""):
    lis = []
    if lng:
        lis.extend([link(request, form.language), " "])
    lis.extend([pre_f, link(request, form)])
    if ftr:
        lis.extend([" ‘", form.meanings[0].meaning, "’"])
    return HTML.span(*lis)


def etymology(request, form):
    etym_chain = []
    if form.donor_assocs:
        etym_chain.append(("bor", form.donor_assocs[0].donor))
    if form.cognates:
        cogset = form.cognates[0].cognateset
        cogdic = {}
        for reflex in cogset.reflexes:
            cogdic[reflex.counterpart.language.id] = reflex.counterpart
        chain = []
        for clade, is_leaf, depth in iter_tree(TREE.root):
            if clade.name == form.language.id:
                chain = [TREE.root] + TREE.get_path(clade)
        for clade in reversed(chain[0:-1]):
            if clade.name in cogdic:
                etym_chain.append(("inh", cogdic[clade.name]))
        return etym_chain
    return None


def etym_link(req, item, lfts=True):
    if item.donor_assocs:
        res = "↶ "
        res += link(
            req,
            item.donor_assocs[0],
            label=item.donor_assocs[0].donor.language.name
            + " "
            + f"‘{item.donor_assocs[0].donor.meanings[0].meaning.name}‘"
            if lfts
            else "" + item.donor_assocs[0].donor.name,
        )
        if item.cognates:
            if (
                item.cognates[0].cognateset
                == item.donor_assocs[0].donor.cognates[0].cognateset
            ):
                res += f" (" + link(req, item.cognates[0].cognateset) + ")"
            else:
                res += f" or " + link(req, item.cognates[0].cognateset)
        return res
    if item.cognates:
        return link(req, item.cognates[0].cognateset)
    return ""


def filtered_tree(tree, data):
    new_tree = copy.deepcopy(tree)
    internals = [x.name for x in new_tree.get_nonterminals()]
    for item in new_tree.get_terminals():
        if item.name not in data:
            try:
                new_tree.prune(item)
            except ValueError:
                return None
    for item in new_tree.get_terminals():
        if not item.clades and item.name in internals:
            new_tree.prune(item)
    return new_tree


def build_ul(request, coghits, clade):
    lis = []
    for child in clade.clades:
        if child == clade:
            continue
        if isinstance(coghits, dict):
            if child.name in coghits:
                cognates = coghits[child.name].cognates
                pre_str = ""
                if not child.is_terminal():
                    pre_str = "*"
                cogset_label = ""
                if len(cognates) > 0:
                    cogset_label = cognates[0].cognateset.id
                lis.append(
                    HTML.li(
                        link(request, coghits[child.name].language),
                        ": ",
                        pre_str,
                        HTML.i(
                            HTML.b(
                                link(request, coghits[child.name], cogset=cogset_label)
                            )
                        ),
                        class_="tree",
                    )
                )
            else:
                lg = list(DBSession.query(Language).filter(Language.id == child.name))
                if len(lg) > 0:
                    lis.append(HTML.li(lg[0], "", class_="tree"))
                else:
                    lis.append(HTML.li(child.name, "", class_="tree"))
        else:
            lg = list(DBSession.query(Language).filter(Language.id == child.name))
            if len(lg) > 0:
                lis.append(HTML.li(link(request, lg[0]), class_="tree"))
            else:
                lis.append(HTML.li(child.name, class_="tree"))
        if not child.is_terminal():
            lis.append(build_ul(request, coghits, child))
    return HTML.ul(*lis, class_="tree")


def family_tree(request):
    trees = list(DBSession.query(models.Tree))
    if len(trees) > 0:
        ref_tree = trees[0]
        tree = Phylo.read(
            StringIO(ref_tree.newick),
            format="newick",
        )
        return build_ul(request, "", tree.root)
    return HTML.div("No trees in database.")


def build_tree(request, cogset, mode="cogset"):
    trees = list(DBSession.query(models.Tree))
    if len(trees) > 0:
        ref_tree = trees[0]
        tree = Phylo.read(
            StringIO(ref_tree.newick),
            format="newick",
        )

        if mode == "cogset":
            coghits = {
                x.counterpart.language.id: x.counterpart for x in cogset.reflexes
            }
        else:
            coghits = {x.word.language.id: x.word for x in cogset.units}
        good_leafs = []
        for clade, is_leaf, depth in iter_tree(tree.root):
            if clade.name in coghits:
                good_leafs.append(clade.name)
        new_tree = tree
        new_tree = filtered_tree(tree, good_leafs)
        if new_tree:
            return build_ul(request, coghits, new_tree.root)
        return ""
    return HTML.div("No trees in database.")
