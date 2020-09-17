from rest_framework import serializers
from core import models


def getShop(user):
    if user.is_owner:
        return models.Shop.objects.get(owner=user)

    if user.is_manager or user.is_salesman:
        created_by = user.created_by
        return models.Shop.objects.get(owner=created_by)


class ShopSerializer(serializers.ModelSerializer):
    """Serializer for shop"""

    class Meta:
        model = models.Shop
        fields = ("id", "name", "money", "owner")
        read_only_fields = ("id", "owner")


class AdminShopSerializer(serializers.ModelSerializer):
    """Admin(Superuser) Serializer for shop"""

    def __init__(self, *args, **kwargs):
        """Shows owner for superuser only"""

        super(AdminShopSerializer, self).__init__(*args, **kwargs)
        self.fields["owner"].queryset = models.User.objects.filter(
            is_owner=True)

    class Meta:
        model = models.Shop
        fields = ("id", "name", "money", "owner")
        read_only_fields = ("id",)

    def validate(self, data):
        owner = data["owner"]

        if not owner:
            raise serializers.ValidationError("No owner has been selected.")

        return data


class WarehouseSerializer(serializers.ModelSerializer):
    """Serializer for warehouse"""

    # if we like to show shop details
    # shop = ShopSerializer(read_only=True)

    class Meta:
        model = models.Warehouse
        fields = ("id", "name", "shop")
        read_only_fields = ("id", "shop")


class WarehouseProductsSerializer(serializers.ModelSerializer):
    """Serializer for warehouse products"""

    class Meta:
        model = models.WareHouseProducts
        fields = ("id", "warehouse", "product", "quantity", "shop")
        read_only_fields = ("id", "shop")


class SalesmanSerializer(serializers.Serializer):
    """Serializer for salesman list"""

    id = serializers.IntegerField()
    username = serializers.CharField()
    mobile = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    class Meta:
        model = models.Product
        fields = ("id", "name", "buying_price",
                  "selling_price", "stock", "shop")
        read_only_fields = ("id", "shop")


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer"""

    class Meta:
        model = models.Customer
        fields = ("id", "name", "contact", "shop")
        read_only_fields = ("id", "shop")


class VendorSerializer(serializers.ModelSerializer):
    """Serializer for Customer"""

    class Meta:
        model = models.Vendor
        fields = ("id", "name", "contact", "shop")
        read_only_fields = ("id", "shop")


class CustomerTrasnscationSerializer(serializers.ModelSerializer):
    """Serializer for customer product transaction"""

    def __init__(self, *args, **kwargs):
        """Filter customers by shop"""

        super(CustomerTrasnscationSerializer, self).__init__(*args, **kwargs)

        own_shop = getShop(user=self.context["request"].user)
        self.fields["customer"].queryset = models.Customer.objects.filter(
            shop=own_shop)

    class Meta:
        model = models.CustomerTrasnscation
        fields = ("id", "order_time", "shop", "customer")
        read_only_fields = ("id", "shop")


class CustomerOrderedItemsSerializer(serializers.ModelSerializer):
    """Serializer for ordered products"""

    def validate(self, data):
        product = data["product"]
        quantity = data["quantity"]
        order = data["order"]
        # bill = data['bill']

        if product is None:
            raise serializers.ValidationError("No product has been selected.")
        if order is None:
            raise serializers.ValidationError("No order has been selected.")

        exists = models.CustomerOrderedItems.objects.filter(
            product=product, order=order
        )

        # print(models.Product.objects.get(pk=product.id).price == product.price)
        data["bill"] = product.selling_price * quantity

        if exists:
            raise serializers.ValidationError("Duplicate entires not allowed.")

        stock = product.stock - quantity

        if stock < 0:
            raise serializers.ValidationError("Insufficient stock.")

        product.stock = stock
        product.save()

        return data

    def __init__(self, *args, **kwargs):
        """Filter customers by shop"""

        super(CustomerOrderedItemsSerializer, self).__init__(*args, **kwargs)

        own_shop = getShop(user=self.context["request"].user)
        self.fields["product"].queryset = models.Product.objects.filter(
            shop=own_shop)
        self.fields["order"].queryset = models.CustomerTrasnscation.objects.filter(
            shop=own_shop
        )

    # product = ProductSerializer()

    class Meta:
        model = models.CustomerOrderedItems
        fields = ("id", "order", "shop", "product", "quantity", "bill")
        read_only_fields = ("id", "shop", "bill")


class CustomerTrasnscationProductDetailSerializer(CustomerOrderedItemsSerializer):
    product = ProductSerializer()


class CustomerTrasnscationBillSerializer(serializers.ModelSerializer):
    """Serializer for Customer transaction bill"""

    def __init__(self, *args, **kwargs):
        """Filter customers by shop"""

        super(CustomerTrasnscationBillSerializer,
              self).__init__(*args, **kwargs)

        own_shop = getShop(self.context["request"].user)
        self.fields["order"].queryset = models.CustomerTrasnscation.objects.filter(
            shop=own_shop
        )

    def validate(self, data):
        order = data["order"]
        total_bill = 0

        orders = models.CustomerOrderedItems.objects.filter(order=order)

        for i in orders:
            total_bill += i.bill

        data["bill"] = total_bill
        return data

    class Meta:
        model = models.CustomerTrasnscationBill
        fields = ("id", "shop", "order", "bill", "paid")
        read_only_fields = ("id", "shop", "bill")


class VendorTrasnscationSerializer(serializers.ModelSerializer):
    """Serializer for vendor product transaction"""

    def __init__(self, *args, **kwargs):
        """Filter vendors by shop"""

        super(VendorTrasnscationSerializer, self).__init__(*args, **kwargs)

        own_shop = getShop(self.context["request"].user)
        self.fields["vendor"].queryset = models.Vendor.objects.filter(
            shop=own_shop)

    class Meta:
        model = models.VendorTrasnscation
        fields = ("id", "order_time", "shop", "vendor")
        read_only_fields = ("id", "shop")


class VendorOrderedItemsSerializer(serializers.ModelSerializer):
    """Serializer for ordered products"""

    def validate(self, data):
        product = data["product"]
        quantity = data["quantity"]
        order = data["order"]
        warehouse = data["delivery_warehouse"]
        # bill = data['bill']

        if product is None:
            raise serializers.ValidationError("No product has been selected.")
        if order is None:
            raise serializers.ValidationError("No order has been selected.")
        if warehouse is None:
            raise serializers.ValidationError(
                "No warehouse has been selected.")

        data["bill"] = product.buying_price * quantity

        stock = product.stock + quantity

        product.stock = stock
        product.save()

        return data

    def __init__(self, *args, **kwargs):
        """Filter vendors by shop"""

        super(VendorOrderedItemsSerializer, self).__init__(*args, **kwargs)

        own_shop = getShop(self.context["request"].user)
        self.fields["product"].queryset = models.Product.objects.filter(
            shop=own_shop)
        self.fields["order"].queryset = models.VendorTrasnscation.objects.filter(
            shop=own_shop
        )
        self.fields["delivery_warehouse"].queryset = models.Warehouse.objects.filter(
            shop=own_shop
        )

    # product = ProductSerializer()

    class Meta:
        model = models.VendorOrderedItems
        fields = (
            "id",
            "order",
            "shop",
            "product",
            "delivery_warehouse",
            "quantity",
            "bill",
        )
        read_only_fields = ("id", "shop", "bill")


class VendorTrasnscationProductDetailSerializer(VendorOrderedItemsSerializer):
    product = ProductSerializer()


class VendorTrasnscationBillSerializer(serializers.ModelSerializer):
    """Serializer for vendor transaction bill"""

    def __init__(self, *args, **kwargs):
        """Filter vendors by shop"""

        super(VendorTrasnscationBillSerializer, self).__init__(*args, **kwargs)

        own_shop = getShop(self.context["request"].user)
        self.fields["order"].queryset = models.VendorTrasnscation.objects.filter(
            shop=own_shop
        )

    def validate(self, data):
        order = data["order"]

        previos_paid = models.VendorTrasnscationBill.objects.get(
            id=self.instance.id
        ).paid
        new_paid = data["paid"]

        shop = self.instance.shop
        total_bill = 0

        orders = models.VendorOrderedItems.objects.filter(order=order)

        for i in orders:
            total_bill += i.bill

        if new_paid > shop.money:
            raise serializers.ValidationError("Not enough money.")

        data["bill"] = total_bill
        data["due"] = total_bill - previos_paid - new_paid

        shop.money -= new_paid
        shop.save()

        return data

    class Meta:
        model = models.VendorTrasnscationBill
        fields = ("id", "shop", "order", "bill", "paid", "due")
        read_only_fields = ("id", "shop", "bill", "due")


class MoveProductSerializer(serializers.ModelSerializer):
    """Serializer for moving product shop to warehouse"""

    def __init__(self, *args, **kwargs):
        super(MoveProductSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        try:
            warehouse = data["warehouse"]
            product = data["product"]
            quantity = data["quantity"]
            move = data["move"]

            if not move:
                raise serializers.ValidationError("Please fulfill all fields.")
        except:
            raise serializers.ValidationError("Please fulfill all fields.")

        warehouse_stock = models.WareHouseProducts.objects.filter(
            warehouse=warehouse, product=product
        )

        shop_product = models.Product.objects.get(id=product.pk)

        if move == "S2W":
            if shop_product.stock < quantity:
                raise serializers.ValidationError(
                    "Shop does not have this amount of product."
                )

            if warehouse_stock:
                warehouse_stock = warehouse_stock[0]

                warehouse_stock.quantity += quantity
                shop_product.stock -= quantity

                warehouse_stock.save()
                shop_product.save()
            else:
                own_shop = getShop(self.context["request"].user)
                models.WareHouseProducts.objects.create(
                    warehouse=warehouse,
                    product=product,
                    quantity=quantity,
                    shop=own_shop,
                )

                shop_product.stock -= quantity
                shop_product.save()
        elif move == "W2S":

            if warehouse_stock:
                warehouse_stock = warehouse_stock[0]

                if warehouse_stock.quantity < quantity:
                    raise serializers.ValidationError(
                        "Warehouse does not have this amount of product."
                    )

                warehouse_stock.quantity -= quantity
                shop_product.stock += quantity

                warehouse_stock.save()
                shop_product.save()
            else:
                models.WareHouseProducts.objects.create(
                    warehouse=warehouse, product=product, quantity=0
                )
                raise serializers.ValidationError(
                    "Warehouse does not have this amount of product."
                )

        return data

    def __init__(self, *args, **kwargs):
        """Filter by shop"""

        super(MoveProductSerializer, self).__init__(*args, **kwargs)

        own_shop = getShop(self.context["request"].user)
        self.fields["warehouse"].queryset = models.Warehouse.objects.filter(
            shop=own_shop
        )
        self.fields["product"].queryset = models.Product.objects.filter(
            shop=own_shop)

    class Meta:
        model = models.MoveProduct
        fields = ("id", "shop", "warehouse", "product", "quantity", "move")
        read_only_fields = ("id", "shop")
