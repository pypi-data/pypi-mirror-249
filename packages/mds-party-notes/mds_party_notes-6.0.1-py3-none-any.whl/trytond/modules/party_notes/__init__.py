# -*- coding: utf-8 -*-
# This file is part of the party-notes module for Tryton from m-ds.de.
# The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .party import Party


def register():
    Pool.register(
        Party,
        module='party_notes', type_='model')
