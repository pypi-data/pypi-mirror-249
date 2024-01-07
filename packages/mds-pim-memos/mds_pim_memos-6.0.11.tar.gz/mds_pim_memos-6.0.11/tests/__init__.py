# -*- coding: utf-8 -*-
# This file is part the pim-memos-module for Tryton from m-ds.de.
# The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.pim_memos.tests.test_memos import PimMemoTestCase

__all__ = ['suite']


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        PimMemoTestCase))
    return suite
