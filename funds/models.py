from __future__ import annotations

import csv
import uuid
from enum import Enum

from django.db import models


class Strategy(Enum):
    LSEQUITY = "Long/Short Equity"
    GLOBAL_MACRO = "Global Macro"
    ARBITRAGE = "Arbitrage"


def _clean_fund_data(fund_data):
    return {key: value if value else None for key, value in fund_data.items()}


class Fund(models.Model):
    class Meta:
        indexes = [models.Index("strategy", "name", name="ix_fund_strategy")]

    str_fmt = "{name}"
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    strategy = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in Strategy],
        blank=False,
        null=False,
    )
    aum = models.IntegerField(blank=True, null=True)
    inception_date = models.DateField(blank=True, null=True)

    @classmethod
    def upload_funds(cls, file):
        reader = csv.DictReader(file.read().decode("utf-8").splitlines())
        reader.fieldnames = ["name", "strategy", "aum", "inception_date"]
        next(reader)  # ignore existing header

        Fund.objects.bulk_create(
            (Fund(**_clean_fund_data(fund_data)) for fund_data in reader),
            update_conflicts=True,
            unique_fields=["name"],
            update_fields=["strategy", "aum", "inception_date"],
        )
