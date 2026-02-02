from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.people.models import People
from .serializers import PeopleSerializer
#from .filters import PeopleFilter
from django.db.models import Q
import logging

logger = logging.getLogger("apps.people")

@api_view(['GET','POST'])
def people_list(request, format=None):
    if request.method == 'GET':
        logger.info("GET / people / requested")
        try:
            peoples = People.objects.all()
            logger.debug(f"Total People Count: {peoples.count}")

            search = request.GET.get('search')
            if search:
                logger.info(f"Searching people with keyword: {search}")
                peoples = peoples.filter( Q(name__icontains=search) | Q(description__icontains=search))

            serializer = PeopleSerializer(peoples, many=True)
            logger.info("People list fetched successfully")
            return Response(serializer.data)
        
        except Exception:
            logger.error("Error while fetching people list",exc_info=True)
            return Response({"error":"something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    elif request.method == 'POST':
        logger.info("POST/ people / requested")

        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New person created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Invalid poeple data : {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def people_detail(request, pk, format=None):
    logger.info(f"Request on /people/{pk}/ with method {request.method}")

    try:
        peoples = People.objects.get(pk=pk)

    except People.DoesNotExist:
        logger.warning(f"People with id={pk} not found")
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PeopleSerializer(peoples)
        logger.info(f"People {pk} fetched successfully")
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PeopleSerializer(peoples, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"People {pk} updated successfully")
            return Response(serializer.data)
        
        logger.warning(f"Update failed for people {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        peoples.delete()
        logger.info(f"People {pk} deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)
