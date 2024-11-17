from django import forms


class StudentLoginForm(forms.Form):
    student_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    std_passwd = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'type':'password', 'class':'form-control'}))
    log_failed = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'id':'std_log_stats'}), required=False)
    def __init__(self, *args, **kwargs):
        log_failed = kwargs.pop('log_failed', [])
        super(StudentLoginForm, self).__init__(*args, **kwargs)
        self.fields['log_failed'].widget=forms.TextInput(attrs={'value':log_failed, 'type':'hidden', 'id':'std_log_stats'})


class QuestionForm(forms.Form):
    CHOICES = [
            (1, "ch1"),
            (2, "ch2"),
            (3, "ch3"),
            (4, "ch4"),
    ]
    choice = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=False)
    chs = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'id':'chs_id'}), required=False)
    ans = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'id':'ans_id'}), required=False)
    qn_jump = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'id':'qn_id'}), required=False)

    def __init__(self, *args, **kwargs):
        choice = kwargs.pop('chs', [])
        ans = kwargs.pop('ans', [])
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['choice'].choices = choice
        self.fields['ans'].widget=forms.TextInput(attrs={'value':ans, 'type':'hidden', 'id':'ans_id'})


class AdminForm(forms.Form):
    admin_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    admin_passwd = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}))
    log_failed = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'id':'admin_log_stats'}), required=False)
    def __init__(self, *args, **kwargs):
        log_failed = kwargs.pop('log_failed', [])
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields['log_failed'].widget=forms.TextInput(attrs={'value':log_failed, 'type':'hidden', 'id':'admin_log_stats'})


class StdDbFileForm(forms.Form):
    # title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    file = forms.FileField(widget=forms.TextInput(attrs={'type': 'file', 'class': 'form-control'}))


class QnsDbFileForm(forms.Form):
    # title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    file = forms.FileField(widget=forms.TextInput(attrs={'type': 'file', 'class': 'form-control'}))
