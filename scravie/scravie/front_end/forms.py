from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100)


class DateSearchForm(forms.Form):
    date_query = forms.CharField(label='Date', max_length=100)
