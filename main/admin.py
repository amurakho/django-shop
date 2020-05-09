from django.contrib import admin
from django.contrib import messages
from django import forms

from main import models

admin.site.register(models.Promotion)


class ImageInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # Check if it is at least one image
        # Check delete main without another
        image_counter = 0
        is_all_delete = True
        for form in self.forms:
            try:
                if form.cleaned_data:
                    image_counter += 1
                if not form.cleaned_data.get('DELETE', True):
                    is_all_delete = False
            except AttributeError:
                pass
        if image_counter < 1:
            raise forms.ValidationError('Нужно ввести хотя бы одно изображение')
        if is_all_delete:
            raise forms.ValidationError('Ты пытался удалить все изображения. '
                                        'Загрузи заранее новое, которое будет главным. '
                                        'Изменения не сохранились')


class ImageInLine(admin.StackedInline):
    formset = ImageInlineFormset
    model = models.Image


class ProductAdmin(admin.ModelAdmin):
    inlines = (ImageInLine,)
    list_display = ('name', 'price', 'art', 'in_stock', 'promotion', 'category')

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            formset.is_valid()
            instances = formset.save(commit=False)

            # Check more then one is_main=True
            # i need "False". And "None == False -> False" but "not None -> True"
            was_main = [info.get('is_main') for info in formset.cleaned_data
                        if info.get('is_main') or info.get('is_main') == False]
            if any(was_main) and sum(was_main) != 1:
                messages.add_message(request, messages.WARNING,
                                     'Ты указал несколько изображений как главные(is_main=True).'
                                     ' Я оставил главным - первое изображение, а остальным выключил этот параметр')

            # Check save without is_main=True
            # if was some not empty inline form and all of them are is_main=False
            if was_main and not any(was_main):
                # get first inline form and make it main
                instances[0].is_main = True
                messages.add_message(request, messages.WARNING,
                                     'Ты не объявил ни одно изображение как главное(is_main=True),'
                                     'Я сделал главным первое изображение в списке')

            # Check delete main with another
            if formset.deleted_forms:
                for obj in formset.deleted_objects:
                    if obj.is_main:
                        messages.add_message(request, messages.WARNING,
                                             'Ты попытался удалить главное изображение. '
                                             'Я уставновил главным другое изображение')

            self.save_formset(request, form, formset, change=change)


admin.site.register(models.Product, ProductAdmin)

admin.site.register(models.Review)

admin.site.register(models.Category)

admin.site.register(models.Bucket)

admin.site.register(models.ProductInBucket)

admin.site.register(models.Order)