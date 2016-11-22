from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView
from .forms import ReviewForm
# from django.http import HttpResponse # we can remove it cause we dont use it now.
from .models import Author, Book #We now import Author too!
# Create your views here.

def list_books(request):
	"""
	List the books that have reviews
	"""

	books = Book.objects.exclude(date_reviewed__isnull=True).prefetch_related('authors')

	context = {
		'books': books,
	}

	return render(request, "list.html", context)



class AuthorList(View):
	def get(self, request):
		authors = Author.objects.annotate(
			published_books = Count('books')
		).filter(
			published_books__gt = 0
		)
		context = {'authors': authors, }

		return render(request, 'authors.html', context)


class BookDetail(DetailView):
	model = Book
	template_name = 'book.html'


class AuthorDetail(DetailView):
	model = Author
	template_name = 'author.html'



def review_books(request):
	"""
	List all of the books that we want to review.
	"""
	books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')
	form = ReviewForm

	context = {
		'books': books,
		'form': form,
	}

	return render(request, "list-to-review.html", context)


def review_book(request, pk):
	"""
	Review an individual book
	"""
	book = get_object_or_404(Book, pk=pk)

	context = {
		'book': book,
	}

	return render(request, "review-book.html", context)
