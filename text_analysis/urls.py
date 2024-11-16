from django.urls import path
from .views import AnalyzeTextView

urlpatterns = [
    path('analyze-text/', AnalyzeTextView.as_view(), name='analyze-text'),
]
