from django.shortcuts import render, redirect
from .models import Transaction, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse


@login_required(login_url='/authentication/login')
def transactions(request):
    categories = Category.objects.all()
    transactions = Transaction.objects.filter(owner=request.user)
    paging = Paginator(transactions, per_page=5)
    page_number = request.GET.get('page')
    page = Paginator.get_page(paging,page_number)
    context = {
        'transactions': transactions,
        'page': page
    }
    return render(request, 'transactions/transactions.html', context)


def add_transaction(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'field_values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'transactions/add_transaction.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['transaction_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'transactions/add_transaction.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'transactions/add_transaction.html', context)

        transaction = Transaction.objects.create(owner=request.user,
                                                 amount=amount,
                                                 description=description,
                                                 category=category,
                                                 date=date)
        transaction.save()
        messages.success(request, 'Transaction saved')
    return redirect('transactions')


def edit_transaction(request, id):
    transaction = Transaction.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'transaction': transaction,
        'field_values': transaction,
        'categories': categories,
    }
    if request.method == 'GET':
        return render(request, 'transactions/edit_transaction.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['transaction_date']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'transactions/edit_transaction.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'transactions/edit_transaction.html', context)

        transaction.owner = request.user
        transaction.amount = amount
        transaction.description = description
        transaction.category = category
        transaction.date = date

        transaction.save()

        messages.success(request, 'Transaction updated')
        return redirect('transactions')

def delete_transaction(request, id):
    transaction = Transaction.objects.get(pk=id)
    transaction.delete()
    messages.success(request, 'Transaction deleted')
    
    return redirect('transactions')

def search_transaction(request):
    if request.method == 'POST':
        needle = json.loads(request.body).get('needle')
        transactions = (Transaction.objects.filter(amount__istartswith=needle, owner=request.user) |
                        Transaction.objects.filter(date__istartswith=needle, owner=request.user) |
                        Transaction.objects.filter(description__icontains=needle, owner=request.user) |
                        Transaction.objects.filter(category__icontains=needle, owner=request.user))
        
        data = transactions.values()
        return JsonResponse(list(data), safe=False)
