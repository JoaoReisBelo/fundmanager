from __future__ import annotations

from django.core.files.base import ContentFile
from django.test import TestCase
from funds.models import Fund
from rest_framework import status
from rest_framework.test import APIClient


class FundApiTestCase(TestCase):
    URL = "/api/fund/"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.fund = Fund.objects.create(
            name="Amazing Fund 1",
            strategy="Long/Short Equity",
            aum="355000000",
            inception_date="2011-03-10",
        )
        cls.another_fund = Fund.objects.create(
            name="Pretty Good Fund X",
            strategy="Global Macro",
            inception_date="2012-04-10",
        )

    def setUp(self):
        super().setUp()

        self.client = APIClient()

    def test_retrieve(self):
        response = self.client.get(f"{self.URL}{self.fund.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": str(self.fund.id),
                "name": "Amazing Fund 1",
                "strategy": "Long/Short Equity",
                "aum": 355000000,
                "inception_date": "2011-03-10",
            },
        )

    def test_list(self):
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": str(self.fund.id),
                        "name": "Amazing Fund 1",
                        "strategy": "Long/Short Equity",
                        "aum": 355000000,
                        "inception_date": "2011-03-10",
                    },
                    {
                        "id": str(self.another_fund.id),
                        "name": "Pretty Good Fund X",
                        "strategy": "Global Macro",
                        "aum": None,
                        "inception_date": "2012-04-10",
                    },
                ],
            },
        )

    def test_filter(self):
        response = self.client.get(self.URL, data={"strategy": "Global Macro"})
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [{
                    "id": str(self.another_fund.id),
                    "name": "Pretty Good Fund X",
                    "strategy": "Global Macro",
                    "aum": None,
                    "inception_date": "2012-04-10",
                }],
            },
        )

        response = self.client.get(self.URL, data={"strategy": "Long/Short Equity"})
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [{
                    "id": str(self.fund.id),
                    "name": "Amazing Fund 1",
                    "strategy": "Long/Short Equity",
                    "aum": 355000000,
                    "inception_date": "2011-03-10",
                }],
            },
        )

        response = self.client.get(self.URL, data={"strategy": "Arbitrage"})
        self.assertEqual(
            response.json(), {"count": 0, "next": None, "previous": None, "results": []}
        )


class FundUpload(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.file = ContentFile(
            b"Name,Strategy,AUM (USD),Inception Date\nAmazing Fund 1,Long/Short Equity,355000000,2011-03-10\nAnother Fund Y,Global Macro,,"
        )

    def test_upload(self):
        self.assertFalse(Fund.objects.all().exists())

        Fund.upload_funds(self.file)
        self.assertEqual(Fund.objects.count(), 2)
        self.assertTrue(Fund.objects.filter(name="Amazing Fund 1").exists())
        self.assertTrue(Fund.objects.filter(aum=None).exists())

    def test_upload_twice(self):
        self.assertFalse(Fund.objects.all().exists())

        Fund.upload_funds(self.file)
        self.assertEqual(Fund.objects.count(), 2)
        self.file.seek(0)

        Fund.upload_funds(self.file)
        self.assertEqual(Fund.objects.count(), 2)
