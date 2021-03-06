#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009-2012 Zuza Software Foundation
# Copyright 2013-2014 Evernote Corporation
#
# This file is part of Pootle.
#
# Pootle is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Pootle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pootle; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from pootle_app.models import Directory
from pootle_app.models.permissions import (get_permission_contenttype,
                                           PermissionSet)
from pootle_app.views.admin import util
from pootle_misc.forms import GroupedModelChoiceField
from pootle_statistics.models import Submission


User = get_user_model()

PERMISSIONS = {
    'positive': ['view', 'suggest', 'translate', 'review', 'administrate'],
    'negative': ['hide'],
}


class PermissionFormField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, instance):
        return _(instance.name)


def admin_permissions(request, current_directory, template, context):
    project = context.get('project', None)
    language = context.get('language', None)

    negative_permissions_excl = list(PERMISSIONS['negative'])
    positive_permissions_excl = list(PERMISSIONS['positive'])

    # Don't provide means to alter access permissions under /<lang_code>/*
    # In other words: only allow setting access permissions for the root
    # and the `/projects/<code>/` directories
    if language is not None:
        access_permissions = ['view', 'hide']
        negative_permissions_excl.extend(access_permissions)
        positive_permissions_excl.extend(access_permissions)

    content_type = get_permission_contenttype()

    positive_permissions_qs = content_type.permission_set.exclude(
        codename__in=negative_permissions_excl,
    )
    negative_permissions_qs = content_type.permission_set.exclude(
        codename__in=positive_permissions_excl,
    )

    base_queryset = User.objects.filter(is_active=1).exclude(
            id__in=current_directory.permission_sets \
                                    .values_list('user_id', flat=True),
    )
    querysets = [(None, base_queryset.filter(
        username__in=('nobody', 'default')
    ))]

    querysets.append((
        _('All Users'),
        base_queryset.exclude(username__in=('nobody', 'default'))
                     .order_by('username'),
    ))


    class PermissionSetForm(forms.ModelForm):

        class Meta:
            model = PermissionSet
            fields = ('user', 'directory', 'positive_permissions',
                      'negative_permissions')

        directory = forms.ModelChoiceField(
                queryset=Directory.objects.filter(pk=current_directory.pk),
                initial=current_directory.pk,
                widget=forms.HiddenInput,
        )
        user = GroupedModelChoiceField(
                label=_('Username'),
                querysets=querysets,
                queryset=User.objects.all(),
                required=True,
                widget=forms.Select(attrs={
                    'class': 'js-select2 select2-username',
                }),
        )
        positive_permissions = PermissionFormField(
                label=_('Add Permissions'),
                queryset=positive_permissions_qs,
                required=False,
                widget=forms.SelectMultiple(attrs={
                    'class': 'js-select2 select2-multiple',
                    'data-placeholder': _('Select one or more permissions'),
                }),
        )
        negative_permissions = PermissionFormField(
                label=_('Revoke Permissions'),
                queryset=negative_permissions_qs,
                required=False,
                widget=forms.SelectMultiple(attrs={
                    'class': 'js-select2 select2-multiple',
                    'data-placeholder': _('Select one or more permissions'),
                }),
        )

        def __init__(self, *args, **kwargs):
            super(PermissionSetForm, self).__init__(*args, **kwargs)

            # Don't display extra negative permissions field where they
            # are not applicable
            if language is not None:
                del self.fields['negative_permissions']


    link = lambda instance: unicode(instance.user)
    directory_permissions = current_directory.permission_sets \
                                             .order_by('user').all()

    return util.edit(request, template, PermissionSet, context, link,
                     linkfield='user', queryset=directory_permissions,
                     can_delete=True, form=PermissionSetForm)
