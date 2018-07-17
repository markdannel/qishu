import datetime
from haystack import indexes
from novel.models import Name, Chaptername
 
class NameIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    name = indexes.CharField(model_attr='xs_name')
    author = indexes.CharField(model_attr='xs_author')
    category = indexes.CharField(model_attr='category')
 
    def get_model(self):
        return Name
 
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

#class ChapternameIndex(indexes.SearchIndex, indexes.Indexable):
#    text = indexes.CharField(document=True, use_template=True)
    
#    name = indexes.CharField(model_attr='xs_chaptername')
#    content = indexes.CharField(model_attr='xs_content')
 
#    def get_model(self):
#        return Chaptername
 
#    def index_queryset(self, using=None):
#        """Used when the entire index for model is updated."""
#        return self.get_model().objects.all()