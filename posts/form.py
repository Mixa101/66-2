from django import forms

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ["title", "content", "rate", "image"]


class PostForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()
    rate = forms.IntegerField()
    image = forms.ImageField(required=False)

    def clean_title(self):
        data = self.cleaned_data["title"]

        if "war" in data:
            raise forms.ValidationError("this is banned word!")

        return data

    # def clean(self) -> dict[str, Any]:
    #     cleaned_data = super().clean()

    #     if "war" in cleaned_data["title"]:
    #         raise forms.ValidationError("this is banned word")
    #     return cleaned_data
