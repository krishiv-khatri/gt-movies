# Profile Picture Upload Feature

## Overview
This feature allows users to upload and manage profile pictures on their profile page. Users can now personalize their accounts by showing everyone what they look like!

## What Was Implemented

### 1. **Database Model** (`store/models.py`)
- Created `UserProfile` model with the following fields:
  - `profile_picture`: ImageField for storing profile pictures
  - `bio`: TextField for user biography (max 500 characters)
  - `created_at`: Timestamp when profile was created
  - `updated_at`: Timestamp when profile was last updated
- Added signal handlers to automatically create a UserProfile for every new user

### 2. **Forms** (`store/forms.py`)
- Created `UserProfileForm` that allows users to:
  - Upload a profile picture (accepts JPG, PNG, GIF)
  - Edit their bio
  - Update first name, last name, and email

### 3. **Views** (`store/views.py`)
- `profile_view`: Displays the user's profile with:
  - Profile picture (or default avatar if not set)
  - Personal information (username, email, name)
  - Bio
  - Activity statistics (reviews count, orders count, cart items)
- `profile_edit`: Allows users to edit their profile with:
  - Profile picture upload with live preview
  - Form validation and error handling
  - Success messages

### 4. **Templates**
- `store/templates/store/profile.html`: Profile view page with a clean, modern UI
- `store/templates/store/profile_edit.html`: Profile editing page with:
  - Image upload with preview
  - Form fields for all editable information
  - JavaScript for live image preview before upload

### 5. **Navigation Updates** (`store/templates/store/base.html`)
- Added "My Profile" link to the user dropdown menu
- Profile picture now appears in the navigation bar (thumbnail next to username)
- Updated dropdown menu with icons for better UX

### 6. **URL Configuration** (`store/urls.py`)
- `/profile/` - View user profile
- `/profile/edit/` - Edit user profile

### 7. **Admin Interface** (`store/admin.py`)
- Registered UserProfile model in admin
- Added Profile inline to User admin for easy management
- Admins can now view and edit user profiles from the Django admin

### 8. **Management Command**
- Created `create_user_profiles` command to ensure all existing users have profiles
- Already executed - 5 user profiles were created for existing users

## How to Use

### For End Users:
1. **View Your Profile:**
   - Click on your username in the top navigation bar
   - Select "My Profile" from the dropdown menu
   - View your profile information and statistics

2. **Edit Your Profile:**
   - Go to your profile page
   - Click the "Edit Profile" button
   - Upload a profile picture (recommended size: 400x400px)
   - Update your bio and personal information
   - Click "Save Changes"

3. **Profile Picture:**
   - Your profile picture will appear in the navigation bar
   - It will be displayed on your profile page
   - Other users can see your profile picture when viewing your reviews

### For Administrators:
- Access user profiles through the Django admin interface
- Edit user profiles inline when managing users
- View profile statistics and information

## File Structure
```
store/
├── models.py                          # UserProfile model
├── forms.py                           # UserProfileForm
├── views.py                           # profile_view, profile_edit
├── urls.py                            # Profile URL patterns
├── admin.py                           # UserProfile admin
├── templates/store/
│   ├── profile.html                   # Profile view template
│   ├── profile_edit.html              # Profile edit template
│   └── base.html                      # Updated navigation
└── management/commands/
    └── create_user_profiles.py        # Profile creation command

media/
└── profile_pictures/                  # Uploaded profile pictures stored here
```

## Technical Details

### Media Files
- Profile pictures are uploaded to `media/profile_pictures/`
- Media files are properly configured in `config/settings.py`
- Media URLs are served in development via `config/urls.py`

### Database Migration
- Migration `0008_userprofile.py` was created and applied
- All existing users have been given UserProfile instances

### Security
- Only authenticated users can view/edit their profiles
- Users can only edit their own profiles (enforced via `@login_required` decorator)
- File upload validation ensures only images are accepted
- CSRF protection enabled on all forms

## Testing
To test the feature:
1. Start the development server: `python manage.py runserver`
2. Log in with an existing user account
3. Click on your username → "My Profile"
4. Click "Edit Profile" and upload a profile picture
5. Save changes and verify the picture appears in navigation

## Future Enhancements (Optional)
- Image cropping/resizing before upload
- Avatar selection (default avatars to choose from)
- Public profile pages for users
- Profile picture displayed next to reviews
- Profile completion percentage indicator

