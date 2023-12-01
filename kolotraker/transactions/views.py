from django.shortcuts import render

# Create your views here.
def transactions(request):
    return render(request, 'transactions/transactions.html')

def add_transaction(request):
    return render(request, 'transactions/add_transaction.html')