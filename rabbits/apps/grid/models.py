from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _ 

from package.models import BaseModel, Package


class Grid(BaseModel):

    title        = models.CharField(_('Title'), max_length=100)
    slug         = models.SlugField(_('Slug'))    
    description  = models.TextField(_('Description'), blank=True, help_text="Lines are broken and urls are urlized")
    is_locked    = models.BooleanField(_('Is Locked'), default=False, help_text="Moderators can lock grid access")
    
    def elements(self):
        elements = []
        for feature in self.feature_set.all(): 
            for element in feature.element_set.all(): 
                elements.append(element)
        return elements
                    
    def __unicode__(self):
        return self.title

class GridPackage(BaseModel):
    """ These are Packages on one side of the grid 
        Have to make this intermediary table to get things to work right
    """
    
    grid        = models.ForeignKey(Grid)
    package     = models.ForeignKey(Package)
    
    class Meta:
        
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'        
        
    def __unicode__(self):
        return '%s : %s' % (self.grid.slug, self.package.slug)
    
class Feature(BaseModel):
    """ These are the features measured against a grid """
    
    grid         = models.ForeignKey(Grid)
    title        = models.CharField(_('Title'), max_length=100)
    description  = models.TextField(_('Description'), blank=True)
    
    def __unicode__(self):
        return '%s : %s' % (self.grid.slug, self.title)    
    
class Element(BaseModel):
    """ The individual table elements """
    
    grid_package = models.ForeignKey(GridPackage)
    feature      = models.ForeignKey(Feature)
    text         = models.TextField(_('text'), blank=True, help_text="very limited formatting is allowed!")
    
    def __unicode__(self):
        return '%s : %s : %s' % (self.grid_package.grid.slug, self.grid_package.package.slug, self.feature.title)
    
    