from cProfile import label

from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    DROPDOWN_LIST = [
        ('date_up', 'Date Up'),
        ('date_down', 'Date Down'),
        ('category_up', 'Category Up'),
        ('category_down', 'Category Down'),
    ]

    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple,
                                              required=False)
    search_from_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, 2024)), required=False)
    search_to_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, 2024)), required=False)

    sorting = forms.CharField(label='Choose the sorting', widget=forms.Select(choices=DROPDOWN_LIST))


    class Meta:
        model = Expense
        fields = ['name',  ]

        widgets = {'category': forms.CheckboxSelectMultiple,}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False


class CategorySearchForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False


