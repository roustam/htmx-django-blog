import random
from datetime import datetime

# myblog/posts/management/commands/seed_posts.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from posts.models import Post, Tag


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10)

    def handle(self, *args, **options):
        count = options["count"]
        self.stdout.write(f"Seeding {count} posts...")
        test_tags = Tag.objects.last()

        sample_text = '''Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar. The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli, but the Little Blind Text didn’t listen. She packed her seven versalia, put her initial into the belt and made herself on the way. When she reached the first hills of the Italic Mountains, she had a last view back on the skyline of her hometown Bookmarksgrove, the headline of Alphabet Village and the subline of her own road, the Line Lane. Pityful a rethoric question ran over her cheek, then'''

        sample_text_list = sample_text.split(' ')

        for post in range(1, count):
            
            random.shuffle(sample_text_list)
            post_title = f"{" ".join(sample_text_list[:3])} {random.randint(10,99)}"
            post_slug = slugify(post_title)
            new_post = Post(
                id=post,
                post_title=post_title,
                post_slug=post_slug,
                body_html=" ".join(sample_text_list),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                )
            new_post.save()
            new_post.tags.set([test_tags])
            print(post, new_post)

