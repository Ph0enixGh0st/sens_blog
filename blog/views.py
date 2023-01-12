from django.shortcuts import render, get_object_or_404
from blog.models import Comment, Post, Tag
from django.db.models import Count, Prefetch


def serialize_post(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.first().title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts_count, # <<<<< PIECE A SHIT : len(Post.objects.filter(tags=tag)) /// tag.tags_count
    }


def index(request):

    #prefetch = Prefetch('tags', queryset=Tag.objects.annotate(posts_count=Count('posts')))
    #most_popular_posts = Post.objects.popular().select_related('author').prefetch_related(prefetch)[:5].fetch_with_comments_count()

    most_popular_posts = Post.objects.popular().select_related('author').prefetch_related(Prefetch('tags', Tag.objects.annotate(posts_count=Count('posts'))))[:5].fetch_with_comments_count()

    fresh_posts = Post.objects.order_by('published_at').annotate(comments_count=Count('comments', distinct=True)).select_related('author').prefetch_related(Prefetch('tags', Tag.objects.annotate(posts_count=Count('posts'))))
    most_fresh_posts = fresh_posts.order_by('-published_at')[:5].annotate(comments_count=Count('comments'))

    most_popular_tags = Tag.objects.popular()[:5]

    #most_popular_posts = Post.objects.popular().select_related('author')[:5].fetch_with_comments_count()

    #most_fresh_posts = Post.objects.annotate(comments_count=Count('comments')).prefetch_related('tags').select_related('author').order_by('-published_at')[:5]


    context = {
        'most_popular_posts': [serialize_post(post) for post in most_popular_posts[:5]],
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.annotate(comments_count=Count('post')).filter(post=post)
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    likes = post.likes.all()

    related_tags = post.tags.all()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': len(likes),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in related_tags],
    }

    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = Post.objects.popular().select_related('author')[:5].fetch_with_comments_count()

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = get_object_or_404(Tag, title=tag_title)

    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = Post.objects.popular().select_related('author')[:5].fetch_with_comments_count()

    related_posts = tag.posts.all()[:20]

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
