from rest_framework import serializers
from product.models import Product, Variant, ProductImage, ProductVariant, ProductVariantPrice

from rest_framework import serializers

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['title', 'description', 'active']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['file_path']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['variant_title', 'variant']

class ProductVariantPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantPrice
        fields = ['product_variant_one', 'product_variant_two', 'product_variant_three', 'price', 'stock']

class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    product_variants = ProductVariantSerializer(many=True)
    product_variant_prices = ProductVariantPriceSerializer(many=True)

    class Meta:
        model = Product
        fields = ['title', 'sku', 'description', 'product_images', 'product_variants', 'product_variant_prices']

    def create(self, validated_data):
        product_images_data = validated_data.pop('product_images')
        product_variants_data = validated_data.pop('product_variants')
        product_variant_prices_data = validated_data.pop('product_variant_prices')

        product = Product.objects.create(**validated_data)

        for product_image_data in product_images_data:
            ProductImage.objects.create(product=product, **product_image_data)

        for product_variant_data in product_variants_data:
            variant = product_variant_data.pop('variant')
            product_variant = ProductVariant.objects.create(product=product, variant=variant, **product_variant_data)

        for product_variant_price_data in product_variant_prices_data:
            product_variant_one = product_variant_price_data.pop('product_variant_one', None)
            product_variant_two = product_variant_price_data.pop('product_variant_two', None)
            product_variant_three = product_variant_price_data.pop('product_variant_three', None)

            ProductVariantPrice.objects.create(
                product=product,
                product_variant_one=product_variant_one,
                product_variant_two=product_variant_two,
                product_variant_three=product_variant_three,
                **product_variant_price_data
            )

        return product
