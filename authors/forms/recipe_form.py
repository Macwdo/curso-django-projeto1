from django import forms
from recipes.models import Recipe


class AuthorRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time',\
            'preparation_time_unit', 'servings', 'servings_unit',\
            'preparation_steps', 'cover'

        widgets = {
            'preparation_steps': forms.Textarea(attrs={'class': 'span-2'}),
            'cover': forms.FileInput(attrs={'class': 'span-2'}),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções','Porções'),
                    ('Pedaços','Pedaços'),
                    ('Pessoas','Pessoas'),

                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Horas','Horas'),
                    ('Minutos','Minutos')

                )
            )
        }
