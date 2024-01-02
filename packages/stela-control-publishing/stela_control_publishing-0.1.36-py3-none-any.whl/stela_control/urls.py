from django.urls import path, include
from . import views, validators
  
app_name="stela"

urlpatterns = [
    #stela Home
    path('i18n/', include('django.conf.urls.i18n')),
    path('meta-data/', views.metaID, name="meta_data"),
    path('ig-data/', views.igID, name="ig_data"),
    path('meta-api/', views.metaAPI, name="meta_request"),
    path('validators/', views.validators, name="validators"),
    path('api-control/', views.StelaAPIView, name="api_view"),

    #Stela Dashboard
    path('console/newcomer', views.newcomer, name="newcomer"),
    path('console/home', views.console, name="console"),
    path('pro-stela/chats/', views.stelaChat, name="chats"),
    path('pro-stela/expert', views.stelaExpert, name="expert"),

    #access
    path('', views.loginstela, name='login'),
    path('logout/', views.logout_view, name="logout"),

    #Inbox
    path('content/inbox', views.contactMessage, name="inbox"), 
    
    #Comments
    path('comments-blog', views.commentsBlog, name="commentsBlog"),

    #StelaContent
    path('dycontent', views.mainContent, name="main-content"),
    path('dycontent/main', views.siteMain, name="site-main"),
    path('dycontent/docs', views.siteDocs, name="site-docs"),
    path('dycontent/staff', views.staff, name="site-staff"),
    path('dycontent/stela-story', views.stelaStory, name="stela_story"),
    
    #inventory
    path('inventory-control/services', views.publishing, name="publishing"),

    #metaplatform
    path('marketing/business-suite', views.metaSuite, name="meta_business"),
    path('marketing/business-suite/<int:id>', views.metaDetail, name="meta_detail"),
    path('marketing/business-suite/<int:id>/content-pro', views.page, name="fb_page"),
    path('marketing/business-suite/<int:id>/analythics', views.pageAnalythics, name="page_insights"),
    path('marketing/<int:id>/icreative-actions/<int:ig>/', views.IcreativeActions, name="ic_actions"),
    path('marketing/business-suite/<int:id>/insight-creative/<int:ig>', views.insightCreative, name="increative"),
    path('marketing/business-suite/<int:id>/analyzer/<int:ig>', views.igAnalyzer, name="iganalyzer"),
    path('marketing/business-suite/fbmedia', views.fbmedia, name="fb_media"),
    path('marketing/business-suite/igmedia', views.igmedia, name="ig_media"),
    path('marketing/business-suite/ig-counter/<int:id>/', views.igCounter, name="ig_counter"),
    path('marketing/business-suite/ig-check/<int:id>/', views.igCheckPost, name="check_ig_post"),
    path('marketing/<int:id>/grid/<int:ig>/', views.grid, name="ig_grid"),
    
    #googlePlatform
    path('googleapis/auth', views.googleAuth, name="google_auth"),

    # #reviews
    # path('reviews-list', views.reviews_list, name="review_list"),
    # path('update-review/<int:id>/', views.update_review, name="update_review"),
    # path('delete-review/', views.delete_reviews, name="delete_review"),
    # path('search-auto/review/', views.autocompleteReview, name="autocomplete_review"),
    
    #users
    path('users-control', views.users, name="users"),
    path('users/<int:id>/', views.update_users, name="update_user"),
    path('subscribers-control', views.subscribers, name="subscribers"),
    path('subscribers-control/<int:id>/', views.update_subscribers, name="update_subscribers"),

    #StelaValidationSystem
    path('validations/accounts/', validators.accountsData, name="accounts_data"),
    path('validations/content/', validators.contentData, name="content_data"),
    path('validations/docs/', validators.docsData, name="docs_data"),
    path('validations/staff/', validators.staffData, name="staff_data"),
    path('validations/stela-story/', validators.stelaStoryData, name="stela_story_data"),
    path('validations/inventory/', validators.inventoryData, name="inventory_data"),
    path('validations/booking/', validators.bookingData, name="booking_data"),
    path('validations/inputs/', validators.inputsData, name="inputs_data"),
    path('validations/stela-api/', validators.requestAPI, name="api_data"),
    path('validations/jobs/', validators.jobApplication, name="jobs_data"),
    path('validations/handlers/', validators.coreHandlers, name="handlers_data"),
    path('validations/youtube-playlist/', validators.get_youtube_playlist_videos, name="playlist_data"),
    # path('validations/billing/', validators.billingData, name="billind_data"),
    path('validations/sendgrid/<int:id>/<int:ig>/', validators.sendgridData, name="sendgrid_data"),
    path('validations/facebook/<int:id>/', validators.sendgridData, name="sendgrid_data"),
    path('validations/instagram/<int:id>/<int:ig>/', validators.sendgridData, name="sendgrid_data"),
    # path('validations/payments/', views.siteMain, name="site-main"),
    #validateURL
    path('auth/password_reset_confirm/<uidb64>/<token>/', validators.new_password_activate, name="password_reset_token"),
    path('auth/account/<uidb64>/<token>/', validators.account_activate, name="account_token"),
]