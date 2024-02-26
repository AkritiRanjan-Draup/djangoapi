from django.http import HttpResponse, JsonResponse


def home_page(request):
    # print("home page requested")
    # return HttpResponse("This is home page")
    friends = ['ankit', 'ankush', 'shreya']
    return JsonResponse(friends, safe=False)
