from django.views.generic.list import ListView
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year, summary_per_month, total_amount, number_expenses_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()

            from_date = form.cleaned_data.get('search_from_date')
            to_date = form.cleaned_data.get('search_to_date')
            category = form.cleaned_data.get('category')
            sorting = form.cleaned_data.get('sorting')

            if name:
                queryset = queryset.filter(name__icontains=name)
            if from_date:
                queryset = queryset.filter(date__gte=from_date).order_by('-date')
            if to_date:
                queryset = queryset.filter(date__lte=to_date).order_by('-date')

            if category:
                category_first = queryset.filter(category__name=category[0])
                for el in category:
                    category_el = queryset.filter(category__name=el)
                    category_first = category_first | category_el
                queryset = category_first

            if sorting:
                if sorting == 'category_up':
                    queryset = queryset.order_by('category')
                elif sorting == 'category_down':
                    queryset = queryset.order_by('-category')
                elif sorting == 'date_down':
                    queryset = queryset.order_by('-date')
                else:
                    queryset = queryset.order_by('date')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_per_month=summary_per_month(queryset),
            summary_per_year=summary_per_year(queryset),
            total_amount=total_amount(queryset),
            number_expenses_per_category=number_expenses_per_category(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

