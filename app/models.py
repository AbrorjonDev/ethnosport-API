from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from decouple import config

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

    @property
    def get_sportsmen(self):
        return self.sportsmen.all()

    @property
    def get_sportsmen_count(self):
        return self.sportsmen.all().count()

    @property
    def get_events(self):
        return self.events.all()
    
    @property
    def get_events_count(self):
        return self.events.all().count()

    @property
    def statistics(self):
        ball=0
        rates = [event.rate for event in self.events.all()]
        for rate in rates:
            ball += rate
 #       print("Ball: ", ball)
#        print( "max ball: ", float(self.get_events_count*int(config('MAX_EVENT_BALL', default=20))))
        # return  ball
        if self.get_events_count:
            return round(ball/float(self.get_events_count*int(config('MAX_EVENT_BALL', default=20)))*100, 2)
        return 0
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
    slug = models.SlugField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    text = models.TextField(null=True, blank=True)
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
    def __str__(self):
        return self.name

class Sportsmen(models.Model):

    name = models.CharField(max_length=200, verbose_name='Sportsman\'s name')
    date = models.DateField(null=True, blank=True)
    achievements = ArrayField(
        models.TextField(), size=100, null=True, blank=True
    )
    category = models.ManyToManyField(Category, null=True, blank=True, default=None, related_name='category')
    sport = models.ForeignKey(Sports, on_delete=models.SET_NULL, null=True, blank=True, related_name='sport')
    region = models.ForeignKey(RegionModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='sportsmen')

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
        return self.sportman_image.first()
    

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
    region = models.ForeignKey(RegionModel, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='events')
    date_occured = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    visited = models.IntegerField(default=0, null=True, blank=True)


    @property
    def get_images(self):
        return self.images.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

        ordering = ( 'date_created', 'date_updated',)


class EventsImages(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='eventsimages')

    def __str__(self):
        return '{0} for {1}'.format(self.image.name, self.event.name)


class Competitions(models.Model):
    name = models.CharField(max_length=300, verbose_name=_('name'))
    sports = models.ManyToManyField(Sports, default=None, related_name='sports')
    pdf = models.FileField(upload_to='competitions', null=True, blank=True)
    region = models.ForeignKey(RegionModel, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='competitionimages', null=True, blank=True)
    download_counter = models.IntegerField(default=0)
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
        return f'{self.competition.name} {self.id}'


class CommentsINCompetitions(models.Model):
    competition = models.ForeignKey(Competitions, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=3000)
    name = models.CharField(max_length=200, help_text='Who is commenting?')
#    rate = models.FloatField(default=0.0)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.competition.name

class Videos(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name

    def save(self, *args,**kwargs):
        if not self.video and not self.url:
            raise ValidationError('Kamida bitta sohani to\'ldiring: (\'video\', \'url\')')
        if not self.name:
            self.name = self.video.name
        return super(Videos, self).save(*args,**kwargs)

class Fotos(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    foto = models.FileField(upload_to='foros')

    def __str__(self):
        return self.name

    def save(self, *args,**kwargs):
        if not self.name:
            self.name = self.video.name
        return super(Fotos, self).save(*args,**kwargs)


class CategoryDocs(models.Model):
    name = models.CharField(max_length=2000)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name


class News(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(null=True, blank=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    #image = models.ImageField(upload_to='newsimages', null=True, blank=True)
    def __str__(self):
        return self.name

    @property
    def news_images(self):
        return self.images.all()
    @property
    def main_image(self):
        if self.images.all().count():
            return self.images.first()

class NewsImages(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news_images')

    def __str__(self):
        return f'{self.news.name} {self.id}'




