from django import forms
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "image", "caption")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "shadow border rounded w-full py-2 px-3 text-gray-700",
                    "placeholder": "Enter post title",
                }
            ),
            "caption": forms.Textarea(
                attrs={
                    "class": "shadow border rounded w-full py-2 px-3 text-gray-700",
                    "placeholder": "Write a caption...",
                    "rows": 3,
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")

        return title

    def clean_caption(self):
        caption = self.cleaned_data.get("caption", "")

        if caption and len(caption) > 1000:
            raise forms.ValidationError("Caption cannot exceed 1000 characters.")

        return caption


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "class": "shadow border rounded w-full py-2 px-3 text-gray-700",
                    "placeholder": "Add a comment...",
                }
            )
        }

    def clean_body(self):
        body = self.cleaned_data.get("body")

        if not body.strip():
            raise forms.ValidationError("Comment cannot be empty.")

        return body
