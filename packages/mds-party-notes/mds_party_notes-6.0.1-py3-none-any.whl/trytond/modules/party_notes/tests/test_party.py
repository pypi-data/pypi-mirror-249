# -*- coding: utf-8 -*-
# This file is part of the party-notes module for Tryton from m-ds.de.
# The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool


class PartyTestCase(ModuleTestCase):
    'Test party module'
    module = 'party_notes'

    @with_transaction()
    def test_notes_create_party(self):
        """ create party, check notes, search
        """
        Party = Pool().get('party.party')

        Party.create([{
            'name': 'full name',
            'notizen': 'this is a note\nwith new line',
            }])

        party, = Party.search([])
        self.assertEqual(party.name, 'full name')
        self.assertEqual(party.notizen, 'this is a note\nwith new line')

        party2, = Party.search([('notizen', 'ilike', '%note%')])
        party2, = Party.search([('notizen_tree', 'ilike', '%note%')])

# end PartyTestCase


del ModuleTestCase
