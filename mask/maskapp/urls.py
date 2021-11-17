from django.urls import path

from .views import index, mask_img, mask_vid, video_feed


urlpatterns = [
    path('', index, name='home'),
    path('img/', mask_img, name='image'),
    path('vid/', mask_vid, name='video'),
    path('vid1/', video_feed, name='video_feed'), 
    
]