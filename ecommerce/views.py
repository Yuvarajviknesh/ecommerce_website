from django.shortcuts import render

def custom_page_notfound(request,exception):
    return render(request,'404.html',status=404)