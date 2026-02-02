
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.trees.models import Trees
from .serializers import TreeSerializer
#from .filters import TaskFilter, UserFilter
from django.db.models import Q
import logging

logger = logging.getLogger("apps.trees")

@api_view(['GET','POST'])
def tree_list(request, format=None):
    if request.method == 'GET':
        logger.info("GET /trees/ requested")
        try:
            trees = Trees.objects.all()
            logger.debug(f"Total trees count: {trees.count()}")

            search = request.GET.get('search')
            if search:
                logger.info(f"Searching trees with keyword: {search}")
                trees = trees.filter(Q(name__icontains=search) | Q(description__icontains=search))

            serializer = TreeSerializer(trees, many=True)
            logger.info("Tree list fetched successfully")
            return Response(serializer.data)
        
        except Exception:
            logger.error("Error while fetching tree list", exc_info=True)
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    elif request.method == 'POST':
        logger.info("POST /trees/ requested")

        serializer = TreeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New tree created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Invalid tree data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def tree_detail(request, pk, format=None):
    logger.info(f"Request on /trees/{pk}/ with method {request.method}")

    try:
        trees = Trees.objects.get(pk=pk)
    except Trees.DoesNotExist:
        logger.warning(f"Tree with id={pk} not found")
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TreeSerializer(trees)
        logger.info(f"Tree {pk} fetched successfully")
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TreeSerializer(trees, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Tree {pk} updated successfully")
            return Response(serializer.data)
        
        logger.warning(f"Update failed for tree {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        trees.delete()
        logger.info(f"Tree {pk} deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)