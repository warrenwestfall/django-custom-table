from django.shortcuts import render
from custom_table.views import BaseCustomDataView
from example_app.models import ExampleCustomTable

class CustomTableListView(BaseCustomDataView):
    # queryset = ExampleCustomTable.objects.all()
    # context_object_name = 'example_custom_table_list'
    # template_name = 'examplecustomtable_list.html'

    def get(self, request):
        context_data = self.get_grid_list()
        return render(request, 'custom_table_list.html', context_data)

    
class CustomTableEditView(BaseCustomDataView):
    # queryset = ExampleCustomTable.objects.all()
    # context_object_name = 'example_custom_table_list'
    # template_name = 'examplecustomtable_list.html'

    def get(self, request, pk):
        context_data = self.get_detail(pk)
        return render(request, 'custom_table_edit.html', context_data)
