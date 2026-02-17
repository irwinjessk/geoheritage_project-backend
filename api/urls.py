from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from .views.auth_views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
    UserProfileView
)
from .views.patrimoine_views import (
    PatrimoineListCreateView,
    PatrimoineDetailView,
    PatrimoineNearbyView,
    PatrimoineMapView
)

app_name = 'api'

urlpatterns = [
    # Authentification JWT
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', UserProfileView.as_view(), name='user_profile'),
    
    # Patrimoines
    path('patrimoines/', PatrimoineListCreateView.as_view(), name='patrimoine_list_create'),
    path('patrimoines/map-data/', PatrimoineMapView.as_view(), name='patrimoine_map_data'),
    path('patrimoines/nearby/', PatrimoineNearbyView.as_view(), name='patrimoine_nearby'),
    path('patrimoines/<int:pk>/', PatrimoineDetailView.as_view(), name='patrimoine_detail'),
    
    # Documentation Swagger
    path('docs/', include('rest_framework.urls', namespace='rest_framework')),
]
