from django.contrib import admin
from .models import Zgrada, Stanar, Period, Oglasivac, RacunStanara, Reklama, RacunReklama, RezultatiTreptanja

# Register your models here.

admin.site.register(Zgrada)
admin.site.register(Stanar)
admin.site.register(Period)
admin.site.register(Oglasivac)
admin.site.register(RacunStanara)
admin.site.register(Reklama)
admin.site.register(RacunReklama)
admin.site.register(RezultatiTreptanja)