from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RezultatiTreptanja(models.Model):
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    number_of_blinks = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user} trepnuo {self.number_of_blinks} puta  ({str(self.date_created)})'


class Customer(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    profile_pic = models.ImageField(null=True, blank=True, default= 'anonymous.jpg')  # null=True sets NULL (versus NOT NULL) on the column in your DB..
                                                            # blank determines whether the field will be required in forms. This includes the admin and your custom forms.
                                                            # If blank=True then the field will not be required, whereas if it's False the field cannot be blank.
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Zgrada(models.Model):
    ulica = models.CharField(max_length=255)
    broj = models.CharField(max_length=255)

    def __str__(self):
        return self.ulica + ' ' + self.broj

class Period(models.Model):
    pocetak = models.DateField(auto_now=False)
    kraj = models.DateField(auto_now=False)

    def __str__(self):
        return self.pocetak.strftime('%d-%m-%Y') + ' - ' + self.kraj.strftime('%d-%m-%Y')
    

class Stanar(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    zgrada = models.ForeignKey(Zgrada, on_delete=models.CASCADE, related_name='stanari')
    prezime = models.CharField(max_length=255)
    brojStana = models.IntegerField()
    mesecniIznos = models.DecimalField(decimal_places=2, max_digits=10)
    racunstanar = models.ManyToManyField(Period, through='RacunStanara')
    dugovanje = models.IntegerField(default = 0, verbose_name='dugovanje (rsd)')
    profile_pic = models.ImageField(null=True, blank=True, default= 'anonymous.jpg')

    def __str__(self):
        return  str(self.zgrada) + ', stan ' + str(self.brojStana) + ' (' + self.prezime + ')'

class RacunStanara(models.Model):
    stanar = models.ForeignKey(Stanar, on_delete=models.CASCADE, related_name='racuni')
    period = models.ForeignKey(Period, on_delete= models.CASCADE, related_name='racuni')

    iznos = models.DecimalField(decimal_places=2, max_digits=10)
    isPlatio = models.BooleanField(default=False)
    napomena = models.CharField(max_length=255)

    def __str__(self):
        return str(self.stanar) + ' za period ' + str(self.period)



class Oglasivac(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    imePrezime = models.CharField(max_length=255)
    tipOglasavanja = models.CharField(max_length=255)
    reklamaOglasivaca = models.ManyToManyField(Zgrada, through='Reklama')
    dugovanje = models.IntegerField(default = 0, verbose_name='dugovanje (rsd)')


    def __str__(self):
        return self.imePrezime + '(' + self.tipOglasavanja + ')'

class Reklama(models.Model):
    oglasivac = models.ForeignKey(Oglasivac, on_delete=models.CASCADE, related_name='reklame')
    zgrada = models.ForeignKey(Zgrada, on_delete= models.CASCADE, related_name='reklame')

    ime = models.CharField(max_length=255)
    mesecniIznos = models.IntegerField()
    racunReklam = models.ManyToManyField(Period, through='RacunReklama')


    def __str__(self):
        return self.ime + ' -> ' + str(self.oglasivac) + ' ' + str(self.zgrada)

class RacunReklama(models.Model):
    reklama = models.ForeignKey(Reklama, on_delete=models.CASCADE, related_name='racunireklama')
    period = models.ForeignKey(Period, on_delete= models.CASCADE, related_name='racunireklama')

    iznos = models.DecimalField(decimal_places=2, max_digits=10)
    isPlatio = models.BooleanField(default=False)
    napomena = models.CharField(max_length=255)

    def __str__(self):
        return str(self.reklama) + ' za period ' + str(self.period)
