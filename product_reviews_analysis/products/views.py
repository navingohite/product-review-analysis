from django.shortcuts import render

from .models import Product, Review
from .nlp import sentiment_analysis

def index(request):
    names = [product.name for product in Product.objects.all()]
    context = {
        "products": names,
    }

    print(context)

    return render(request, "index.html", context)

def analysis(request):
    score = sentiment_analysis("I love this")
    context = {
        "score": score,
    }

    return render(request, "analysis.html", context)

def about(request):
    return render(request, "about.html", {})