from django import forms
from .models import Brand,Category




# for brand
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'image']
        
        
# for category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description','image'] 
        
        
                     