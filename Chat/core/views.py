from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from core.forms import RegistrationForm, MessageForm, LoginForm
from core.models import User, Message


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
        messages = Message.objects.all()
        context['messages'] = messages
        return context


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def registration(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        is_val = form.is_valid()
        data = form.cleaned_data
        if data['password'] != data['password2']:
            is_val = False
            form.add_error('password2', ['Пароли должны совпадать'])
        if User.objects.filter(username=data['username']).exists():
            form.add_error('username', ['Такой логин уже занят'])
            is_val = False
        if is_val:
            new_user = User.objects.create_user(data['username'], data['email'], data['password'])
            print(new_user)
            user = User()
            user.user = new_user
            user.email = data['email']
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
    #

# class RegistrationView(RegistrationForm):
#     def get(self,request,*args,**kwargs):
#         form = RegistrationForm(request.POST)
#         return render(request,'registration.html',{'form':form})
#
#
#     def post(self,request,*args,**kwargs):
#         if request.method == 'POST':
#             form = RegistrationForm(request.POST)
#             is_val = form.is_valid()
#             data = form.cleaned_data
#             if data['password'] != data['password2']:
#                 is_val = False
#                 form.add_error('password2', ['Пароли должны совпадать'])
#             if User.objects.filter(username=data['username']).exists():
#                 form.add_error('username', ['Такой логин уже занят'])
#                 is_val = False
#             if is_val:
#                 new_user = User.objects.create_user(data['username'], data['email'], data['password'])
#                 print(new_user)
#                 user = User()
#                 user.user = new_user
#                 user.email = data['email']
#                 user.save()
#                 return HttpResponseRedirect('/')
#             else:
#                 form = RegistrationForm()
#         return render(request, 'registration.html', {'form': form})
