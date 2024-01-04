# -*- coding: utf-8 -*-
# This file is part of the party-notes module for Tryton from m-ds.de.
# The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.


import trytond.tests.test_tryton
import unittest

from .test_party import PartyTestCase


__all__ = ['suite']


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PartyTestCase))
    return suite
