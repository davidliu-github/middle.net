import json

import requests
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Location
from apps.core.serializers import LocationModelSerializer, LocationSerializer

from backend.apps.core.utils import populate_slug_for_multiple_locations


class LocationView(APIView):
    def get(self, request, slug):
        return Response(LocationModelSerializer(Location.objects.filter(slug=slug), many=True).data)

    def post(self, request):
        serializer = LocationSerializer(data=populate_slug_for_multiple_locations(request.data), many=True)
        serializer.is_valid(raise_exception=True)
        locations = serializer.save()
        return Response(LocationModelSerializer(Location.objects.filter(slug=locations[0].slug) if len(locations) > 0 else [], many=True).data, status=status.HTTP_201_CREATED)

    def delete(self, request, slug):
        if 'id' in request.query_params:
            get_object_or_404(Location, slug=slug, id=request.query_params.get('id')).delete()
            return Response('Location deleted successfully', status=status.HTTP_204_NO_CONTENT)
        return Response('id is required', status=status.HTTP_400_BAD_REQUEST)


class NearbyPlacesView(APIView):
    def post(self, request):
        try:
            response = requests.request("GET", request.data.get('url'))
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        if response.status_code == status.HTTP_200_OK:
            return Response(json.loads(response.text)['results'][:5])
        else:
            return Response(response.text, status=response.status_code)
