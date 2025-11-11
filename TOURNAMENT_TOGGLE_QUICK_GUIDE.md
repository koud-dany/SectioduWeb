# Tournament Toggle Feature - Quick Reference

## What It Does
Allows admins to open/close the tournament, controlling:
- ✅ Participant video uploads
- ✅ New participant registrations
- ❌ Does NOT affect: Existing videos, voting, viewing, or browsing

## Quick Start

### 1. Initialize (First Time)
```bash
python init_tournament_settings.py
```

### 2. Test Installation
```bash
python test_tournament_toggle.py
```

### 3. Use as Admin
1. Go to `/admin` dashboard
2. Look for "Tournament Status" card at top
3. Click "Close Tournament" or "Open Tournament"
4. Confirm the action
5. Page reloads with new status

## Status Indicators

### OPEN (Green Badge)
- 🟢 Participants can upload videos
- 🟢 Users can register as participants
- 🟢 All normal operations

### CLOSED (Red Badge)
- 🔴 Video uploads blocked
- 🔴 New registrations blocked
- 🟢 Existing videos still viewable
- 🟢 Voting still works
- 🟢 Comments still work

## Key Files Modified

### Backend
- `app.py`: Core functionality (3 functions, 2 routes, 3 checks)
  - `is_tournament_open()` - Check status
  - `/admin/toggle_tournament` - Toggle endpoint
  - `/admin/tournament_status` - Status endpoint
  - Upload route protection
  - Upgrade route protection

### Frontend
- `templates/admin/dashboard.html` - Toggle UI
- `templates/upgrade_mobile.html` - Closed alert

### Database
- `system_settings` table
  - `tournament_open` = 'true' or 'false'

### Translations
- `static/translations/en.json` - English messages
- `static/translations/fr.json` - French messages

## Admin Actions

```bash
# View current status
python -c "from app import is_tournament_open; print('OPEN' if is_tournament_open() else 'CLOSED')"

# Manual toggle via database
sqlite3 tournament.db "UPDATE system_settings SET setting_value = 'false' WHERE setting_key = 'tournament_open';"
```

## Template Usage
```html
{% if tournament_open %}
    <a href="{{ url_for('upload_video') }}">Upload Video</a>
{% else %}
    <span class="text-muted">Tournament Closed</span>
{% endif %}
```

## Routes Protected
- `/upload_video` - Redirects to dashboard when closed
- `/upgrade` - Redirects to dashboard when closed

## Logged Actions
Every toggle is logged in `admin_logs`:
- Admin user ID
- Action: 'toggle_tournament'
- Timestamp
- Details: "Tournament opened/closed"

## Testing Checklist
- [x] Database table created
- [x] Default status is 'true' (OPEN)
- [x] Toggle works correctly
- [x] Upload blocked when closed
- [x] Upgrade blocked when closed
- [x] Admin UI displays correctly
- [x] Translations work (EN/FR)
- [x] All tests pass

## Common Issues

**Q: How do I check if tournament is open?**
A: Look at admin dashboard or run: `python -c "from app import is_tournament_open; print(is_tournament_open())"`

**Q: Can I schedule automatic opening/closing?**
A: Not yet - manual toggle only (future enhancement)

**Q: What happens to existing videos when closed?**
A: Nothing - they remain viewable and votable

**Q: Can users still vote when tournament is closed?**
A: Yes - only uploads and registrations are blocked

## Support
- Full documentation: `TOURNAMENT_TOGGLE_FEATURE.md`
- Test script: `test_tournament_toggle.py`
- Init script: `init_tournament_settings.py`
