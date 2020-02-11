# -*- coding: utf-8 -*-
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return
    openupgrade.logged_query(
        env.cr, "UPDATE event_registration SET partner_id = agent_id"
    )
