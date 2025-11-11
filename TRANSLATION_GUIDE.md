# Translation Guide for SectionduWeb

## Overview
SectionduWeb now supports multiple languages! Users can easily switch between English, French, Spanish, German, and Italian.

## How Translation Works

### Backend (Python/Flask)
- Translations are stored in JSON files in `static/translations/`
- Each language has its own JSON file: `en.json`, `fr.json`, `es.json`, `de.json`, `it.json`
- The `app.py` file loads translations and makes them available to templates
- User's language preference is stored in the session

### Frontend (HTML/JavaScript)
- Templates use Jinja2 syntax to display translations: `{{ translations.nav.home }}`
- JavaScript can access translations via `window.translations` object
- Helper function `t(key)` can be used in JavaScript: `t('nav.home')`
- Elements with `data-i18n` attribute are automatically translated

## Language Switcher
A language dropdown is available in the navbar with flags for each language:
- 🇺🇸 English
- 🇫🇷 Français (French)
- 🇪🇸 Español (Spanish)
- 🇩🇪 Deutsch (German)
- 🇮🇹 Italiano (Italian)

## Usage in Templates

### Method 1: Jinja2 Templates (Recommended)
```html
<h1>{{ translations.video.title if translations.video else 'Title' }}</h1>
<button>{{ translations.common.submit if translations.common else 'Submit' }}</button>
```

### Method 2: Data Attributes (For Dynamic Content)
```html
<span data-i18n="nav.home">{{ translations.nav.home }}</span>
<button data-i18n="common.save">{{ translations.common.save }}</button>
```

### Method 3: JavaScript
```javascript
// Access translation in JavaScript
const title = t('video.title');
const submitText = t('common.submit');

// Update element text
document.getElementById('myButton').textContent = t('common.save');
```

## Translation File Structure

### English (en.json)
```json
{
  "nav": {
    "home": "Home",
    "videos": "Videos",
    "dashboard": "Dashboard"
  },
  "common": {
    "submit": "Submit",
    "cancel": "Cancel"
  },
  "video": {
    "title": "Title",
    "description": "Description"
  }
}
```

### French (fr.json)
```json
{
  "nav": {
    "home": "Accueil",
    "videos": "Vidéos",
    "dashboard": "Tableau de bord"
  },
  "common": {
    "submit": "Soumettre",
    "cancel": "Annuler"
  },
  "video": {
    "title": "Titre",
    "description": "Description"
  }
}
```

## Adding New Translations

1. **Edit all language files** in `static/translations/`
2. **Use nested structure** for organization:
   ```json
   {
     "section": {
       "subsection": {
         "key": "Translation"
       }
     }
   }
   ```
3. **Keep keys consistent** across all language files
4. **Test the translation** by switching languages

## Example: Adding Video Detail Page Translations

### 1. Add to en.json:
```json
{
  "video": {
    "rateThisVideo": "Rate this Video",
    "castYourVote": "Cast Your Vote",
    "comments": "Comments",
    "addComment": "Add a comment"
  }
}
```

### 2. Add to fr.json:
```json
{
  "video": {
    "rateThisVideo": "Notez cette vidéo",
    "castYourVote": "Votez maintenant",
    "comments": "Commentaires",
    "addComment": "Ajouter un commentaire"
  }
}
```

### 3. Use in template:
```html
<h5>{{ translations.video.rateThisVideo }}</h5>
<button>{{ translations.video.castYourVote }}</button>
```

## Available Translation Categories

- **nav**: Navigation menu items
- **footer**: Footer text
- **common**: Common buttons and actions
- **video**: Video-related text
- **comments**: Comment system
- **rating**: Rating system
- **auth**: Authentication (login/register)
- **dashboard**: Dashboard page
- **upload**: Upload video page
- **leaderboard**: Leaderboard page
- **profile**: Profile page
- **payment**: Payment/upgrade pages
- **admin**: Admin panel
- **messages**: Success/error messages

## Best Practices

1. **Always provide fallbacks**:
   ```html
   {{ translations.nav.home if translations.nav else 'Home' }}
   ```

2. **Use semantic keys**:
   - Good: `video.uploadDate`, `auth.signIn`
   - Bad: `text1`, `button2`

3. **Keep translations consistent**:
   - Use the same terminology across the app
   - Maintain similar tone and formality

4. **Test all languages**:
   - Switch to each language and verify
   - Check for text overflow in UI
   - Ensure special characters display correctly

5. **Use proper encoding**:
   - All JSON files use UTF-8 encoding
   - French accents: é, è, ê, à, ç
   - Spanish: ñ, á, é, í, ó, ú
   - German: ä, ö, ü, ß

## Dynamic Content Translation

For content that changes based on variables:

### In JavaScript:
```javascript
// Use template literals
const message = t('rating.ratingUpdated') + ' ' + oldRating + ' ' + t('rating.to') + ' ' + newRating;

// Example: "Rating updated from 3 to 5 stars"
// French: "Note mise à jour de 3 à 5 étoiles"
```

### In Templates:
```html
<p>
  {{ translations.rating.ratingUpdated }} {{ old_rating }} 
  {{ translations.rating.to }} {{ new_rating }} 
  {{ translations.rating.stars }}
</p>
```

## Troubleshooting

### Translation not showing?
1. Check if the key exists in the JSON file
2. Verify JSON syntax is valid
3. Clear browser cache
4. Restart Flask server

### Wrong language displaying?
1. Click the language switcher in navbar
2. Check session is persisting
3. Verify browser language settings

### Special characters broken?
1. Ensure files are UTF-8 encoded
2. Check `<meta charset="UTF-8">` in HTML
3. Verify Flask is serving with correct encoding

## API Endpoints

### Change Language
```
GET /set_language/<language>
```
Example: `/set_language/fr` switches to French

Parameters:
- `language`: Language code (en, fr, es, de, it)

Response: Redirects to referring page with language updated in session

## Session Storage

The selected language is stored in the Flask session:
```python
session['language'] = 'fr'
```

This persists across page loads until the user:
- Logs out
- Clears browser cookies
- Changes language again

## Future Enhancements

- Add more languages (Portuguese, Arabic, Chinese, etc.)
- User profile language preference
- Auto-detect browser language on first visit
- RTL (Right-to-Left) support for Arabic/Hebrew
- Pluralization support
- Date/time localization
- Number format localization

## Contributing Translations

To contribute a new language:

1. Copy `en.json` to new file (e.g., `pt.json` for Portuguese)
2. Translate all values (keep keys in English)
3. Add language to `SUPPORTED_LANGUAGES` in `app.py`
4. Add dropdown option in `base.html` navbar
5. Test thoroughly
6. Submit pull request

## Contact

For translation issues or suggestions, please contact the development team or open an issue on GitHub.

---
**Note**: Translations are constantly being improved. Some pages may still be partially in English while we complete the translation coverage.
