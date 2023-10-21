from rest_framework import serializers

from shop_reviews.models import ReplayToReview, ShopReviews


class ReplayToReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReplayToReview
        fields = (
            'text',
            'pub_date',
            'name'
        )


class ReplayToReviewAdminSerializer(serializers.ModelSerializer):
    review_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReplayToReview
        fields = (
            'pk',
            'text',
            'pub_date',
            'name',
            'review_id'
        )
        read_only_fields = ('review_id', 'pk')


class ShopReviewsSerializer(serializers.ModelSerializer):
    replay = ReplayToReviewSerializer(read_only=True)

    class Meta:
        model = ShopReviews
        fields = (
            'pk',
            'text',
            'pub_date',
            'author_name',
            'author_email',
            'average_score',
            'delivery_speed_score',
            'quality_score',
            'price_score',
            'replay'
        )
        read_only_fields = ('replay', 'pk', 'pub_date')

    def get_average_score(self, obj):
        return obj.average_score()


class ShopReviewsAdminSerializer(serializers.ModelSerializer):
    replay = ReplayToReviewSerializer(read_only=True)

    class Meta:
        model = ShopReviews
        fields = (
            'pk',
            'text',
            'pub_date',
            'author_name',
            'author_email',
            'average_score',
            'delivery_speed_score',
            'quality_score',
            'price_score',
            'replay',
            'is_published'
        )
        read_only_fields = ('replay', 'pk', 'pub_date')

    def get_average_score(self, obj):
        return obj.average_score()
