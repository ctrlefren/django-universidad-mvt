from django.db import models


class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"


class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.matricula} - {self.nombre}"


class Curso(models.Model):
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=10, unique=True)

    # Relación 1:N (Un profesor dicta muchos cursos)
    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.CASCADE,
        related_name='cursos'
    )

    # Relación N:M (Muchos estudiantes cursan muchos cursos)
    estudiantes = models.ManyToManyField(
        Estudiante,
        related_name='cursos',
        blank=True
    )

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
        