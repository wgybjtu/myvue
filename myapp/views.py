# coding:utf-8
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from myapp.models import Book


@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except :
        response['msg'] = '添加错误'
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list']  = json.loads(serializers.serialize("json", books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except :
        response['msg'] = '获取错误'
        response['error_num'] = 1

    return JsonResponse(response)