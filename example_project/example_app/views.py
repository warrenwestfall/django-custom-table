import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from custom_table.views import BaseMetadataView, BaseCustomTableView
from example_app.models import CustomMetadata


class RestMetadataListView(BaseMetadataView):
    def get(self, request):
        return JsonResponse(self.get_list(), safe=False)


class RestMetadataDetailView(BaseMetadataView):
    def get(self, request, name):
        return JsonResponse(self.get_detail(name), safe=False)


class RestCustomTableListView(BaseCustomTableView):
    include_metadata = False

    def get(self, request):
        return JsonResponse(self.get_grid_list(), safe=False)


    def post(self, request):
        new_record = self.create(json.loads(request.body))
        return JsonResponse({'pk': new_record.pk}, status=201)


class RestCustomTableDetailView(BaseCustomTableView):
    include_metadata = False

    def get(self, request, pk):
        return JsonResponse(self.get_detail(pk), safe=False)


    def patch(self, request, pk):
        self.update_fields(pk, json.loads(request.body))
        return HttpResponse(status=202)


    def delete(self, request, pk):
        self.delete_record(pk)
        return HttpResponse(status=204)



class HtmlCustomTableListView(BaseCustomTableView):
    metadata_model = CustomMetadata
    # queryset = ExampleCustomTable.objects.all()
    # context_object_name = 'example_custom_table_list'
    # template_name = 'examplecustomtable_list.html'

    def get(self, request):
        return render(request, 'custom_table_list.html', self.get_grid_list())

    
class HtmlCustomTableDetailView(BaseCustomTableView):
    metadata_model = CustomMetadata
    # queryset = ExampleCustomTable.objects.all()
    # context_object_name = 'example_custom_table_list'
    # template_name = 'examplecustomtable_list.html'

    def get(self, request, pk):
        return render(request, 'custom_table_edit.html', self.get_detail(pk))
