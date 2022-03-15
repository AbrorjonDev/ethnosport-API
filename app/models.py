from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

User = get_user_model()

from phonenumber_field.modelfields import PhoneNumberField


class RegionModel(models.Model):

    name = models.CharField(max_length=30, verbose_name=_('Regions'))
    email = models.EmailField(null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    phone = PhoneNumberField(
        blank=True, null=True, verbose_name=_('Phone'), 
        help_text='+998971661186'
        )
    boss = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Boss'))
    address = models.CharField(max_length=2000, null=True, blank=True)
    d = models.TextField(blank=True, null=True, help_text='for using in map.')
    reg_id = models.CharField(max_length=10, null=True, blank=True, help_text='for using in map.')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
    
        ordering = ('id', )

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        super(RegionModel, self).save(*args, **kwargs)
        if not self.email:
            try:
                self.email = self.admin.email
            except:
                pass


class Sports(models.Model):

    name = models.CharField(max_length=200, verbose_name='Sport name')
    slug = models.SlugField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug !=slugify(self.name):
            self.slug = slugify(self.name)
        return super(Sports, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def sport_images(self):
        return self.sport_img.all()
    

class SportImages(models.Model):
    sport = models.ForeignKey(Sports, on_delete=models.CASCADE, related_name='sport_img')
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return '{0} for {1}'.format(self.image.name, self.sport.name)



class Category(models.Model):

    name = models.CharField(max_length=200, verbose_name='Sportsman\'s category')


class Sportsmen(models.Model):

    name = models.CharField(max_length=200, verbose_name='Sportsman\'s name')
    date = models.DateField(null=True, blank=True)
    achievements = ArrayField(
        models.TextField(), size=100, null=True, blank=True
    )
    category = models.ManyToManyField(Category, default=None, related_name='category')
    sport = models.ForeignKey(Sports, on_delete=models.SET_NULL, null=True, blank=True, related_name='sport')
    region = models.ForeignKey(RegionModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='region')

    class Meta:
        verbose_name = _('Sportsman')
        verbose_name_plural = _('Sportsmen')
    
        ordering = ('id', )

    def __str__(self) -> str:
        return self.name

    @property
    def sportsman_images(self):
        return self.sportman_image.all()

    @property
    def main_sportman_image(self):
        return '{0}'.format(self.sportman_image.first().image.url)   
    

class SportsmenImages(models.Model):
    sportsman = models.ForeignKey(Sportsmen, on_delete=models.CASCADE, related_name='sportman_image')
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return '{0} for {1}'.format(self.image.name, self.sportsman.name)

class Events(models.Model):

    name = models.CharField(max_length=200, verbose_name=_('Event\'s name'))
    text = models.TextField(null=True, blank=True)
    videos = ArrayField(
        models.URLField(), size=100, null=True, blank=True
    )
    seen = models.BooleanField(default=False)
    rate = models.FloatField(default=0.0)
    region = models.ForeignKey(RegionModel, on_delete=models.SET_NULL, null=True, blank=True)
    date_occured = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

        ordering = ( 'date_created', 'date_updated',)


class Competitions(models.Model):
    name = models.CharField(max_length=300, verbose_name=_('name'))
    sports = models.ManyToManyField(Sports, default=None, related_name='sports')
    pdf = models.FileField(upload_to='competitions', null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def competition_images(self):
        return self.competition_images.all()

    @property
    def main_competition_image(self):
        try:
            return self.competition_images.first().image
        except:
            return None

    @property
    def get_comments(self):
        return self.comments.all()

class CompetitionImages(models.Model):
    competition = models.ForeignKey(Competitions, on_delete=models.CASCADE, related_name='competition_images')
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.image


class CommentsINCompetitions(models.Model):
    competition = models.ForeignKey(Competitions, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=3000)
    name = models.CharField(max_length=200, help_text='Who is commenting?')
    rate = models.FloatField(default=0.0)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.competition.name

class Videos(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    video = models.FileField(upload_to='videos')


    def save(self, *args,**kwargs):
        
        if not self.name:
            self.name = self.video.name
        return super(Videos, self).save(*args,**kwargs)

class Fotos(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    foto = models.FileField(upload_to='foros')

    def save(self, *args,**kwargs):
        if not self.name:
            self.name = self.video.name
        return super(Fotos, self).save(*args,**kwargs)


class CategoryDocs(models.Model):
    name = models.CharField(max_length=2000)

    def __str__(self):
        return self.name

    @property
    def get_docs(self):
        return self.docs.all()
        

class Docs(models.Model):
    category = models.ForeignKey(CategoryDocs, on_delete=models.SET_NULL, null=True, related_name='docs')
    name = models.CharField(max_length=1000, null=True, blank=True)
    doc = models.FileField(upload_to='docs', null=True, blank=True)
    doc_url = models.URLField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.name and self.doc:
            self.name = self.doc.name
        return super(Docs, self).save(*args, **kwargs)









