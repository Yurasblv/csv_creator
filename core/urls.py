from django.urls import include,path
from core import views

urlpatterns = [
    path('logout/', include('django.contrib.auth.urls'), name='logout'),
    path('home/', views.AuthClass.as_view(), name='home_page'),
    path('main/',views.CsvMainPageClass.as_view(),name='main_page'),
    path('csv_list/',views.CsvListView.as_view(),name='csv_list'),
    path('delete/<int:pk>/', views.CsvDeleteView.as_view(), name='csv_delete'),
    path('csv_generate/<int:pk>/', views.CsvClassView.as_view(), name='csv_generate'),

]
