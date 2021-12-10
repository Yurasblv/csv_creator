from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import TableModel,DataSetModel,ColumnModel
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from core.forms import UserForm, Table_Form, row_formset, DataSetForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from core.tasks import csv_create_task
from django.views.generic.edit import FormMixin

class AuthClass(CreateView):
    form_class = UserForm
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if User.objects.filter(username=username).exists():
                login(request, user)
                return redirect('main_page')
            else:
                user = User.objects.create_user(username=username,password=password)
                user.save()
                login(request,user)
                return redirect('main_page')


class CsvMainPageClass(CreateView):
    form_class = Table_Form
    template_name = 'main.html'
    success_url = reverse_lazy('csv_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["row"] = row_formset(self.request.POST)
        else:
            data["row"] = row_formset()
        return data

    def form_valid(self, form):
        print(self.request)
        form.instance.user = self.request.user
        context = self.get_context_data()
        row = context["row"]
        if not row.is_valid():
            return super().form_invalid(form)
        self.object = form.save()
        row.instance = self.object
        row.save()
        return super().form_valid(form)


class CsvListView(ListView):
    model = TableModel
    template_name = 'csv_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class CsvDeleteView(DeleteView):
    model = TableModel
    template_name = 'csv_delete.html'
    success_url = reverse_lazy('csv_list')




class CsvClassView(ListView,FormMixin):
    model = DataSetModel
    form_class = DataSetForm
    template_name = 'csv_generate.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(schema_id=self.schema_id)

    def form_valid(self, form):
        form.instance.schema_id = self.schema_id
        form.instance.status = DataSetModel.Status.PROCESSING

        dataset = form.save()
        csv_create_task.delay(dataset.id)
        print(csv_create_task.delay(dataset))
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        self.schema_id = kwargs["pk"]
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.path