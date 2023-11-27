from django.contrib import admin

from shop_reviews.models import ReplayToReview, ShopReviews


class ReplayToReviewInline(admin.TabularInline):
    """Включение ответов в админку отзывов"""
    model = ReplayToReview
    extra = 0


@admin.register(ShopReviews)
class ShopReviewsAdmin(admin.ModelAdmin):
    """Админка отзывов"""
    list_select_related = ('replay',)
    list_display = (
        'pk',
        'is_published',
        'delivery_speed_score',
        'price_score',
        'quality_score',
        'average_score',
        'author_name',
        'text',
        'replay',
        'pub_date',
        'author_email'
    )
    list_filter = ('pub_date', 'is_published')
    list_editable = (
        'is_published',
        'author_name',
        'text',
        'delivery_speed_score',
        'price_score',
        'quality_score',
        'author_email',
    )
    inlines = (
        ReplayToReviewInline,
    )
    empty_value_display = '-пусто-'
    search_fields = ('author_email', 'author_name')


@admin.register(ReplayToReview)
class ReplayToReviewAdmin(admin.ModelAdmin):
    """Админка ответов на отзывы"""
    list_display = (
        'pk',
        'text',
        'pub_date',
        'review_id'
    )
    list_filter = ('pub_date',)
    list_editable = (
        'text',
    )
    empty_value_display = '-пусто-'
    search_fields = ('text',)
