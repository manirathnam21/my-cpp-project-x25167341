from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category

class Command(BaseCommand):
    help = 'Creates a superuser and initial categories if they don\'t exist'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
        
        # Create initial categories if they don't exist
        categories = [
            {'name': 'Clothing', 'description': 'Sustainable clothing items including shirts, pants, dresses, and more.'},
            {'name': 'Accessories', 'description': 'Eco-friendly accessories such as bags, jewelry, and scarves.'},
            {'name': 'Footwear', 'description': 'Environmentally conscious shoes, sandals, and boots.'}
        ]
        
        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
        
        self.stdout.write(self.style.SUCCESS('Initial categories created successfully!'))