from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from esame.models import Battute, Recensioni, ProfiloDettagliato


class HomeView(ListView):
    template_name = 'home.html'
    model = Battute


class RegistrazioneView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registrazione.html'
    success_url = reverse_lazy('home')


class AggiungiBattuta(LoginRequiredMixin, CreateView):
    model = Battute
    template_name = 'aggiunta_battuta.html'
    fields = ('testo', 'tipo')
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.utente = self.request.user
        return super().form_valid(form)


class ProfiloView(DetailView):
    template_name = 'profilo.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(ProfiloView, self).get_context_data(**kwargs)
        context['profilo'] = ProfiloDettagliato.objects.get(utente=self.request.user)
        return context


class AggiungiRecensione(LoginRequiredMixin, CreateView):
    model = Recensioni
    template_name = 'aggiungi_recensione.html'
    fields = ('voto',)
    success_url = reverse_lazy('home')

    def form_valid(self, form, ):
        form.instance.utente = self.request.user
        form.instance.battuta_id = self.kwargs['pk']
        return super().form_valid(form)


class ModificaProfilo(LoginRequiredMixin, UpdateView):
    model = ProfiloDettagliato
    template_name = 'modifica_profilo.html'
    fields = ('nome', 'cognome', 'foto_profilo', 'datadinascita', 'email', 'citta', 'bio')
    success_url = reverse_lazy('home')