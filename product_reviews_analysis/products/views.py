from glob import escape
from django.shortcuts import render

from .models import Product, Review
from .nlp import sentiment_analysis


def index(request):
    products = [product for product in Product.objects.all()]

    if request.method == 'POST':
        print("form is not valid")
        product_id = int(request.POST["product_id"])
        reviews = Review.objects.filter(product_id=product_id)
        for review in reviews:
            score = sentiment_analysis(review.review)
            review.__setattr__("score_compound", score["compound"])
            review.__setattr__("score_pos", score["pos"])
            review.__setattr__("score_neg", score["neg"])
            review.__setattr__("score_neu", score["neu"])
    else:
        reviews = Review.objects.all()
        product_id =products[0].id
        scores = {}

    context = {
        "products": products,
        "selected_product_id": product_id,
        "reviews" : reviews,
    }

    print(context)

    return render(request, "index.html", context)

def nlp(request):
    score = sentiment_analysis("I love this")
    context = {
        "score": score,
    }

    return render(request, "analysis.html", context)

def about(request):
    return render(request, "about.html", {})