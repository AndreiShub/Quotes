import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .models import Quote
from .forms import QuoteForm
from django.urls import reverse
from django.core.paginator import Paginator

def home(request):
    quotes = list(Quote.objects.all())
    if not quotes:
        return render(request, "quotes/home.html", {"quote": None})

    weights = [q.weight for q in quotes]
    min_weight = min(weights)
    if min_weight <= 0:
        weights = [w - min_weight + 1 for w in weights]

    quote = random.choices(quotes, weights=weights, k=1)[0]
    quote.views += 1
    quote.save()

    voted = request.session.get('voted_quotes', {})

    return render(request, "quotes/home.html", {"quote": quote, "voted": voted})

def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            source = form.cleaned_data['source']
            if Quote.objects.filter(text=text, source=source).exists():
                form.add_error('text', 'Такая цитата уже существует.')
            else:
                count = Quote.objects.filter(source=source).count()
                if count >= 3:
                    form.add_error('source', 'У этого источника уже 3 цитаты.')
                else:
                    form.save()
                    return redirect("home")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})

def ajax_random_quote(request):
    quotes = list(Quote.objects.all())
    if not quotes:
        return JsonResponse({"error": "Нет цитат"})

    weights = [q.weight for q in quotes]
    min_weight = min(weights)
    if min_weight <= 0:
        weights = [w - min_weight + 1 for w in weights]

    quote = random.choices(quotes, weights=weights, k=1)[0]
    quote.views += 1
    quote.save()

    voted = request.session.get('voted_quotes', {})

    return JsonResponse({
        "id": quote.pk,
        "text": quote.text,
        "source": quote.source,
        "likes": quote.likes,
        "dislikes": quote.dislikes,
        "voted": voted.get(str(quote.pk), 0),
        "views": quote.views,
    })

def top_quotes(request):
    quotes = Quote.objects.all()

    for q in quotes:
        q.weight = q.likes - q.dislikes
        q.views += 1
        q.save()

    top5 = quotes.order_by('-weight', '-likes')[:5]

    voted = request.session.get('voted_quotes', {})

    return render(request, "quotes/top_quotes.html", {"quotes": top5, "voted": voted})

def all_quotes(request):
    quotes = Quote.objects.all().order_by('-id')
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    voted = request.session.get('voted_quotes', {})

    return render(request, "quotes/all_quotes.html", {"quotes": page_obj, "voted": voted})

def ajax_vote_quote(request, pk, action):
    quote = get_object_or_404(Quote, pk=pk)
    voted = request.session.get('voted_quotes', {})
    current_vote = voted.get(str(pk))

    status = None

    if request.method == "POST":
        action = request.path.split("/")[-2]

        if action == "like":
            if current_vote == 1:
                quote.likes -= 1
                voted[str(pk)] = None
                status = "unliked"
            elif current_vote == -1:
                quote.dislikes -= 1
                quote.likes += 1
                voted[str(pk)] = 1
                status = "liked"
            else:
                quote.likes += 1
                voted[str(pk)] = 1
                status = "liked"

        elif action == "dislike":
            if current_vote == -1:
                quote.dislikes -= 1
                voted[str(pk)] = None
                status = "undisliked"
            elif current_vote == 1:
                quote.likes -= 1
                quote.dislikes += 1
                voted[str(pk)] = -1
                status = "disliked"
            else:
                quote.dislikes += 1
                voted[str(pk)] = -1
                status = "disliked"

        quote.weight = quote.likes - quote.dislikes
        quote.save()
        request.session['voted_quotes'] = voted
        request.session.modified = True

    return JsonResponse({
        "status": status,
        "likes": quote.likes,
        "dislikes": quote.dislikes,
    })