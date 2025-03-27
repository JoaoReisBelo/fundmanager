from __future__ import annotations

from django import forms
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from funds.models import Fund
from funds.models import Strategy
from rest_framework import filters
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ("id", "name", "strategy", "aum", "inception_date")


class StrategyFilter(filters.SearchFilter):
    search_param = "strategy"


class FundViewSet(ReadOnlyModelViewSet):
    queryset = Fund.objects.all()
    permission_classes = [AllowAny]
    serializer_class = FundSerializer
    ordering = ["name"]
    filter_backends = [StrategyFilter]
    search_fields = ["strategy"]


class IndexView(ListView):
    template_name = "funds/list.html"
    context_object_name = "funds"

    def get_queryset(self):
        qs = Fund.objects.all()

        selected = self.request.GET.get("strategy")
        if selected:
            qs = qs.filter(strategy=selected)

        return qs.order_by("name")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        selected = self.request.GET.get("strategy")
        context["strategies"] = [(s.value, s.value == selected) for s in Strategy]
        context["total_aum"] = (
            self.get_queryset().aggregate(total_aum=Sum("aum")).get("total_aum")
        )

        return context


class UploadFileForm(forms.Form):
    upload_file = forms.FileField()


class UploadFileView(View):

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                Fund.upload_funds(request.FILES["upload_file"])
            except Exception as e:
                return render(
                    request, "funds/upload.html", {"form": form, "error": str(e)}
                )

            return HttpResponseRedirect("../list/")

        return render(request, "funds/upload.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()

        return render(request, "funds/upload.html", {"form": form})
