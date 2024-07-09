import re

from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.db.models import Q

from .models import Price, Registrator, TeamMember
from .forms import CompaniesSortForm, ContactForm
from .tasks import send_join_team_mail


SORT_FIELD_NAMES = {
    'CN': 'registrator__name',
    'CI': 'registrator__city',
    'RE': 'price_reg',
    'PR': 'price_prolong',
    'PE': 'price_change',

}


def is_english(text):
    return re.match(r'^[a-zA-Z0-9\s]+$', text) is not None


def extract_name_from_quotes(name):
    match = re.search(r'«(.*?)»', name)
    return match.group(1) if match else None


def registrator_list(request):
    if request.method == "POST":
        form = CompaniesSortForm(request.POST)
        if form.is_valid():
            sort_by = (form.cleaned_data['reverse_order']
                       + SORT_FIELD_NAMES.get(
                        form.cleaned_data['sort_by'], 'name'))
            search = form.cleaned_data['search']

    else:
        form = CompaniesSortForm()
        sort_by = 'id'
        search = ''

    if search:
        if is_english(search):
            search_by_name_only = False
            companies = Price.objects.filter(
                Q(registrator__website__icontains=search)
            )
        else:
            search_by_name_only = True
            companies = Price.objects.filter(
                Q(registrator__name__icontains=search)
            )

    else:
        companies = Price.objects.filter()

    companies = companies.order_by('registrator_id', '-parse__id', '-created_at').distinct('registrator_id')

    sort_by_lst = []
    if 'price_reg' in sort_by:
        sort_by_lst = ['-reg_status', sort_by]
    elif 'price_prolong' in sort_by:
        sort_by_lst = ['-prolong_status', sort_by]
    elif 'price_change' in sort_by:
        sort_by_lst = ['-change_status', sort_by]
    else:
        sort_by_lst = [sort_by]

    companies = Price.objects.filter(id__in=companies).order_by(*sort_by_lst)

    if search and search_by_name_only:
        sorted_companies_lambda = sorted(
            filter(lambda x: extract_name_from_quotes(x.registrator.name).lower().startswith(search.lower()),
                   companies),
            key=lambda x: extract_name_from_quotes(x.registrator.name)
        )
    else:
        sorted_companies_lambda = companies

    return render(request, 'registrator-list.html', {'companies': sorted_companies_lambda, 'form': form})


def registrator_details(request, id):
    try:
        registrator = Registrator.objects.get(id=id)
        prices = Price.objects.filter(registrator=registrator)
    except Price.DoesNotExist:
        return HttpResponseNotFound(f"Компания с идентификатором {id} в базе не найдена.")
    return render(request, 'registrator-details.html', {'prices': prices, 'registrator': registrator})


def about(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            contact = request.POST.get("contact")
            speciality = request.POST.get("speciality")
            message = request.POST.get("message")
            send_join_team_mail.delay(name, contact, speciality, message)
            return HttpResponseRedirect('/')
    else:
        form = ContactForm()

    team_members = TeamMember.objects.all()

    if request.path == "/about-us/":
        template_name = 'about-us.html'
    elif request.path == "/project/":
        template_name = 'project.html'
    else:
        template_name = 'default.html'

    return render(request, template_name, {'contact_form': form, 'team_members': team_members})



def project_view(request):
    return render(request, 'project.html')
