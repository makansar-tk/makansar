from django.forms import ModelForm, RadioSelect, Textarea, ValidationError
from main.models import Makanan, UserProfile
from account.models import User

class ProductEntryForm(ModelForm):
    class Meta:
        model = Makanan
        fields = ["category", "food_name", "price", "shop_name", "location", "food_desc", "rating_default"]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['nama', 'no_telp']

    # Validasi nama
    def clean_nama(self):
        nama = self.cleaned_data.get('nama')

        if not nama:
            raise ValidationError("Nama tidak boleh kosong!")
        
        if not all(x.isalpha() or x.isspace() for x in nama):
            raise ValidationError("Nama hanya boleh berisi huruf dan spasi.")
            
        return nama

    # Validasi nomor telepon
    def clean_no_telp(self):
        no_telp = self.cleaned_data.get('no_telp')

        if not no_telp:
            raise ValidationError("Nomor telepon tidak boleh kosong!")
        
        if not no_telp.isdigit():
            raise ValidationError("Nomor HP harus terdiri dari angka!")

        if len(no_telp) < 10 or len(no_telp) > 15:
            raise ValidationError("Nomor HP harus memiliki panjang antara 10-15 digit!")

        return no_telp

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'jenis_kelamin', 'email', 'alamat']
        widgets = {
            'jenis_kelamin': RadioSelect(choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')]),
            'alamat': Textarea(attrs={'rows': 3}),
        }

    def clean_alamat(self):
        alamat = self.cleaned_data.get('alamat')
        if not alamat:
            raise ValidationError("Alamat tidak boleh kosong!")
        return alamat

