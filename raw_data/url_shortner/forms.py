from django import forms

from models import UrlShortner


class URLShortnerForm(forms.Form):
    """

    """
    long_url = forms.CharField(required=True, label="Long URL")
    short_url = forms.CharField(required=False, label="Custom URL")

    def clean_long_url(self):
        """

        :return:
        """
        long_url = self.cleaned_data.get('long_url', "").strip()

        if long_url:
            try:
                long_url_object = UrlShortner.objects.get(long_url=long_url)
                if long_url_object:
                    raise forms.ValidationError('Long URL Exists. Short URL: %s' % long_url_object.short_url)
            except UrlShortner.DoesNotExist:
                print ("Long URL Not available")
            return long_url

    def clean_short_url(self):
        """

        :return:
        """
        short_url = self.cleaned_data.get('short_url', "").strip()
        if short_url:
            try:
                short_url_object = UrlShortner.objects.get(short_url=short_url)
                if short_url_object:
                    raise forms.ValidationError('Custom Short URL Exists. Long URL: %s' %
                                                short_url_object.long_url)
            except UrlShortner.DoesNotExist:
                print ("No shortner url")
            return short_url