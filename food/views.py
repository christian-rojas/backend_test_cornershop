from django.http import HttpResponse
from food.models import Food

def index(request):
    salad = 'salad'
    entrance = 'entrance'
    desert = 'desert'
    user = Food(1, salad, entrance, desert)
    user.save()
    items = Food.objects.all()
    return HttpResponse(items.values())

def post(request):
    # username = request.POST.get('')
    salad = 'salad'
    entrance = 'entrance'
    desert = 'desert'
    user = Food(1, salad, entrance, desert)
    user.save()
    return HttpResponse("Hello, world. You're at the food index.")