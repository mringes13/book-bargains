import django_filters
from django_filters import CharFilter, NumberFilter
from django import forms
from .models import *

class BookFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt', label='Price Greater Than')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt', label='Price Less Than')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains', label='Author')
    ISBN13 = django_filters.CharFilter(field_name='ISBN13', lookup_expr='icontains', label='ISBN13')
    field = django_filters.CharFilter(field_name='field', lookup_expr='icontains', label='Field')
    
    class Meta:
        model = Book
        fields = ['selldonate', 'title', 'author', 'ISBN13', 'edition', 'condition', 'field']

