from django.urls import reverse_lazy

from django_async_extensions.acore.paginator import AsyncPaginator
from django_async_extensions.aviews import generic

from .forms import ContactForm
from .models import Artist, Author, Page, Book, BookSigning


class CustomTemplateView(generic.AsyncTemplateView):
    template_name = "test_generic_views/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"key": "value"})
        return context


class ObjectDetail(generic.AsyncDetailView):
    template_name = "test_generic_views/detail.html"

    async def get_object(self):
        return {"foo": "bar"}


class ArtistDetail(generic.AsyncDetailView):
    queryset = Artist.objects.all()


class AuthorDetail(generic.AsyncDetailView):
    queryset = Author.objects.all()


class AuthorCustomDetail(generic.AsyncDetailView):
    template_name = "test_generic_views/author_detail.html"
    queryset = Author.objects.all()

    async def get(self, request, *args, **kwargs):
        # Ensures get_context_object_name() doesn't reference self.object.
        author = await self.get_object()
        context = {"custom_" + self.get_context_object_name(author): author}
        return self.render_to_response(context)


class PageDetail(generic.AsyncDetailView):
    queryset = Page.objects.all()
    template_name_field = "template"


class CustomContextView(generic.detail.AsyncSingleObjectMixin, generic.AsyncView):
    model = Book
    object = Book(name="dummy")

    async def get_object(self):
        return Book(name="dummy")

    def get_context_data(self, **kwargs):
        context = {"custom_key": "custom_value"}
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_context_object_name(self, obj):
        return "test_name"


class CustomSingleObjectView(generic.detail.AsyncSingleObjectMixin, generic.AsyncView):
    model = Book
    object = Book(name="dummy")


class NonModel:
    id = "non_model_1"

    _meta = None


class NonModelDetail(generic.AsyncDetailView):
    template_name = "test_generic_views/detail.html"
    model = NonModel

    async def get_object(self, queryset=None):
        return NonModel()


class ObjectDoesNotExistDetail(generic.AsyncDetailView):
    async def get_queryset(self):
        return Book.does_not_exist.all()


class ContactView(generic.AsyncFormView):
    form_class = ContactForm
    success_url = reverse_lazy("authors_list")
    template_name = "test_generic_views/form.html"


class LateValidationView(generic.AsyncFormView):
    form_class = ContactForm
    success_url = reverse_lazy("authors_list")
    template_name = "test_generic_views/form.html"

    async def form_valid(self, form):
        form.add_error(None, "There is an error")
        return await self.form_invalid(form)


class AuthorGetQuerySetFormView(generic.edit.AsyncModelFormMixin):
    fields = "__all__"

    async def get_queryset(self):
        return Author.objects.all()


class DictList(generic.AsyncListView):
    """A ListView that doesn't use a model."""

    queryset = [{"first": "John", "last": "Lennon"}, {"first": "Yoko", "last": "Ono"}]
    template_name = "test_generic_views/list.html"


class ArtistList(generic.AsyncListView):
    template_name = "test_generic_views/list.html"
    queryset = Artist.objects.all()


class AuthorList(generic.AsyncListView):
    queryset = Author.objects.all()


class AuthorListGetQuerysetReturnsNone(AuthorList):
    async def get_queryset(self):
        return None


class BookList(generic.AsyncListView):
    model = Book


class CustomPaginator(AsyncPaginator):
    def __init__(self, queryset, page_size, orphans=0, allow_empty_first_page=True):
        super().__init__(
            queryset,
            page_size,
            orphans=2,
            allow_empty_first_page=allow_empty_first_page,
        )


class AuthorListCustomPaginator(AuthorList):
    paginate_by = 5

    def get_paginator(
        self, queryset, page_size, orphans=0, allow_empty_first_page=True
    ):
        return super().get_paginator(
            queryset,
            page_size,
            orphans=2,
            allow_empty_first_page=allow_empty_first_page,
        )


class CustomMultipleObjectMixinView(
    generic.list.AsyncMultipleObjectMixin, generic.AsyncView
):
    queryset = [
        {"name": "John"},
        {"name": "Yoko"},
    ]

    async def get(self, request):
        self.object_list = await self.get_queryset()


class BookConfig:
    queryset = Book.objects.all()
    date_field = "pubdate"


class BookArchive(BookConfig, generic.AsyncArchiveIndexView):
    pass


class BookYearArchive(BookConfig, generic.AsyncYearArchiveView):
    pass


class BookMonthArchive(BookConfig, generic.AsyncMonthArchiveView):
    pass


class BookWeekArchive(BookConfig, generic.AsyncWeekArchiveView):
    pass


class BookDayArchive(BookConfig, generic.AsyncDayArchiveView):
    pass


class BookTodayArchive(BookConfig, generic.AsyncTodayArchiveView):
    pass


class BookDetail(BookConfig, generic.AsyncDateDetailView):
    pass


class BookDetailGetObjectCustomQueryset(BookDetail):
    async def get_object(self, queryset=None):
        return await super().get_object(
            queryset=Book.objects.filter(pk=self.kwargs["pk"])
        )


class BookSigningConfig:
    model = BookSigning
    date_field = "event_date"
    # use the same templates as for books

    def get_template_names(self):
        return ["test_generic_views/book%s.html" % self.template_name_suffix]


class BookSigningArchive(BookSigningConfig, generic.AsyncArchiveIndexView):
    pass


class BookSigningYearArchive(BookSigningConfig, generic.AsyncYearArchiveView):
    pass


class BookSigningMonthArchive(BookSigningConfig, generic.AsyncMonthArchiveView):
    pass


class BookSigningWeekArchive(BookSigningConfig, generic.AsyncWeekArchiveView):
    pass


class BookSigningDayArchive(BookSigningConfig, generic.AsyncDayArchiveView):
    pass


class BookSigningTodayArchive(BookSigningConfig, generic.AsyncTodayArchiveView):
    pass


class BookArchiveWithoutDateField(generic.AsyncArchiveIndexView):
    queryset = Book.objects.all()


class BookSigningDetail(BookSigningConfig, generic.AsyncDateDetailView):
    context_object_name = "book"
