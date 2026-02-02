from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.relationship.models import Relation
from .serializers import RelationSerializer
#from .filters import RelationFilter
from django.db.models import Q
import logging

logger = logging.getLogger("apps.relationship")

@api_view(['GET','POST'])
def relation_list(request, format=None):
    if request.method == 'GET':
        logger.info("GET /relations/ requested")

        try:
            relations = Relation.objects.all()
            logger.debug(f"Total relations count: {relations.count()}")

            search = request.GET.get('search')
            if search:
                logger.info(f"Searching relations with keyword: {search}")
                relations = relations.filter( Q(name__icontains=search) | Q(description__icontains=search))

            serializer = RelationSerializer(relations, many=True)
            logger.info("Relation list fetched successfully")
            return Response(serializer.data)
        
        except Exception:
            logger.error("Error while fetching relation list", exc_info=True)
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        logger.info("POST /relations/ requested")

        serializer = RelationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New relation created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Invalid relation data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def relation_detail(request, pk, format=None):

    logger.info(f"Request on /relations/{pk}/ with method {request.method}")

    try:
        relations = Relation.objects.get(pk=pk)

    except Relation.DoesNotExist:
        logger.warning(f"Relation with id={pk} not found")
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RelationSerializer(relations)
        logger.info(f"Relation {pk} fetched successfully")
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = RelationSerializer(relations, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Relation {pk} updated successfully")
            return Response(serializer.data)
        
        logger.warning(f"Update failed for relation {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        relations.delete()
        logger.info(f"Relation {pk} deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)
