from rest_framework import viewsets
from rest_framework.response import Response

from app.db_router import RegionRouter
from .multi_db_model import get_good_model


class GoodViewSet(viewsets.ViewSet):
    # 使用router.db_for_read或router.db_for_write时传递hints
    # db = RegionRouter().db_for_read(instance.__class__, hints={'custom_hint': 'my_value'})
    def list(self, request, region=None):
        GoodModel = get_good_model(region)
        if not GoodModel:
            return Response({'error': 'Invalid region'}, status=400)

        goods = GoodModel.objects.all().values()
        return Response(list(goods))

    def create(self, request, region=None):
        GoodModel = get_good_model(region)
        if not GoodModel:
            return Response({'error': 'Invalid region'}, status=400)

        name = request.data.get('name')
        price = request.data.get('price')
        good = GoodModel.objects.create(name=name, price=price)
        return Response({'id': good.id, 'name': good.name, 'price': good.price})

    def retrieve(self, request, pk=None, region=None):
        GoodModel = get_good_model(region)
        if not GoodModel:
            return Response({'error': 'Invalid region'}, status=400)

        good = GoodModel.objects.filter(id=pk).first()
        if not good:
            return Response({'error': 'Good not found'}, status=404)

        return Response({'id': good.id, 'name': good.name, 'price': good.price})

    def update(self, request, pk=None, region=None):
        GoodModel = get_good_model(region)
        if not GoodModel:
            return Response({'error': 'Invalid region'}, status=400)

        good = GoodModel.objects.filter(id=pk).first()
        if not good:
            return Response({'error': 'Good not found'}, status=404)

        good.name = request.data.get('name', good.name)
        good.price = request.data.get('price', good.price)
        good.save()
        return Response({'id': good.id, 'name': good.name, 'price': good.price})

    def destroy(self, request, pk=None, region=None):
        GoodModel = get_good_model(region)
        if not GoodModel:
            return Response({'error': 'Invalid region'}, status=400)

        good = GoodModel.objects.filter(id=pk).first()
        if not good:
            return Response({'error': 'Good not found'}, status=404)

        good.delete()
        return Response({'success': True})
