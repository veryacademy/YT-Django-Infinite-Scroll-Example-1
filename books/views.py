from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from books.models import Books
from . forms import AddForm
from django.db.models import F
from django.utils import timezone
# from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


# def redirect_view(request):
#     response = redirect('/books/')
#     return response
def redirect_view(request):
    response = redirect('books: ex2', permanent=False)

    return response


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(),
                                     self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/books')

        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class BookEditView(UserAccessMixin, UpdateView):
    permission_required = ('books.change_books')
    model = Books
    form_class = AddForm
    template_name = 'add.html'
    success_url = '/books/'


class AddBookView(CreateView):
    model = Books
    form_class = AddForm
    template_name = 'add.html'
    success_url = '/books/'


class IndexView(ListView):

    model = Books
    template_name = "home.html"
    context_object_name = 'books'
    paginate_by = 2

    # queryset = Books.objects.all()[:2]
    # def get_queryset(self):
    # return Books.objects.all()[:3]


class GenreView(ListView):
    model = Books
    template_name = 'home.html'
    context_object_name = 'books'
    paginate_by = 1  # Pagination over-write

    def get_queryset(self, *args, **kwargs):
        return Books.objects.filter(genre__icontains=self.kwargs.get('genre'))


class BookDetailView(DetailView):

    model = Books
    template_name = 'book-detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = Books.objects.filter(slug=self.kwargs.get('slug'))
        post.update(count=F('count') + 1)

        context['time'] = timezone.now()

        return context
