import logging
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import User
from .serializers import UserSerializer, UserRegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

logger = logging.getLogger("apps.users")

class UserList(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        logger.info("GET /users/ requested")

        try:
            users = User.objects.all()
            logger.debug(f"Total users count: {users.count()}")

            search = request.GET.get("search")
            if search:
                logger.info(f"Searching users with keyword: {search}")
                users = users.filter(
                    Q(username__icontains=search) |
                    Q(email__icontains=search)
                )

            serializer = UserSerializer(users, many=True)
            logger.info("User list fetched successfully")
            return Response(serializer.data)

        except Exception:
            logger.error("Error while fetching user list", exc_info=True)
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        logger.info("POST /users/ requested")

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New user created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"Invalid user data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            logger.warning(f"User with id={pk} not found")
            return None

    def get(self, request, pk, format=None):
        logger.info(f"GET /users/{pk}/ requested")

        user = self.get_object(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        logger.info(f"User {pk} fetched successfully")
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        logger.info(f"PUT /users/{pk}/ requested")

        user = self.get_object(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {pk} updated successfully")
            return Response(serializer.data)

        logger.warning(f"Update failed for user {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        logger.info(f"DELETE /users/{pk}/ requested")

        user = self.get_object(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        logger.info(f"User {pk} deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)
