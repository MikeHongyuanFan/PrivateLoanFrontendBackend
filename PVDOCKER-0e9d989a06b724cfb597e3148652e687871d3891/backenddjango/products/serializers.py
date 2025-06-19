from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model with null/blank handling for minimal data creation
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'applications', 'documents', 'borrowers', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            # Make most fields optional and allow null/blank values for minimal data creation
            'name': {'required': False, 'allow_null': True, 'allow_blank': True},
            'applications': {'required': False, 'allow_null': True},
            'documents': {'required': False, 'allow_null': True},
            'borrowers': {'required': False, 'allow_null': True},
        }