
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from feed.models import Equipamento, Status


class ConfirmarAtividadeForm(forms.Form):
    justificativa_attrs = {
        'class': 'materialize-textarea',
    }
    concluido_attrs = {
        "onchange": "activateJustificativaTextArea(this)",
    }

    justificativa = forms.CharField(widget=forms.Textarea(attrs=justificativa_attrs), required=False)
    concluido = forms.BooleanField(widget=forms.CheckboxInput(attrs=concluido_attrs), required=False)

    def clean(self):
        cleaned_data = super(ConfirmarAtividadeForm, self).clean()
        justificativa = cleaned_data.get('justificativa')
        concluido = cleaned_data.get('concluido')

        if not justificativa and not concluido:
            raise ValidationError({'justificativa': _('Caso o projeto não tenha sido concluido, digite uma justificativa.')})


class CadastrarEquipamentoForm(forms.ModelForm):
    class Meta:
        descricao_attrs = {
            'class': 'materialize-textarea',
        }
        model = Equipamento
        fields = '__all__'
        widgets = {
            'descricao' : forms.Textarea(attrs=descricao_attrs)
        }


class AddStatusForm(forms.Form):
    descricao_attrs = {
        'class': 'materialize-textarea',
    }
    descricao = forms.CharField(widget=forms.Textarea(attrs=descricao_attrs))


