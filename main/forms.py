from django import forms

from main import models


class SearchForm(forms.Form):
    value = forms.CharField(max_length=100, help_text='Write some request')


class ReviewForm(forms.ModelForm):

    RATING_CHOICE = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    )

    order_number = forms.IntegerField(widget=
                                      forms.NumberInput(attrs={'class': 'border-dark form-control com-order',
                                                              'placeholder': 'Введите номер заказа'}),
                                      error_messages={'required': 'Вы должны ввести номер заказа'})
    author = forms.CharField(widget=
                             forms.TextInput(attrs={'class': 'border-dark form-control com-author',
                                                  'placeholder': 'Введите имя и фамилию'}),
                             error_messages={'required': 'Вы должны ввести Имя и/или Фамилию'})
    rating = forms.ChoiceField(widget=
                               forms.Select(attrs={'class': 'border-dark form-control com-rating'}),
                               choices=RATING_CHOICE,
                               )
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'border-dark form-control com-text',
                                                      'placeholder': 'Сообщение'}),
                           error_messages={'required': 'Вы должны ввести сообщение'})

    class Meta:
        model = models.Review
        exclude = ('date', 'product')

    def clean(self):
        order_id = self.cleaned_data['order_number']
        order = models.Order.objects.filter(id=order_id)
        if not order:
            raise forms.ValidationError('Вы ввели неправильный номер заказа')
