from django import forms

from main import models as product_models


class OrderCreationForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control order-input'}), label='Имя')
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control order-input'}), label='Фамилия')
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control order-input'}), label='Город')
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control order-input'}), label='Телефон')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control order-input'}), label='Email',
                             required=False)
    delivery_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control order-input',
                                                                 'id': 'delivery-choice',
                                                                 'autocomplete': 'off'}),
                                      label='Доставка', choices=product_models.DELIVERY_CHOICES)
    post_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control order-input'}),
                                    label='Номер отделения')
    index = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control order-input'}), label='Индекс',
                            required=False)
    street = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control order-input'}), label='Улица',
                             required=False)
    house_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control order-input'}),
                                   label='Номер дома', required=False)
    # flat_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control order-input'}),
    #                                  label='Номер квартиры', required=False)

    class Meta:
        model = product_models.Order
        exclude = ('bucket', )