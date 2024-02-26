from django.shortcuts import render
from .models import Company
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views import View


class CompanyList_or_Post(View):
    def get(self, request):
        companies = Company.objects.all()
        data = [{'company_id': company.company_id, 'name': company.name, 'location': company.location,
                 'type': company.type, 'added_date': company.added_date.strftime('%Y-%m-%d %H:%M:%S'),
                 'active': company.active} for company in companies]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        company = Company.objects.create(
            name=data['name'],
            location=data['location'],
            type=data['type'],
        )
        response_data = {'company_id': company.company_id, 'name': company.name, 'location': company.location,
                         'type': company.type, 'added_date': company.added_date.strftime('%Y-%m-%d %H:%M:%S'),
                         'active': company.active}
        return JsonResponse(response_data, safe=False)



class CompanyUpdate_or_Delete(View):
    def put(self, request, company_id):
        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)

        data = json.loads(request.body)
        company.name = data.get('name', company.name)
        company.location = data.get('location', company.location)
        company.type = data.get('type', company.type)
        company.save()

        response_data = {'company_id': company.company_id, 'name': company.name, 'location': company.location,
                         'type': company.type, 'added_date': company.added_date.strftime('%Y-%m-%d %H:%M:%S'),
                         'active': company.active}
        return JsonResponse(response_data)

    def delete(self, request, company_id):
        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)

        company.delete()
        return JsonResponse({'message': 'Company deleted successfully'})






# Create your views here.
# def company_list(request):
# data = Company.objects.create( name="Samsung", location="Aus", type="Laptop",)
# data = ["hello world"]
# data = Company.objects.all()
# return JsonResponse(data, safe=False)

# @csrf_exempt
# def company_list(request):
#     if request.method == 'GET':
#         companies = Company.objects.all()
#         data = [{'company_id': company.company_id, 'name': company.name, 'location': company.location,
#                  'type': company.type, 'added_date': company.added_date.strftime('%Y-%m-%d %H:%M:%S'),
#                  'active': company.active} for company in companies]
#         return JsonResponse(data, safe=False)
#
#     elif request.method == 'POST':
#         data = json.loads(request.body)
#         company = Company.objects.create(
#             name=data['name'],
#             location=data['location'],
#             type=data['type'],
#         )
#         datas = {'company_id': company.company_id, 'name': company.name, 'location': company.location,
#                  'type': company.type, 'added_date': company.added_date.strftime('%Y-%m-%d %H:%M:%S'),
#                  'active': company.active}
#         return JsonResponse(datas, safe=False)
#
# @csrf_exempt
# def update_company(request, company_id):
#     try:
#         company = Company.objects.get(pk=company_id)
#     except Company.DoesNotExist:
#         return JsonResponse({'error': 'Company not found'}, status=404)
#     if request.method == 'PUT':
#         data = json.loads(request.body)
#         company.name = data.get('name', company.name)
#         company.location = data.get('location', company.location)
#         company.type = data.get('type', company.type)
#
#         company.save()
#         return JsonResponse({'company_id': company.company_id, 'name': company.name, 'location': company.location,
#                              'type': company.type, 'added_date': company.added_date.strftime('%Y-%m-%d %H:%M:%S'),
#                              'active': company.active})
#
#     elif request.method == 'DELETE':
#         company.delete()
#         return JsonResponse({'message': 'Company deleted successfully'})
