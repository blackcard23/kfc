# Импорты
from django.db.models import Subquery, OuterRef, Sum
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DetailView, DeleteView
from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from main.forms import CategoryForm, DishForm
from main.models import Category, Dish, Basket, Order, OrderElement

# Главная страница
class MainPage(TemplateView):
    template_name = 'main/main.html'

# Список категорий и блюд
class Categoryy(ListView):
    template_name = 'main/menu.html'
    model = Category
    context_object_name = 'Categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        cate_id = self.request.GET.get('category', Category.objects.first().id)
        current_category = Category.objects.get(id=cate_id)
        foods = Dish.objects.filter(category_id=cate_id)
        context = super().get_context_data(**kwargs)
        context['foods'] = foods.annotate(count=Subquery(
            Basket.objects.filter(
                id=OuterRef('basket')
            ).values('count')
        ))
        context['current_category'] = current_category

        userid = self.request.user.id
        basket = Basket.objects.filter(users_id=userid)
        context['meals_in_basket'] = list(basket.values_list('dishes_id', flat=True))

        return context

# Управление корзиной
class BasketCountAdd(UpdateView):
    def post(self, request, *args, **kwargs):
        food_id = self.request.GET.get('dish')
        category_id = self.request.GET.get('category')
        basket = Basket.objects.filter(users=self.request.user, dishes_id=food_id).first()
        if basket is None:
            basket = Basket.objects.create(users_id=self.request.user.id, count=0, dishes_id=food_id)

        basket.count += 1
        basket.save()

        url = reverse('menu') + f'?category={category_id}'
        return redirect(url)

    def get(self, request, *args, **kwargs):
        raise Http404

class BasketCountMinus(UpdateView):
    def post(self, request, *args, **kwargs):
        food_id = self.request.GET.get('dish')
        category_id = self.request.GET.get('category')
        basket = Basket.objects.filter(users=self.request.user, dishes_id=food_id).first()
        if basket.count > 0:
            basket.count -= 1
            basket.save()
        if basket.count == 0:
            basket.delete()

        url = reverse('menu') + f'?category={category_id}'
        return redirect(url)

    def get(self, request, *args, **kwargs):
        raise Http404

class AddToCart(UpdateView):
    def post(self, request, *args, **kwargs):
        food_id = self.request.GET.get('dish')
        basket = Basket.objects.filter(users=request.user, dishes_id=food_id).first()
        if basket is None:
            basket = Basket.objects.create(users=request.user, count=1, dishes_id=food_id)
        else:
            basket.count += 1
            basket.save()
        return redirect('cart')

    def get(self, request, *args, **kwargs):
        raise Http404

class RemoveFromCart(UpdateView):
    def post(self, request, *args, **kwargs):
        food_id = self.request.GET.get('dish')
        basket = Basket.objects.filter(users=request.user, dishes_id=food_id).first()
        if basket:
            if basket.count > 1:
                basket.count -= 1
                basket.save()
            elif basket.count == 1:
                basket.delete()
        return redirect('cart')

    def get(self, request, *args, **kwargs):
        raise Http404

class CartView(TemplateView):
    template_name = 'main/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        basket_items = Basket.objects.filter(users_id=user_id).select_related('dishes')
        context['basket_items'] = basket_items
        return context

# Оформление заказа
class PlaceOrder(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        basket_items = Basket.objects.filter(users=user)
        if not basket_items:
            return redirect('cart')

        order = Order.objects.create(users=user)
        for item in basket_items:
            OrderElement.objects.create(orders=order, dishes=item.dishes, count=item.count)
        basket_items.delete()
        return redirect('order_success')

    def get(self, request, *args, **kwargs):
        raise Http404

class OrderSuccess(TemplateView):
    template_name = 'main/order_success.html'

class OrderHistoryView(ListView):
    model = Order
    template_name = 'main/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(users=self.request.user).order_by('-created_at')

# Управление категориями
class CategoryCreateView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'category_form.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        return render(request, 'category_form.html', {'form': form})

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'category_list.html', {'categories': categories})

class CategoryDetailView(View):
    def get(self, request, pk):
        category = Category.objects.filter(pk=pk).first()
        if not category:
            raise Http404("Категория не существует")
        return render(request, 'category_detail.html', {'category': category})

class CategoryUpdateView(View):
    def get(self, request, pk):
        category = Category.objects.filter(pk=pk).first()
        if not category:
            raise Http404("Категория не существует")
        form = CategoryForm(instance=category)
        return render(request, 'category_form.html', {'form': form})

    def post(self, request, pk):
        category = Category.objects.filter(pk=pk).first()
        if not category:
            raise Http404("Категория не существует")
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
        return render(request, 'category_form.html', {'form': form})

class CategoryDeleteView(View):
    def get(self, request, pk):
        category = Category.objects.filter(pk=pk).first()
        if not category:
            raise Http404("Категория не существует")
        return render(request, 'category_confirm_delete.html', {'category': category})

    def post(self, request, pk):
        category = Category.objects.filter(pk=pk).first()
        if not category:
            raise Http404("Категория не существует")
        category.delete()
        return redirect('category_list')

# Управление блюдами
class DishListView(ListView):
    model = Dish
    template_name = 'dish_list.html'

class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'dish_form.html'
    success_url = reverse_lazy('dish_list')

class DishDetailView(DetailView):
    model = Dish
    template_name = 'dish_detail.html'

class DishUpdateView(UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'dish_form.html'
    success_url = reverse_lazy('dish_list')

class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'dish_confirm_delete.html'
    success_url = reverse_lazy('dish_list')
