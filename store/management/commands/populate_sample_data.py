from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Movie, Review, Cart


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create sample movies
        movies_data = [
            {
                'title': 'The Dark Knight',
                'price': 12.99,
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'genre': 'action',
                'rating': 'PG-13',
                'director': 'Christopher Nolan',
                'cast': 'Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine',
                'release_year': 2008,
                'duration': 152,
                'language': 'English',
            },
            {
                'title': 'Inception',
                'price': 14.99,
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'genre': 'sci-fi',
                'rating': 'PG-13',
                'director': 'Christopher Nolan',
                'cast': 'Leonardo DiCaprio, Marion Cotillard, Tom Hardy, Joseph Gordon-Levitt',
                'release_year': 2010,
                'duration': 148,
                'language': 'English',
            },
            {
                'title': 'Pulp Fiction',
                'price': 11.99,
                'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
                'genre': 'crime',
                'rating': 'R',
                'director': 'Quentin Tarantino',
                'cast': 'John Travolta, Uma Thurman, Samuel L. Jackson, Bruce Willis',
                'release_year': 1994,
                'duration': 154,
                'language': 'English',
            },
            {
                'title': 'The Shawshank Redemption',
                'price': 13.99,
                'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'genre': 'drama',
                'rating': 'R',
                'director': 'Frank Darabont',
                'cast': 'Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler',
                'release_year': 1994,
                'duration': 142,
                'language': 'English',
            },
            {
                'title': 'Forrest Gump',
                'price': 12.99,
                'description': 'The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.',
                'genre': 'drama',
                'rating': 'PG-13',
                'director': 'Robert Zemeckis',
                'cast': 'Tom Hanks, Robin Wright, Gary Sinise, Sally Field',
                'release_year': 1994,
                'duration': 142,
                'language': 'English',
            },
            {
                'title': 'The Matrix',
                'price': 15.99,
                'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                'genre': 'sci-fi',
                'rating': 'R',
                'director': 'Lana Wachowski, Lilly Wachowski',
                'cast': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving',
                'release_year': 1999,
                'duration': 136,
                'language': 'English',
            },
            {
                'title': 'Goodfellas',
                'price': 11.99,
                'description': 'The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito.',
                'genre': 'crime',
                'rating': 'R',
                'director': 'Martin Scorsese',
                'cast': 'Robert De Niro, Ray Liotta, Joe Pesci, Lorraine Bracco',
                'release_year': 1990,
                'duration': 146,
                'language': 'English',
            },
            {
                'title': 'The Godfather',
                'price': 16.99,
                'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'genre': 'crime',
                'rating': 'R',
                'director': 'Francis Ford Coppola',
                'cast': 'Marlon Brando, Al Pacino, James Caan, Diane Keaton',
                'release_year': 1972,
                'duration': 175,
                'language': 'English',
            },
            {
                'title': 'Fight Club',
                'price': 13.99,
                'description': 'An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.',
                'genre': 'drama',
                'rating': 'R',
                'director': 'David Fincher',
                'cast': 'Brad Pitt, Edward Norton, Helena Bonham Carter, Meat Loaf',
                'release_year': 1999,
                'duration': 139,
                'language': 'English',
            },
            {
                'title': 'Interstellar',
                'price': 14.99,
                'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'genre': 'sci-fi',
                'rating': 'PG-13',
                'director': 'Christopher Nolan',
                'cast': 'Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine',
                'release_year': 2014,
                'duration': 169,
                'language': 'English',
            },
            {
                'title': 'The Lord of the Rings: The Fellowship of the Ring',
                'price': 17.99,
                'description': 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.',
                'genre': 'fantasy',
                'rating': 'PG-13',
                'director': 'Peter Jackson',
                'cast': 'Elijah Wood, Ian McKellen, Orlando Bloom, Viggo Mortensen',
                'release_year': 2001,
                'duration': 178,
                'language': 'English',
            },
            {
                'title': 'Avatar',
                'price': 15.99,
                'description': 'A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.',
                'genre': 'sci-fi',
                'rating': 'PG-13',
                'director': 'James Cameron',
                'cast': 'Sam Worthington, Zoe Saldana, Sigourney Weaver, Stephen Lang',
                'release_year': 2009,
                'duration': 162,
                'language': 'English',
            }
        ]

        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults=movie_data
            )
            if created:
                self.stdout.write(f'Created movie: {movie.title}')

        # Create a test user if it doesn't exist
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write('Created test user: testuser (password: testpass123)')
            
            # Create cart for test user
            Cart.objects.get_or_create(user=test_user)
            self.stdout.write('Created cart for test user')

        # Create some sample reviews
        sample_reviews = [
            {
                'movie_title': 'The Dark Knight',
                'rating': 5,
                'content': 'Absolutely brilliant! Heath Ledger\'s performance as the Joker is legendary. This is one of the best superhero movies ever made.'
            },
            {
                'movie_title': 'Inception',
                'rating': 4,
                'content': 'Mind-bending and visually stunning. Christopher Nolan delivers another masterpiece that keeps you thinking long after the credits roll.'
            },
            {
                'movie_title': 'Pulp Fiction',
                'rating': 5,
                'content': 'Quentin Tarantino at his finest. The non-linear storytelling and memorable characters make this a true classic.'
            },
            {
                'movie_title': 'The Shawshank Redemption',
                'rating': 5,
                'content': 'A beautiful story of hope and friendship. Tim Robbins and Morgan Freeman deliver outstanding performances.'
            },
            {
                'movie_title': 'The Matrix',
                'rating': 4,
                'content': 'Revolutionary for its time. The visual effects and philosophical themes make this a must-watch sci-fi film.'
            }
        ]

        for review_data in sample_reviews:
            try:
                movie = Movie.objects.get(title=review_data['movie_title'])
                review, created = Review.objects.get_or_create(
                    movie=movie,
                    user=test_user,
                    defaults={
                        'rating': review_data['rating'],
                        'content': review_data['content']
                    }
                )
                if created:
                    self.stdout.write(f'Created review for {movie.title}')
            except Movie.DoesNotExist:
                self.stdout.write(f'Movie not found: {review_data["movie_title"]}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
