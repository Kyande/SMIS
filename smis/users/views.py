from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet


class UserView(ModelViewSet):
    """
    A View to handle everything user related.

    Things to consider:
    1. login.
    2. registration.
    3. User listing.
    4. User deactivation.
    5. Password change.
    """
    @action(methods=['POST'], detail=False)
    def login(self, request):
        return

    @action(methods=['POST'], detail=False)
    def register(self, request):
        return
