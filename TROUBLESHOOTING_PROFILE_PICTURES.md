# Troubleshooting Profile Pictures - 404 Error

## Problem
Getting a 404 error when trying to view profile pictures:
```
"GET /media/profile_pictures/headshot.jpeg HTTP/1.1" 404 179
```

## Solution

### Step 1: Restart the Development Server
The URL configuration was updated, so you need to restart your Django server:

1. **Stop the current server** (if running):
   - Press `Ctrl+C` in the terminal where the server is running

2. **Start the server again**:
   ```bash
   python manage.py runserver
   ```

### Step 2: Clear Browser Cache
Sometimes browsers cache 404 responses. Try one of these:
- Hard refresh: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
- Open in an incognito/private window
- Clear browser cache

### Step 3: Verify the Configuration
The file has been verified to exist at:
- **File location**: `C:\Users\khatr\OneDrive\Desktop\gt_movies\media\profile_pictures\headshot.jpeg`
- **File size**: 62,596 bytes
- **Expected URL**: `http://localhost:8000/media/profile_pictures/headshot.jpeg`

### Step 4: Test Direct Access
After restarting the server, try accessing the image directly:
1. Go to: `http://localhost:8000/media/profile_pictures/headshot.jpeg`
2. You should see the image load in your browser

### Step 5: Verify DEBUG Mode
Make sure `DEBUG = True` in `config/settings.py` (it should be, but double-check):
```python
DEBUG = True
```

Media files are only automatically served in DEBUG mode during development.

## What Was Fixed

1. **Updated `config/urls.py`**: 
   - Added proper conditional serving of media files
   - Media files now only served when `DEBUG = True`

2. **Configuration verified**:
   - `MEDIA_URL = '/media/'` ✓
   - `MEDIA_ROOT = BASE_DIR / 'media'` ✓
   - Static file serving enabled ✓

## If Still Not Working

### Quick Debug Check:
Run this command to verify everything:
```bash
python test_media.py
```

### Check Server Console:
When you access the profile page, you should see in the server console:
```
"GET /profile/ HTTP/1.1" 200 xxxx
"GET /media/profile_pictures/headshot.jpeg HTTP/1.1" 200 62596
```

If you see `404` instead of `200`, the server hasn't been restarted yet.

### Manual Test URLs:
Try these URLs in your browser after restarting the server:
1. `http://localhost:8000/media/movie_images/avatar.jpg` (existing movie image)
2. `http://localhost:8000/media/profile_pictures/headshot.jpeg` (your profile picture)

Both should load successfully.

## Production Note
When deploying to production (PythonAnywhere, Heroku, etc.), you'll need to:
1. Configure a web server (like Nginx or Apache) to serve media files
2. OR use a cloud storage service (like AWS S3, Cloudinary)
3. The current setup only works in development with `DEBUG = True`

