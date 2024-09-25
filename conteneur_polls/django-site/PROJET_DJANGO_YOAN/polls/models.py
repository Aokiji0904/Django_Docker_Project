from django.db import models

class Serveur(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Classe(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Contenu(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Niveau(models.Model):
    valeur = models.IntegerField()

    def __str__(self):
        return str(self.valeur)

  
    

class Personnage(models.Model):
    name = models.CharField(max_length=100)
    serveur = models.ForeignKey(Serveur, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    contenu = models.ForeignKey(Contenu, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.classe.name})"

    class Meta:
        ordering = ['-score']