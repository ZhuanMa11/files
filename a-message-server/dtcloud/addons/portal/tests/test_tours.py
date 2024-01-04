# -*- coding: utf-8 -*-
# Part of DTCloud. See LICENSE file for full copyright and licensing details.

from dtcloud.addons.base.tests.common import HttpCaseWithUserPortal
from dtcloud.tests import tagged


@tagged('post_install', '-at_install')
class TestUi(HttpCaseWithUserPortal):
    def test_01_portal_load_tour(self):
        self.start_tour("/", 'portal_load_homepage', login="portal")
