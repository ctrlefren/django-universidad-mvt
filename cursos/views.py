from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Curso, Profesor, Estudiante
from .forms import CursoForm, EstudianteForm


# ---------- CURSOS ----------


class CursoListView(ListView):
    model = Curso
    template_name = 'cursos/lista.html'
    context_object_name = 'cursos'
    paginate_by = 6  # Máximo 6 cursos por página

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(codigo__icontains=query) |
                Q(profesor__nombre__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class CursoDetailView(DetailView):
    model = Curso
    template_name = 'cursos/detalle.html'
    context_object_name = 'curso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiantes'] = self.object.estudiantes.all()
        return context


class CursoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/formulario.html'
    success_url = reverse_lazy('web_lista_cursos')
    success_message = "¡El curso '%(nombre)s' fue creado exitosamente!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nuevo Curso'
        return context


class CursoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/formulario.html'
    success_url = reverse_lazy('web_lista_cursos')
    success_message = "¡El curso '%(nombre)s' fue actualizado correctamente!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Curso: {self.object.nombre}'
        return context


class CursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = 'cursos/curso_confirm_delete.html'
    success_url = reverse_lazy('web_lista_cursos')
    context_object_name = 'curso'

    def form_valid(self, form):
        messages.warning(self.request, f"El curso '{self.object.nombre}' fue eliminado del sistema.")
        return super().form_valid(form)


# ---------- PROFESORES ----------

class ProfesorListView(ListView):
    model = Profesor
    template_name = 'cursos/profesores_lista.html'
    context_object_name = 'profesores'
    paginate_by = 3  # Máximo 3 profesores por página


class ProfesorDetailView(DetailView):
    model = Profesor
    template_name = 'cursos/profesor_detalle.html'
    context_object_name = 'profesor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = self.object.cursos.all()
        return context


# ---------- LOGIN CON BIENVENIDA ----------

class LoginBienvenidaView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.info(self.request, f"¡Bienvenido, {form.get_user().username}!")
        return super().form_valid(form)

# ---------- ESTUDIANTES ----------

class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'cursos/estudiantes_lista.html'
    context_object_name = 'estudiantes'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(matricula__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = 'cursos/estudiante_detalle.html'
    context_object_name = 'estudiante'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos_inscritos'] = self.object.cursos.all()
        context['cursos_disponibles'] = Curso.objects.exclude(estudiantes=self.object)
        return context


class EstudianteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'cursos/estudiante_formulario.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    success_message = "¡El estudiante '%(nombre)s' fue registrado con éxito hermano!"


class EstudianteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'cursos/estudiante_formulario.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    success_message = "¡Los datos del estudiante '%(nombre)s' fueron actualizados correctamente pa!"


class EstudianteDeleteView(LoginRequiredMixin, DeleteView):
    model = Estudiante
    template_name = 'cursos/estudiante_confirm_delete.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    context_object_name = 'estudiante'

    def form_valid(self, form):
        messages.warning(self.request, f"El estudiante '{self.object.nombre}' fue eliminado.")
        return super().form_valid(form)


@login_required
@require_POST
def inscribir_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    curso = get_object_or_404(Curso, pk=request.POST.get('curso'))
    curso.estudiantes.add(estudiante)
    messages.success(request, f"{estudiante.nombre} fue inscrito en '{curso.nombre}'.")
    return redirect('web_detalle_estudiante', pk=pk)        