from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.people.models import People
from .serializers import PeopleSerializer
#from .filters import PeopleFilter
from django.db.models import Q
import logging
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger("apps.people")

class PeopleList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logger.info("GET /people /requested")

        try:
            peoples = People.objects.all()
            logger.debug(f"Total people count: {peoples.count()}")

            search = request.GET.get('search')
            if search:
                logger.info(f"Searching people with keyword: {search}")
                peoples = peoples.filter( Q(name__icontains=search) | Q(description__icontains=search))

                serializer = PeopleSerializer(peoples, many=True)
                logger.info("People list fetched successfully")
                return Response(serializer.data)
        
        except Exception:
            logger.error("Error while fetching people list", exc_info=True)
            return Response({"error": "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        logger.info("POST /people/ requested")

        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New person created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"Invalid people data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PeopleDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return People.objects.get(pk=pk)
        except People.DoesNotExist:
            logger.warning(f"People with id={pk} not found")
            return None

    def get(self, request, pk, format=None):
        logger.info(f"GET /people/{pk}/ requested")

        people = self.get_object(pk)
        if not people:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PeopleSerializer(people)
        logger.info(f"People {pk} fetched successfully")
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        logger.info(f"PUT /people/{pk}/ requested")

        people = self.get_object(pk)
        if not people:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PeopleSerializer(people, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"People {pk} updated successfully")
            return Response(serializer.data)

        logger.warning(f"Update failed for people {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        logger.info(f"DELETE /people/{pk}/ requested")

        people = self.get_object(pk)
        if not people:
            return Response(status=status.HTTP_404_NOT_FOUND)

        people.delete()
        logger.info(f"People {pk} deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)
