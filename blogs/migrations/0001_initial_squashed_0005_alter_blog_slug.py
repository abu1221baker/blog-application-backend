import blogs.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('blogs', '0001_initial'), ('blogs', '0002_initial'), ('blogs', '0003_blog_views_count'), ('blogs', '0004_blog_viewed_by'), ('blogs', '0005_alter_blog_slug')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=300, unique=True)),
                ('hero_banner', models.ImageField(blank=True, null=True, upload_to=blogs.models.hero_banner_upload_path)),
                ('hero_title', models.CharField(blank=True, default='', max_length=255)),
                ('hero_subtitle', models.CharField(blank=True, default='', max_length=500)),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BlogContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('text', 'Text'), ('image', 'Image')], max_length=10)),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=blogs.models.content_image_upload_path)),
                ('order', models.PositiveIntegerField(default=0)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='blogs.blog')),
            ],
            options={
                'verbose_name': 'Blog Content Block',
                'verbose_name_plural': 'Blog Content Blocks',
                'ordering': ['order'],
            },
        ),
        migrations.AddIndex(
            model_name='blog',
            index=models.Index(fields=['-created_at'], name='blogs_blog_created_29c2e2_idx'),
        ),
        migrations.AddIndex(
            model_name='blog',
            index=models.Index(fields=['slug'], name='blogs_blog_slug_d0bba8_idx'),
        ),
        migrations.AddIndex(
            model_name='blog',
            index=models.Index(fields=['is_published', '-created_at'], name='blogs_blog_is_publ_7200fd_idx'),
        ),
        migrations.AddField(
            model_name='blog',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blog',
            name='viewed_by',
            field=models.ManyToManyField(blank=True, related_name='viewed_blogs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
