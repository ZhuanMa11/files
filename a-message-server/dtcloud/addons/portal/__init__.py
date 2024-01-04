# -*- coding: utf-8 -*-
# Part of DTCloud. See LICENSE file for full copyright and licensing details.

# Updating mako environement in order to be able to use slug
try:
    from dtcloud.addons.mail.models.mail_render_mixin import jinja_template_env, jinja_safe_template_env
    from dtcloud.addons.http_routing.models.ir_http import slug

    jinja_template_env.globals.update({
        'slug': slug,
    })

    jinja_safe_template_env.globals.update({
        'slug': slug,
    })
except ImportError:
    pass

from . import controllers
from . import models
from . import wizard
