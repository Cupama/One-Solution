# -*- coding: utf-8 -*-
import logging

from odoo.exceptions import UserError, ValidationError

from . import models

_logger = logging.getLogger(__name__)


def _enable_price_restriction(env):
    """Turn the native restriction on for every existing POS shop.

    One write per shop, in its own company: pos_hr reads self.company_id as
    a singleton while writing, so a single write over shops belonging to
    several companies raises "Expected singleton". Each write also runs in
    its own savepoint, so one shop carrying invalid legacy data cannot abort
    the installation of the module.
    """
    for config in env['pos.config'].search([]):
        try:
            with env.cr.savepoint():
                config.with_company(config.company_id).write({
                    'restrict_price_control': True,
                })
        except (UserError, ValidationError) as error:
            _logger.warning(
                "Cupama POS price lock: shop %s skipped: %s",
                config.name, error)
