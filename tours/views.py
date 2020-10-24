from django.shortcuts import render
from django.views import View
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from tours.date import departures, description, subtitle, title, tours
from random import sample


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка 404. Ой, что то сломалось... Простите извините!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка 500. Ой, что то сломалось... Простите извините!')


class MainView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': title,
            'subtitle': subtitle,
            'description': description,
            'tours': sample(tours.items(), 6),
            'departures': departures.items(),
        }
        return render(request, 'index.html', context=context)


class DepartureView(View):
    def get(self, request, departure, *args, **kwargs):
        if departure not in departures.keys():
            raise Http404
        context = {
            'title': title,
            'tours': [tour for tour in tours.items() if tour[1]["departure"] == departure],
            'deparcity': departures[departure],
            'departures': departures.items(),
        }

        context['tourscholko'] = len(context['tours'])
        priceAndNights = [tour[1]['price'] for tour in context['tours']]
        context['maxchena'] = max(priceAndNights)
        context['minchena'] = min(priceAndNights)
        priceAndNights = [tour[1]['nights'] for tour in context['tours']]
        context['maxnigt'] = max(priceAndNights)
        context['minnigt'] = min(priceAndNights)
        return render(request, 'departure.html', context=context)


class TourView(View):
    def get(self, request, id, *args, **kwargs):
        if id not in tours:
            raise Http404
        context = {
            'title': title,
            'tour': tours[id],
            'deparcity': departures[tours[id]['departure']],
            'departures': departures.items(),
        }
        return render(request, 'tour.html', context=context)
