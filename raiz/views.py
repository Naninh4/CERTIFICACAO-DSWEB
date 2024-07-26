from django.shortcuts import get_object_or_404, redirect, render
from .models import * 
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    carrinho = CarrinhoDeCompra.objects.get(pk = 1 )
    request.session['carrinho_id'] = carrinho.pk
    produtos = Produto.objects.all()
    
    return render(request, "index.html", {'produtos': produtos})

@login_required
def add_item(request, pk):
    produto = Produto.objects.get(pk = pk)
    return render(request, 'add_carrinho.html', {'produto': produto})

@login_required
def addCar(request, pk):
    produto = get_object_or_404(Produto, id=pk)

    if produto.disponivel:
        carrinho_id = request.session.get('carrinho_id')

        if carrinho_id:
            carrinho = get_object_or_404(CarrinhoDeCompra, id=carrinho_id)
        else:
            carrinho = CarrinhoDeCompra.objects.create()
            request.session['carrinho_id'] = carrinho.pk 

        item, created = ItemDeCarrinho.objects.get_or_create(produto=produto)
        
        if not created:
            item.quantidade += 1
            item.save()
            carrinho.itens.add(item)

        else:
            item.quantidade = 1
            item.save()
            carrinho.itens.add(item)
            
        carrinho.save()
        request.session['carrinho_id'] = carrinho.pk

        return render(request, 'detalhes_carrinho.html', {'carrinho': carrinho}) 
    return redirect('index')