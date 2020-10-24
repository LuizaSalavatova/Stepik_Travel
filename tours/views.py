from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render
from django.views import View
import tours.date as data

from random import sample


class MainView(View):
    def get(self, request):
        context = {'title': data.title,
                   'subtitle': data.subtitle,
                   'description': data.description,
                   'departures': data.departures,
                   'sample_tours': sample(data.tours.items(), 6)
                   }

        return render(request, 'index.html', context=context)


class DepartureView(View):
    def get(self, request, departure):
        if departure not in data.departures:
            raise Http404

        tours_from_departure = {}
        for tour_id, tour in data.tours.items():
            if tour['departure'] == departure:
                tours_from_departure[tour_id] = tour

        tours_count = len(tours_from_departure)
        tours_prices = sorted(tour['price'] for tour in tours_from_departure.values())
        tours_nights = sorted(tour['nights'] for tour in tours_from_departure.values())

        context = {'title': data.title,
                   'departures': data.departures,
                   'departure_title': data.departures[departure],
                   'tours_count': tours_count,
                   'min_price_tour': tours_prices[0],
                   'max_price_tour': tours_prices[-1],
                   'min_nights_tour': tours_nights[0],
                   'max_nights_tour': tours_nights[-1],
                   'tours_from_departure': tours_from_departure,
                   }
        return render(request, 'departure.html', context=context)


class TourView(View):
    def get(self, request, tour_id):
        if tour_id not in data.tours:
            raise Http404

        tour_data = data.tours[tour_id]
        departure_title = data.departures[tour_data['departure']]

        context = {'title': data.title,
                   'departures': data.departures,
                   'departure_title': departure_title,
                   'tour': tour_data,
                   }
        return render(request, 'tour.html', context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Ошибка 404, Простите извините!')


def custom_handler500(request):
    return HttpResponse("Ой, что то сломалось... Ошибка 500, Простите извините!")
