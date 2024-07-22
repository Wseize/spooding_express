from django.urls import path,include
from .views import (
    CategoryDetail,
    CategoryList,
    CategorySupplimentDetail,
    CategorySupplimentList,
    CustomerDeliveryFormDetail,
    CustomerDeliveryFormList,
    CustomerStoreFormDetail,
    CustomerStoreFormList,
    DeliveryPersonDetail,
    DeliveryPersonList,
    GouvernoratDetail,
    GouvernoratList,
    ItemDetail,
    ItemList,
    NoticeStoreDetailView,
    NoticeStoreListCreateView,
    OrderCreate,
    OrderDeliveryUpdate,
    OrderDetail,
    OrderStatusUpdate,
    OrderedItemViewSet,
    PublicityDetail,
    PublicityList,
    RatingDetailView,
    RatingListCreateView,
    RatingStoreDetailView,
    RatingStoreListCreateView,
    StoreDetail,
    StoreList,
    SubCategoryDetail,
    SubCategoryList,
    SupplimentDetail,
    SupplimentList,
    TypeCategoryDetail,
    TypeCategoryList,
)

urlpatterns = [

    path('typecategories/', TypeCategoryList.as_view(), name='typecategory-list'),
    path('typecategories/<int:pk>/', TypeCategoryDetail.as_view(), name='typecategory-detail'),

    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),

    path('sub-categories/', SubCategoryList.as_view(), name='sub-category-list'),
    path('sub-categories/<int:pk>/', SubCategoryDetail.as_view(), name='sub-category-detail'),

    path('gouvernorat/', GouvernoratList.as_view(), name='gouvernorat-list'),
    path('gouvernorat/<int:pk>/', GouvernoratDetail.as_view(), name='gouvernorat-detail'),

    path('stores/', StoreList.as_view(), name='store-list'),
    path('stores/<int:pk>/', StoreDetail.as_view(), name='store-detail'),

    path('items/', ItemList.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),

    path('delivery_persons/', DeliveryPersonList.as_view(), name='delivery-person-list'),
    path('delivery_persons/<int:pk>/', DeliveryPersonDetail.as_view(), name='delivery-person-detail'),

    path('orders/', OrderCreate.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', OrderStatusUpdate.as_view(), name='order-status-update'),
    path('orders/<int:pk>/delivery_person/', OrderDeliveryUpdate.as_view(), name='order-delivery-update'),

    path('ordered-products/', OrderedItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='orderedproduct-list'),
    path('ordered-products/<int:pk>/', OrderedItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='orderedproduct-detail'),

    path('publicities/', PublicityList.as_view(), name='publicity-list'),
    path('publicities/<int:pk>/', PublicityDetail.as_view(), name='publicity-detail'),

    path('ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
    path('ratings/<int:pk>/', RatingDetailView.as_view(), name='rating-detail'),

    path('ratingsStore/', RatingStoreListCreateView.as_view(), name='rating-store-list-create'),
    path('ratingsStore/<int:pk>/', RatingStoreDetailView.as_view(), name='rating-store-detail'),

    path('category-suppliments/', CategorySupplimentList.as_view(), name='category-suppliment-list'),
    path('category-suppliments/<int:pk>/', CategorySupplimentDetail.as_view(), name='category-suppliment-detail'),

    path('suppliments/', SupplimentList.as_view(), name='suppliment-list'),
    path('suppliments/<int:pk>/', SupplimentDetail.as_view(), name='suppliment-detail'),

    path('notices/', NoticeStoreListCreateView.as_view(), name='notice-list-create'),
    path('notices/<int:pk>/', NoticeStoreDetailView.as_view(), name='notice-detail'),

    path('deliveryForm/', CustomerDeliveryFormList.as_view(), name='deliveryForm-list'),
    path('deliveryForm/<int:pk>/', CustomerDeliveryFormDetail.as_view(), name='deliveryForm-detail'),

    path('storeForm/', CustomerStoreFormList.as_view(), name='storeForm-list'),
    path('storeForm/<int:pk>/', CustomerStoreFormDetail.as_view(), name='storeForm-detail'),
]
