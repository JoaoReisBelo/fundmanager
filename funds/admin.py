from __future__ import annotations

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from funds.models import Fund


@admin.register(Fund)
class FundAdmin(ModelAdmin):
    list_display = ["id", "name", "strategy"]
    list_filter = ["strategy"]
    search_fields = ["name"]
    ordering = ["name", "strategy", "id"]
    readonly_fields = ["id"]
    fieldsets = [
        (None, {"fields": ["name", "strategy", "aum", "inception_date", "id"]})
    ]
