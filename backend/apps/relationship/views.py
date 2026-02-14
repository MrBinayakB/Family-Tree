from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.relationship.models import Relation
from .serializers import RelationSerializer
from django.db.models import Q
import logging
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger("apps.relationship")

class RelationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logger.info("GET /relations/ requested")

        try:
            relations = Relation.objects.all()
            logger.debug(f"Total relations count: {relations.count()}")

            search = request.GET.get('search')
            if search:
                logger.info(f"Searching relations with keyword: {search}")
                relations = relations.filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search)
                )

            serializer = RelationSerializer(relations, many=True)
            logger.info("Relation list fetched successfully")
            return Response(serializer.data)

        except Exception:
            logger.error("Error while fetching relation list", exc_info=True)
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        logger.info("POST /relations/ requested")

        serializer = RelationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New relation created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"Invalid relation data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RelationDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Relation.objects.get(pk=pk)
        except Relation.DoesNotExist:
            logger.warning(f"Relation with id={pk} not found")
            return None

    def get(self, request, pk, format=None):
        logger.info(f"GET /relations/{pk}/ requested")

        relation = self.get_object(pk)
        if not relation:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RelationSerializer(relation)
        logger.info(f"Relation {pk} fetched successfully")
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        logger.info(f"PUT /relations/{pk}/ requested")

        relation = self.get_object(pk)
        if not relation:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RelationSerializer(relation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Relation {pk} updated successfully")
            return Response(serializer.data)

        logger.warning(f"Update failed for relation {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        logger.info(f"DELETE /relations/{pk}/ requested")

        relation = self.get_object(pk)
        if not relation:
            return Response(status=status.HTTP_404_NOT_FOUND)

        relation.delete()
        logger.info(f"Relation {pk} deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)
