from django.urls import path

from main.views import *

urlpatterns = [
    path('menu/', Categoryy.as_view(), name='menu'),
    path('', MainPage.as_view(), name='main'),  # Главная страница

    # URL-ы для корзины
    path('cart/add_food/', BasketCountAdd.as_view(), name='cart_add'),  # Добавить еду в корзину
    path('cart/minus_food/', BasketCountMinus.as_view(), name='cart_minus'),  # Уменьшить количество еды в корзине
    path('add_to_cart/', AddToCart.as_view(), name='add_to_cart'),  # Добавить в корзину
    path('remove_from_cart/', RemoveFromCart.as_view(), name='remove_from_cart'),  # Удалить из корзины
    path('cart/', CartView.as_view(), name='cart'),  # Просмотр корзины

    # URL-ы для заказов
    path('place_order/', PlaceOrder.as_view(), name='place_order'),  # Оформить заказ
    path('order_success/', OrderSuccess.as_view(), name='order_success'),  # Успех заказа
    path('order_history/', OrderHistoryView.as_view(), name='order_history'),  # История заказов

    # URL-ы для категорий
    path('categories/', CategoryListView.as_view(), name='category_list'),  # Список категорий
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),  # Создать категорию
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),  # Детали категории
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),  # Изменить категорию
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),  # Удалить категорию

    # URL-ы для блюд
    path('dishes/', DishListView.as_view(), name='dish_list'),  # Список блюд
    path('dishes/create/', DishCreateView.as_view(), name='dish_create'),  # Создать блюдо
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish_detail'),  # Детали блюда
    path('dishes/<int:pk>/update/', DishUpdateView.as_view(), name='dish_update'),  # Изменить блюдо
    path('dishes/<int:pk>/delete/', DishDeleteView.as_view(), name='dish_delete'),  # Удалить блюдо
]
