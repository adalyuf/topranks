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

from ranker.models import Domain, KeywordFile, Conversation, Template, TemplateItem, Message, Project, ProjectUser, ProjectDomain, AIModel
from ranker.forms import KeywordFileForm, TemplateItemForm, MessageForm, TemplateForm, AddDomainToProjectForm

import csv
import os
import openai
import markdown
import json

class ProjectListView(generic.ListView):
    model = Project

    def get_queryset(self):
        user = self.request.user
        projects = user.project_set.all()
        return projects
    
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    global_template_list = Template.objects.filter(scope__exact='per_domain').filter(project__isnull=True)
    project_template_list = project.template_set.all()
    project_domain_list = project.domain.all()
    global_domain_list = Domain.objects.all()
    template_form = TemplateForm()
    domain_form = AddDomainToProjectForm()
    context = {}
    context['project'] = project
    context['global_template_list'] = global_template_list
    context['project_template_list'] = project_template_list
    context['project_domain_list'] = project_domain_list
    context['global_domain_list'] = global_domain_list
    context['template_form'] = template_form
    context['domain_form'] = domain_form
    return render(request, 'ranker/project_detail.html', context)

def project_add_domain(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    domain_id = request.POST['domain']
    domain = get_object_or_404(Domain, pk=domain_id)
    project.domain.add(domain)
    return redirect('project_detail', project.id)

def project_remove_domain(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    domain_id = request.POST['domain']
    domain = get_object_or_404(Domain, pk=domain_id)
    project.domain.remove(domain)
    return redirect('project_detail', project.id)

class ProjectCreate(CreateView):
    model = Project
    fields = ['project']
    
    def form_valid(self, form):
        project = form.save()
        user = self.request.user
        project.user.add(user)
        return super().form_valid(form)

class ProjectUpdate(UpdateView):
    model = Project
    fields = ['project']

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')