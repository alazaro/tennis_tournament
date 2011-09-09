#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#

from core.models import *
from django.contrib import admin

admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Category)
admin.site.register(CategoryInTournament)
