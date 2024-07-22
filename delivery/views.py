from rest_framework import generics,viewsets,status
from rest_framework.response import Response
from .models import CatSuppliments, Category, CustomerDeliveryForm, CustomerStoreForm, Gouvernorat, NoticeStore, OrderItem, Rating, RatingStore, Store, Item, DeliveryPerson, Order, Publicity, SubCategory, Suppliment, TypeCategory
from .serializers import CategorySerializer, CategorySupplimentsSerializer, CustomerDeliveryFormSerializer, CustomerStoreFormSerializer, GouvernoratSerializer, NoticeStoreSerializer, OrderDeliverySerializer, OrderStatusSerializer, OrderedItemSerializer, RatingSerializer, RatingStoreSerializer, StoreSerializer, ItemSerializer, DeliveryPersonSerializer, OrderSerializer, PublicitySerializer, SubCategorySerializer, SupplimentSerializer, TypeCategorySerializer


class TypeCategoryList(generics.ListCreateAPIView):
    queryset = TypeCategory.objects.all()
    serializer_class = TypeCategorySerializer

class TypeCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TypeCategory.objects.all()
    serializer_class = TypeCategorySerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryList(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class SubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class StoreList(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class StoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class DeliveryPersonList(generics.ListCreateAPIView):
    queryset = DeliveryPerson.objects.all()
    serializer_class = DeliveryPersonSerializer

class DeliveryPersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryPerson.objects.all()
    serializer_class = DeliveryPersonSerializer


class PublicityList(generics.ListCreateAPIView):
    queryset = Publicity.objects.all()
    serializer_class = PublicitySerializer

class PublicityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publicity.objects.all()
    serializer_class = PublicitySerializer

class OrderCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        item_items = request.data.pop('items', [])
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        order = serializer.instance
        for item_item_data in item_items:
            item_id = item_item_data.get('item')
            quantity = item_item_data.get('quantity')
            suppliments_ids = item_item_data.get('suppliments', []) 
            if item_id and quantity:
                item = Item.objects.get(pk=item_id)
                store = item.store  
                order_item = OrderItem.objects.create(order=order, item=item, store=store, quantity=quantity)
                order_item.suppliments.add(*suppliments_ids)  

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderStatusUpdate(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    

class OrderDeliveryUpdate(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDeliverySerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    

class OrderedItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderedItemSerializer
    
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

class RatingListCreateView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        item = serializer.validated_data['item']
        
        # Check if the user has already rated the item
        existing_rating = Rating.objects.filter(user=user, item=item).first()
        if existing_rating:
            # If an existing rating is found, update it
            existing_rating.rating = serializer.validated_data['rating']
            existing_rating.save()
            return Response({"message": "Rating updated successfully"}, status=status.HTTP_200_OK)
        else:
            # If the user has not rated the item yet, create a new rating
            serializer.save(user=user)

class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]



class RatingStoreListCreateView(generics.ListCreateAPIView):
    queryset = RatingStore.objects.all()
    serializer_class = RatingStoreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        store = serializer.validated_data['store']
        
        # Check if the user has already rated the item
        existing_rating = RatingStore.objects.filter(user=user, store=store).first()
        if existing_rating:
            # If an existing rating is found, update it
            existing_rating.rating = serializer.validated_data['rating']
            existing_rating.save()
            return Response({"message": "Rating updated successfully"}, status=status.HTTP_200_OK)
        else:
            # If the user has not rated the item yet, create a new rating
            serializer.save(user=user)


class RatingStoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RatingStore.objects.all()
    serializer_class = RatingStoreSerializer
    permission_classes = [IsAuthenticated]



class NoticeStoreListCreateView(generics.ListCreateAPIView):
    queryset = NoticeStore.objects.all()
    serializer_class = NoticeStoreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoticeStoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NoticeStore.objects.all()
    serializer_class = NoticeStoreSerializer
    permission_classes = [IsAuthenticated]



class CategorySupplimentList(generics.ListCreateAPIView):
    queryset = CatSuppliments.objects.all()
    serializer_class = CategorySupplimentsSerializer

class CategorySupplimentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CatSuppliments.objects.all()
    serializer_class = CategorySupplimentsSerializer


class SupplimentList(generics.ListCreateAPIView):
    queryset = Suppliment.objects.all()
    serializer_class = SupplimentSerializer

class SupplimentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Suppliment.objects.all()
    serializer_class = SupplimentSerializer


class CustomerDeliveryFormList(generics.ListCreateAPIView):
    queryset = CustomerDeliveryForm.objects.all()
    serializer_class = CustomerDeliveryFormSerializer


class CustomerDeliveryFormDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerDeliveryForm.objects.all()
    serializer_class = CustomerDeliveryFormSerializer


class CustomerStoreFormList(generics.ListCreateAPIView):
    queryset = CustomerStoreForm.objects.all()
    serializer_class = CustomerStoreFormSerializer


class CustomerStoreFormDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerStoreForm.objects.all()
    serializer_class = CustomerStoreFormSerializer



class GouvernoratList(generics.ListCreateAPIView):
    queryset = Gouvernorat.objects.all()
    serializer_class = GouvernoratSerializer

class GouvernoratDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gouvernorat.objects.all()
    serializer_class = GouvernoratSerializer