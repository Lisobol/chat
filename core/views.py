import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, logout
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView
from django.views.generic.base import TemplateView
from core.forms import RegistrationForm, MessageForm, LoginForm, UploadFileForm
from core.models import User, Message, User_Pic, MessageFile


class LoginPageView(LoginView):
    template_name = "login.html"
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = reverse('login')
        return context

    def get_success_url(self):
        return reverse('chat')


class ChatPageView(TemplateView,LoginRequiredMixin):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_id = self.request.GET.get('last_id')
        if last_id:
            messages = Message.objects.filter(id__gt=last_id).order_by('-id')[:20]
        else:
            messages = Message.objects.all().order_by('-id')
        context['messages'] = messages
        return context

#
# class UploadView(TemplateView):
#     template_name = "upload.html"
#
#     def get_success_url(self):
#         return reverse('upload')
#
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/chat/')
#     else:
#         form = UploadFileForm()
#     return render(request,'chat.html',{'form':form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form.avatar = request.FILES['avatar']
        is_val = form.is_valid()
        data = form.cleaned_data
        if data['password'] != data['password2']:
            is_val = False
            form.add_error('password2', ['Пароли должны совпадать'])
        if User.objects.filter(username=data['username']).exists():
            form.add_error('username', ['Такой логин уже занят'])
            is_val = False
        if is_val:
            # us = User_Pic()
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            # us.avatar = data['avatar']

            user.save()
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


class MessageView(CreateView):
    form_class = MessageForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['post'])

    def get_success_url(self):
        return reverse('chat')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({
            'id': self.object.id,
            'text': self.object.text,
            'author': self.object.author.username,
            'time':self.object.time,
            # 'renderedTemplate':render_to_string(
            #     'message.html',{'message':self.object},self.request
            # )
        })


class MessagesView(LoginRequiredMixin, TemplateView):
    template_name = 'messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_id = self.request.GET.get('last_id')
        if last_id:
            messages = Message.objects.filter(id__gt=last_id).order_by('-id')
        else:
            messages = Message.objects.all().order_by('-id')
        context['messages'] = messages
        return context




    # def post(self, request, *args, **kwargs):
    #     form = MessageForm(request.POST)
    #     if form.is_valid():
    #         text = form.cleaned_data['text']
    #         message = Message()
    #         message.text = text
    #         message.save()
    #         return redirect('chat')
    #     return render(request, 'chat.html', {'form': form, 'form_action': reverse('chat')})
    #

def user_profile(request):
    errors = {}
    if request.method == 'POST':
        picture = request.FILES.get('picture')
        if not picture:
            errors['picture'] = 'Загрузите фото'
        if not errors:
            uid = request.user.id
            user = User.objects.get(id=uid)
            userpic = User_Pic(user=user,picture=picture)
            userpic.save()
            return HttpResponseRedirect('/user_profile')
        else:
            context = {'errors': errors, 'picture': picture}

    return render(request, 'user_profile.html', locals())

def upload_pic(request, HttpResponseForbidden=None):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uid = request.user.id
            user = User.objects.get(id=uid)
            m = User_Pic.objects.get(user=user)
            m.avatar = form.cleaned_data['avatar']
            m.save()
            return HttpResponseRedirect('/chat/')
    else:
        form = UploadFileForm()
    return render(request, 'user_profile.html', locals())

def upload_file(request, HttpResponseForbidden=None):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            m = MessageFile()
            m.file = form.cleaned_data['avatar']
            m.save()
            return HttpResponseRedirect('/chat/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', locals())


class UserpicObject(DetailView):
    model = User_Pic
    context_object_name = 'UserObject'
    template_name = 'user_profile.html'