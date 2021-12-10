from django.contrib import admin
from core.models import TableModel,DataSetModel,ColumnModel

admin.site.register(TableModel)
admin.site.register(ColumnModel)
admin.site.register(DataSetModel)
