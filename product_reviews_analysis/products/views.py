from glob import escape
from django.shortcuts import render

from .models import Product, Review
from .nlp import sentiment_analysis


def index(request):
    products = [product for product in Product.objects.all()]

    if request.method == 'POST':
        review_all = ""
        product_id = int(request.POST["product_id"])
        reviews = Review.objects.filter(product_id=product_id)
        for review in reviews:
            review_all = review_all + review.review
            score = sentiment_analysis(review.review)
            review.__setattr__("score_compound", score["compound"])
            review.__setattr__("score_pos", score["pos"])
            review.__setattr__("score_neg", score["neg"])
            review.__setattr__("score_neu", score["neu"])
        
        selected_product = Product.objects.filter(id=product_id)
        score = sentiment_analysis(review_all)
        selected_product.__setattr__("score_compound", score["compound"])
        selected_product.__setattr__("score_pos", score["pos"])
        selected_product.__setattr__("score_neg", score["neg"])
        selected_product.__setattr__("score_neu", score["neu"])
    else:
        reviews = Review.objects.all()
        selected_product =products[0]
        selected_product.__setattr__("score_compound", 0)
        selected_product.__setattr__("score_pos", 0)
        selected_product.__setattr__("score_neg", 0)
        selected_product.__setattr__("score_neu", 0)

    context = {
        "products": products,
        "selected_product": selected_product,
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