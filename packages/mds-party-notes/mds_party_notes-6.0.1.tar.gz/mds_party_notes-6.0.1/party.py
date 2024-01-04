# -*- coding: utf-8 -*-
# This file is part of the party-notes module for Tryton from m-ds.de.
# The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from sql.conditionals import Case
from sql.functions import Function, Substring, CharLength


class Concat2(Function):
    """ concat columns
    """
    __slots__ = ()
    _function = 'concat'

# end Concat2


class Replace(Function):
    """ replace substrings
    """
    __slots__ = ()
    _function = 'replace'

# end Replace


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    notizen = fields.Text(string='Notes')
    notizen_tree = fields.Function(fields.Char(
        string='Notes', readonly=True),
        'get_notizen_tree', searcher='search_notizen_tree')

    @classmethod
    def get_notizen_tree(cls, notes, names):
        """ get notes for selected parties
        """
        tab_party = cls.__table__()
        cursor = Transaction().connection.cursor()
        result = {x: {y.id: None for y in notes} for x in names}

        query = tab_party.select(
                    tab_party.id,
                    Case(
                        (CharLength(tab_party.notizen) > 40,
                            Concat2(Substring(Replace(
                                tab_party.notizen, '\n', '; '),
                                1, 40), '...')),
                        else_=Replace(tab_party.notizen, '\n', '; ')
                    ).as_('shorttext'),
                    where=tab_party.id.in_([x.id for x in notes]))

        cursor.execute(*query)
        records = cursor.fetchall()

        for record in records:
            values = {
                'notizen_tree': record[1],
                }
            for name in names:
                result[name][record[0]] = values[name]
        return result

    @classmethod
    def search_notizen_tree(cls, name, clause):
        """ search in fulltext
        """
        return [('notizen',) + tuple(list(clause)[1:])]

    @staticmethod
    def order_notizen_tree(tables):
        table, _ = tables[None]
        return [table.notizen]

# ende Party
