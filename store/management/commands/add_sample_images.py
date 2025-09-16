from django.core.management.base import BaseCommand
from store.models import Movie
from django.db import models
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Add sample images to movies (creates placeholder images)'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample images to movies...')
        
        # Create a simple placeholder image using PIL if available
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create media directory if it doesn't exist
            media_dir = os.path.join(settings.MEDIA_ROOT, 'movie_images')
            os.makedirs(media_dir, exist_ok=True)
            
            # Get all movies without images (null or empty)
            movies_without_images = Movie.objects.filter(models.Q(image__isnull=True) | models.Q(image=''))
            
            for movie in movies_without_images:
                # Create a placeholder image
                img = Image.new('RGB', (300, 450), color='#2c3e50')
                draw = ImageDraw.Draw(img)
                
                # Try to use a default font, fallback to basic if not available
                try:
                    font = ImageFont.truetype("arial.ttf", 24)
                    title_font = ImageFont.truetype("arial.ttf", 20)
                except:
                    font = ImageFont.load_default()
                    title_font = ImageFont.load_default()
                
                # Add movie title
                title_lines = self.wrap_text(movie.title, 20)
                y_offset = 50
                for line in title_lines:
                    bbox = draw.textbbox((0, 0), line, font=title_font)
                    text_width = bbox[2] - bbox[0]
                    x = (300 - text_width) // 2
                    draw.text((x, y_offset), line, fill='white', font=title_font)
                    y_offset += 30
                
                # Add genre and year
                info_text = f"{movie.get_genre_display()} • {movie.release_year}"
                bbox = draw.textbbox((0, 0), info_text, font=font)
                text_width = bbox[2] - bbox[0]
                x = (300 - text_width) // 2
                draw.text((x, 200), info_text, fill='#ecf0f1', font=font)
                
                # Add price
                price_text = f"${movie.price}"
                bbox = draw.textbbox((0, 0), price_text, font=font)
                text_width = bbox[2] - bbox[0]
                x = (300 - text_width) // 2
                draw.text((x, 250), price_text, fill='#e74c3c', font=font)
                
                # Add "No Image Available" text
                no_image_text = "No Image Available"
                bbox = draw.textbbox((0, 0), no_image_text, font=font)
                text_width = bbox[2] - bbox[0]
                x = (300 - text_width) // 2
                draw.text((x, 350), no_image_text, fill='#95a5a6', font=font)
                
                # Save the image
                filename = f"{movie.id}_{movie.title.replace(' ', '_').replace(':', '').lower()}.png"
                image_path = os.path.join(media_dir, filename)
                img.save(image_path)
                
                # Update the movie with the image
                movie.image = f'movie_images/{filename}'
                movie.save()
                
                self.stdout.write(f'Created placeholder image for: {movie.title}')
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {movies_without_images.count()} placeholder images!')
            )
            
        except ImportError:
            self.stdout.write(
                self.style.WARNING('PIL/Pillow not available. Install it with: pip install Pillow')
            )
            self.stdout.write('You can manually add images through the admin panel.')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating images: {str(e)}')
            )

    def wrap_text(self, text, max_length):
        """Wrap text to fit within max_length characters per line"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            if len(' '.join(current_line + [word])) <= max_length:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
