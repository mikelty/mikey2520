from blog.models import Post
from quote.models import Entry
from datetime import date
from random import seed, choice


def all_tags(request):
    return {
        'all_tags':{t:Post.objects.filter(tags__name__in=[t]) for t in Post.tags.all()},
    }

def all_posts(request):
    return {
        'all_posts':Post.objects.all(),
    }

def daily_quote(request):
	def to_integer(dt_time):
	    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

	seed(to_integer(date.today()))
	return {
	    'daily_quote':choice(Entry.objects.all()).content,
	}