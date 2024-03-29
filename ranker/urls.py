from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from ranker import views
from ranker.domains import views as domain_views
from ranker.conversations import views as conv_views
from ranker.projects import views as project_views



urlpatterns = [
    path("", domain_views.DomainListView.as_view(), name="home"),
    path("sitemap.xml", views.sitemap, name="sitemap_index"),
    path("sitemap-static.xml", views.sitemap_static, name="sitemap_static"),
    path("media/sitemaps/<str:folder>/sitemap-<str:category>-<int:page_num>.xml", views.sitemap_redirect, name="sitemap_redirect"),
    path("robots.txt",TemplateView.as_view(template_name="ranker/robots.txt", content_type="text/plain")),  #add the robots.txt file


    path('dashboard/', views.DashboardsView.as_view(template_name = 'pages/dashboards/index.html'), name='dashboard'),

    path("domains/"                                 , domain_views.DomainListView.as_view()     , name="domain_list"),
    path("domain_search/"                           , domain_views.domain_search                , name="domain_search"),
    path('domains/<int:domain_id>/'                 , domain_views.domain_detail                , name='domain_detail'),
    path('domains/<int:domain_id>/<slug:slug>/'     , domain_views.domain_detail                , name='domain_detail'),


    path('keywordfile_make_primary/<int:domain_id>/<int:keywordfile_id>/'   , login_required(domain_views.keywordfile_make_primary) , name='keywordfile_make_primary'),
    path('get_keyword_responses/<int:batch_multiplier>/'                    , login_required(domain_views.get_keyword_responses)    , name='get_keyword_responses'),
    path('get_business_data/'                                               , login_required(domain_views.get_business_data)        , name='get_business_data'),
    path('index_brands/'                                                    , login_required(domain_views.index_brands)             , name='index_brands'),

    path('conversations/<int:conversation_id>/'                     , login_required(conv_views.conversation_detail)                 , name='conversation_detail'),
    path('conversations/add/<int:template_id>/<int:domain_id>/<int:ai_model_id>/', login_required(conv_views.conversation_add)       , name='conversation_add'),
    path('conversations/edit/<int:conversation_id>/'                , login_required(conv_views.conversation_edit)                   , name='conversation_edit'),
    path('conversations/edit/<int:conversation_id>/update_order/'   , login_required(conv_views.conversation_update_order)           , name='conversation_update_order'),
    path('conversations/edit/<int:conversation_id>/get_responses/'  , login_required(conv_views.conversation_get_responses)          , name='conversation_get_responses'),

    path('messages/delete/<int:message_id>/'            , conv_views.message_delete, name='message_delete'),

    path("templates/"                                   , login_required(views.TemplateListView.as_view())      , name="template_list"),
    path("templates/create/"                            , login_required(views.template_create)                 , name="template_create"),
    path("templates/create/<int:project_id>/"           , login_required(views.template_create)                 , name="template_create"),
    path("templates/create_conversations/"              , login_required(views.template_create_conversations)   , name="template_create_conversations"),
    path("templates/<int:pk>/"                          , login_required(views.GetTemplateView.as_view())       , name="template_detail"),
    path("templates/delete/<int:template_id>/"          , login_required(views.template_delete)                 , name="template_delete"),
    path("templates/<int:template_id>/update_order/"    , login_required(views.template_item_order)             , name="template_item_order"),
    path("template_items/delete/<int:TemplateItem_id>/" , login_required(views.template_item_delete)            , name="template_item_delete"),

    path("projects/"                                    , login_required(project_views.ProjectListView.as_view())       , name="project_list"),
    path("projects/<int:project_id>/"                   , login_required(project_views.project_detail)                  , name="project_detail"),
    path("projects/<int:project_id>/settings/"          , login_required(project_views.project_settings)                , name="project_settings"),
    path("projects/<int:project_id>/settings/<str:setting>/", login_required(project_views.project_settings)            , name="project_settings"),
    path("projects/<int:project_id>/remove_domain/"     , login_required(project_views.project_remove_domain)           , name="project_remove_domain"),
    path("projects/<int:project_id>/remove_user/"       , login_required(project_views.project_remove_user)             , name="project_remove_user"),
    path("projects/<int:project_id>/get_responses/"     , login_required(project_views.project_get_all_responses)       , name="project_get_all_responses"),
    path('projects/create/'                             , login_required(project_views.ProjectCreate.as_view())         , name='project_create'),
    path('projects/<int:pk>/update/'                    , login_required(project_views.ProjectUpdate.as_view())         , name='project_update'),
    path('projects/<int:pk>/delete/'                    , login_required(project_views.ProjectDelete.as_view())         , name='project_delete'),

    path("keywords/"                        , login_required(views.KeywordListView.as_view())       , name='keyword_list'),
    path("keywords/<int:pk>/"               , views.KeywordDetailView.as_view()                     , name='keyword_detail'),
    path("keywords/<int:pk>/<slug:slug>/"   , views.KeywordDetailView.as_view()                     , name='keyword_detail'),
    path("keywords/<slug:slug>-<int:pk>/"   , views.KeywordDetailView.as_view()                     , name='keyword_detail'),
    path("keywords/keyword_search/"         , login_required(views.keyword_search)                  , name="keyword_search"),
    path("keywords/reset_keyword_queue/"    , login_required(views.reset_keyword_queue)             , name="reset_keyword_queue"),
    path("keywords/gap/"                    , login_required(views.keyword_gap)                     , name='keyword_gap'),
    path("keywords/gap/<int:brand1_id>/<int:brand2_id>/", login_required(views.keyword_gap)         , name='keyword_gap'),
    path("keywords/gap/autocomplete-brands/", login_required(views.autocomplete_brands)             , name='autocomplete_brands'),
    path("keywords/answer/<int:ai_model_id>/<int:keyword_id>/", login_required(views.keyword_answer), name='keyword_answer'),


]