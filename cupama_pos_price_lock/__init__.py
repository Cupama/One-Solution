# -*- coding: utf-8 -*-
from . import models


def _enable_price_restriction(env):
    """Turn the native restriction on for every existing POS shop."""
    env['pos.config'].with_context(active_test=False).search([]).write({
        'restrict_price_control': True,
    })
