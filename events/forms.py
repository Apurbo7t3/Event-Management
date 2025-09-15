from django import forms
from events.models import Category,Event,Participant

class FormMixin:
    default_class = "border-2 border-gray-300- p-3 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-blue-500"
    def style(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_class,
                    'placeholder':f'Enter {field.label.title()}'
                })

            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':f'{self.default_class}',
                    'placeholder':f'Enter {field.label.title()}'
                })

            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    'class':f'{self.default_class}',
                    'placeholder':f'Enter {field.label.title()}'
                })

        
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':f'{self.default_class} space-y-2 h-5 w-5',
                    'placeholder':f'Enter {field.label.title()}'
                })
            elif isinstance(field.widget,forms.DateInput):
                field.widget.attrs.update({
                    'class':f'{self.default_class} space-x-2',
                    'type':'date'
                })
            elif isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':f'{self.default_class}',
                    'type':'time'
                })
            else:
                field.widget.attrs.update({
                    'class':f'{self.default_class}',
                })
            




class CategoryModelForm(FormMixin,forms.ModelForm):
    class Meta:
        model= Category
        fields=['name','description']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style()


class ParticipantModelForm(FormMixin,forms.ModelForm):
    class Meta:
        model= Participant
        fields=['name','email']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style()



class EventModelForm(FormMixin,forms.ModelForm):
    class Meta:
        model= Event
        fields= '__all__'
        widgets={
            'participants' : forms.CheckboxSelectMultiple(),
            'date': forms.SelectDateWidget(attrs={'date':'date'}),
            'time' : forms.TimeInput(attrs={'type':'time'}),
        }
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style()