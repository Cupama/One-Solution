# -*- coding: utf-8 -*-
"""Helpers used to write readable log notes in the chatter (#14)."""
from markupsafe import Markup

from odoo import _


def field_label(record, fname):
    return record._fields[fname].get_description(record.env)['string']


def field_value(record, fname):
    """Return a human readable representation of ``record[fname]``."""
    field = record._fields[fname]
    value = record[fname]
    if field.type in ('many2one', 'many2many', 'one2many'):
        names = value.mapped('display_name')
        return ', '.join(names) if names else _("empty")
    if field.type == 'selection':
        selection = dict(field._description_selection(record.env))
        return selection.get(value) or _("empty")
    if field.type == 'boolean':
        return _("Yes") if value else _("No")
    if value in (False, None, ''):
        return _("empty")
    if field.type in ('float', 'monetary'):
        return '{:.2f}'.format(value)
    return str(value)


def snapshot(record, fnames):
    """Freeze the displayed value of ``fnames`` before a write."""
    return {fname: field_value(record, fname) for fname in fnames}


def diff(record, before):
    """Compare a snapshot with the current values, oldest field first."""
    changes = []
    for fname, old in before.items():
        new = field_value(record, fname)
        if old != new:
            changes.append(_(
                "%(field)s: %(old)s -> %(new)s",
                field=field_label(record, fname), old=old, new=new,
            ))
    return changes


def note(title, items=()):
    """Build a chatter body: a sentence and an optional bullet list."""
    body = Markup('<span>%s</span>') % title
    if items:
        body += Markup('<ul>%s</ul>') % Markup('').join(
            Markup('<li>%s</li>') % item for item in items
        )
    return body
