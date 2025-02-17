from django.contrib.flatpages.forms import FlatpageForm

from asgiref.sync import sync_to_async


class AsyncFlatPageForm(FlatpageForm):
    async def asave(self, commit=True):
        return await sync_to_async(self.save)(commit=commit)
