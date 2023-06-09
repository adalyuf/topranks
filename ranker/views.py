from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone, html
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger,)
from django.core.management import call_command
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages as djmessages
from django.views import generic, View
from django.urls import reverse, reverse_lazy
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme

from .models import Domain, KeywordFile, Conversation, Template, TemplateItem, Message, Project, ProjectUser, ProjectDomain, AIModel, Keyword
from .forms import KeywordFileForm, TemplateItemForm, MessageForm, TemplateForm, AddDomainToProjectForm, CreateConversationsForm

import csv
import os
import openai
import markdown
import json

class TemplateListView(generic.ListView):
    model = Template
    queryset = Template.objects.filter(project__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context) # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock']) # Include vendors and javascript files for dashboard widgets    
        context['form'] = TemplateForm()
        return context

class KeywordListView(generic.ListView):
    model = Keyword
    queryset = Keyword.objects.filter(answered_at__isnull=False).order_by('-answered_at')[:500]
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context) # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock']) # Include vendors and javascript files for dashboard widgets    
        context['kwtotal'] = Keyword.objects.count()
        context['kwavailable'] = Keyword.objects.filter(requested_at__isnull=True).count()
        context['kwpending'] = Keyword.objects.filter(requested_at__isnull=False).filter(answered_at__isnull=True).count()
        context['kwcompleted'] = Keyword.objects.filter(answered_at__isnull=False).count()
        if os.getenv("ENVIRONMENT") == "production":
            context['kw_batch_size'] = 10000
        else:
            context['kw_batch_size'] = 100
        return context

def keyword_search(request):
    user_search = request.GET['user_search']
    if user_search:
        queryset = Keyword.objects.filter(answered_at__isnull=False).filter(ai_answer__icontains=user_search)
    else:
        queryset = Keyword.objects.filter(answered_at__isnull=False) 
    return render(request, 'ranker/keyword_list.html', {'keyword_list': queryset})

def reset_keyword_queue(request):
    pending_keywords = Keyword.objects.filter(requested_at__isnull=False).filter(answered_at__isnull=True)
    item_list= []
    for keyword in pending_keywords:
        keyword.requested_at = None
        item_list.append(keyword)
    Keyword.objects.bulk_update(item_list, ["requested_at"], batch_size=5000)
    return redirect('keyword_list')

class KeywordDetailView(generic.DetailView):
    model = Keyword


def template_create(request, project_id=None):
    template_form = TemplateForm()
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            if project_id:
                project = get_object_or_404(Project, id=project_id)
                template.project = project
            template.save()
            return redirect('template_detail', template.id)
    return redirect('template_list')

def template_create_conversations(request):
    if request.method == 'POST':
        template = get_object_or_404(Template, id = request.POST['template_id'])
        ai_model = get_object_or_404(AIModel, id = request.POST['ai_model_id'])
        project = template.project
        domains = project.domain.all()
        for domain in domains:
            try:
                conversation = Conversation.objects.get(domain=domain, template=template, ai_model=ai_model, project=project)
                conversation.message_set.all().delete() #TODO: confirm that we actually want to delete all existing messages when rebuilding conversations from a template
            except:
                conversation = Conversation(domain=domain, template=template, ai_model=ai_model, project=project)
                conversation.save() 
            template_items = template.templateitem_set.all()
            for template_item in template_items:
                m = Message(
                    prompt      = template_item.prompt1, #TODO: Add logic that uses tokens and concatenates with other parts of prompt
                    title       = template_item.title,
                    visible     = template_item.visible,
                    order       = template_item.order,
                    conversation = conversation,
                    template_item = template_item,
                )
                m.prompt = m.prompt.replace("@currentDomain", conversation.domain.domain)
                m.save()
    return redirect('project_detail', project.id)    

    # How this generic view works:
    # Calls the template at .templates/<app>/<model>_list.html (templates/ranker/template_list.html)
    # Passes the object <model>_list (template_list)
    # queryset = Template.objects.all()
    # context = {'context_object_name': queryset}

    # Below are examples of how to override the defaults for generic list views
    # context_object_name = 'book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location


class GetTemplateView(View):

    def get(self, request, *args, **kwargs):
        view = TemplateDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TemplateDetailFormView.as_view()
        return view(request, *args, **kwargs)

class TemplateDetailView(generic.DetailView):
    model = Template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context) # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        template = self.get_object()
        context['ai_model_list'] = AIModel.objects.all()
        if template.project:
            self.request.session['template'] = template.id
            self.request.session['project'] = template.project.id
            domain_array = []
            domains = template.project.domain.all()
            for domain in domains:
                domain_array.append(domain.id)
            self.request.session['domains'] = domain_array
            context['create_conversations_form'] = CreateConversationsForm()
        context['form'] = TemplateItemForm()
        return context

class TemplateDetailFormView(SingleObjectMixin, FormView):
    template_name = 'ranker/template_detail.html'
    form_class = TemplateItemForm #We display the template item form
    model = Template #But look up things by the template class

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        template = self.get_object()
        form = self.get_form()
        if form.is_valid():
            template_item = form.save(commit=False)
            template_item.template = template
            template_item.order = 100
            template_item.save()
        return self.form_valid(form)

    def get_success_url(self):
        return reverse('template_detail', kwargs={'pk': self.object.pk})

@login_required
def template_delete(request, template_id):
    template = get_object_or_404(Template, pk=template_id)

    if request.method == 'POST':
        if template.project:
            project = template.project
            template.delete()
            return redirect('project_settings', project.id)
    template.delete()
    
    return redirect('template_list')

@login_required
def template_item_order(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    template_items = template.templateitem_set.all().order_by('order')

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        template_item_ids = json.loads(request.body) 
        index = 0
        while index < len(template_item_ids):
            pt = get_object_or_404(TemplateItem, pk=int(template_item_ids[index]))
            pt.order = index
            pt.save()
            index += 1
    form = TemplateItemForm()

    return render(request, 'ranker/template_detail.html', {'template':template, 'template_items':template_items, 'form': form})

@login_required
def template_item_delete(request, TemplateItem_id):
    template_item = get_object_or_404(TemplateItem, pk=TemplateItem_id)
    template = template_item.template

    if request.method == 'POST':
        template_item.delete()
    
    return redirect('template_detail', template.id)

class DashboardsView(TemplateView):
    template_name = 'pages/dashboards/index.html'

    # Predefined function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])

        return context


