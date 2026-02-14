from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.trees.models import Trees
from .serializers import TreeSerializer
from django.db.models import Q
import logging

logger = logging.getLogger("apps.trees")

class TreeList(APIView):

    def get(self, request, format=None):
        logger.info("GET /trees/ requested")

        try:
            trees = Trees.objects.all()
            logger.debug(f"Total trees count: {trees.count()}")

            search = request.GET.get('search')
            if search:
                logger.info(f"Searching trees with keyword: {search}")
                trees = trees.filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search)
                )

            serializer = TreeSerializer(trees, many=True)
            logger.info("Tree list fetched successfully")
            return Response(serializer.data)

        except Exception:
            logger.error("Error while fetching tree list", exc_info=True)
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        logger.info("POST /trees/ requested")

        serializer = TreeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New tree created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"Invalid tree data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TreeDetail(APIView):

    def get_object(self, pk):
        try:
            return Trees.objects.get(pk=pk)
        except Trees.DoesNotExist:
            logger.warning(f"Tree with id={pk} not found")
            return None

    def get(self, request, pk, format=None):
        logger.info(f"GET /trees/{pk}/ requested")

        tree = self.get_object(pk)
        if not tree:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TreeSerializer(tree)
        logger.info(f"Tree {pk} fetched successfully")
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        logger.info(f"PUT /trees/{pk}/ requested")

        tree = self.get_object(pk)
        if not tree:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TreeSerializer(tree, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Tree {pk} updated successfully")
            return Response(serializer.data)

        logger.warning(f"Update failed for tree {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        logger.info(f"DELETE /trees/{pk}/ requested")

        tree = self.get_object(pk)
        if not tree:
            return Response(status=status.HTTP_404_NOT_FOUND)

        tree.delete()
        logger.info(f"Tree {pk} deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)
