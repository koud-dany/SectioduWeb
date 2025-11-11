# 🏆 Tournament Toggle Feature

## Overview
The Tournament Toggle feature allows super admins to open and close the tournament competition, automatically managing participant status and access control.

## How It Works

### 🟢 When Tournament is OPEN
- Users can pay $35 to upgrade to participant status
- Participants can upload videos
- Competition is active
- Leaderboard displays rankings

### 🔴 When Tournament is CLOSED
- **All participants are immediately downgraded to regular users**
- Users cannot upgrade to participant status (upgrade button disabled)
- Ex-participants cannot upload videos
- Existing videos remain visible and votable
- Payment history is preserved in database

## Admin Controls

### Accessing the Toggle
1. Log in as a super admin
2. Navigate to **Admin Dashboard** (`/admin/dashboard`)
3. See the Tournament Control Panel at the top
4. Click **CLOSE Tournament** or **OPEN Tournament** button

### Confirmation Dialog
When closing the tournament, admins see a warning message showing:
- Number of participants that will be affected
- Consequences of closing
- Confirmation requirement

### Visual Indicators
- **Green background**: Tournament is OPEN 🟢
- **Red background**: Tournament is CLOSED 🔴
- **Participant count**: Shows current active participants
- **Last updated timestamp**: When status was last changed

## Database Structure

### Tables Created/Modified

#### `tournament_settings`
```sql
- id: 1 (singleton record)
- is_open: BOOLEAN (TRUE = open, FALSE = closed)
- last_updated: TIMESTAMP
- updated_by: INTEGER (admin user_id)
```

#### `payment_history`
```sql
- id: AUTO INCREMENT
- user_id: INTEGER
- amount: REAL ($35.00)
- payment_type: 'participant_fee'
- payment_date: TIMESTAMP
- transaction_id: TEXT
- status: 'completed'
- tournament_session: INTEGER
```

#### `users` table - New Column
```sql
- was_participant: BOOLEAN (tracks who was ever a participant)
```

## Payment Logic

### First Time Participant
1. User pays $35
2. `is_paid` = TRUE
3. `was_participant` = TRUE
4. Payment recorded in `payment_history`

### Tournament Closes
1. Admin clicks CLOSE button
2. All users with `is_paid = TRUE` are downgraded
3. `is_paid` = FALSE (downgraded to regular user)
4. `was_participant` = TRUE (history preserved)
5. Payment record remains in `payment_history`

### Tournament Reopens
1. Admin clicks OPEN button
2. Ex-participants (was_participant = TRUE) must pay $35 again
3. New payment creates new entry in `payment_history`
4. `is_paid` = TRUE (upgraded back to participant)

### Key Points
- **Users must pay EVERY time** tournament closes and reopens
- **Payment history is preserved** for auditing
- **No refunds** - payment is per tournament session
- **Videos remain visible** even after downgrade

## Admin Logging

Every tournament toggle action is logged in `admin_logs`:
```sql
- admin_id: Who performed the action
- action: 'toggle_tournament'
- target_type: 'tournament'
- target_id: 1
- details: Description of what happened
- timestamp: When it occurred
```

## Frontend Implementation

### Admin Dashboard Components
1. **Tournament Control Panel** (top of dashboard)
   - Color-coded status indicator
   - Participant count badge
   - Last updated timestamp
   - Large toggle button

2. **Confirmation Dialog**
   - Warning about consequences
   - Participant count
   - Clear action description
   - Double confirmation required

3. **AJAX Submission**
   - No page reload needed
   - Loading spinner during processing
   - Success/error messages
   - Auto-refresh after successful toggle

### User-Facing Changes
- Upgrade button disabled when tournament closed
- Flash message: "Tournament is currently closed"
- Upload page checks tournament status
- Clear messaging about payment requirements

## Security

### Access Control
- Only super admins (`@admin_required('super')`) can toggle
- Regular admins cannot access this feature
- Logged in `admin_logs` for audit trail

### Data Integrity
- Transactions are atomic (all or nothing)
- Foreign key constraints maintained
- Payment history never deleted

## Testing Checklist

✅ **Before Deployment:**
1. [ ] Test opening tournament as super admin
2. [ ] Test closing tournament with active participants
3. [ ] Verify participants are downgraded
4. [ ] Verify videos remain visible
5. [ ] Test that downgraded users cannot upload
6. [ ] Test that users cannot upgrade when closed
7. [ ] Verify payment history is preserved
8. [ ] Test reopening tournament
9. [ ] Verify ex-participants must pay again
10. [ ] Check admin logs for proper recording

## API Endpoints

### POST `/admin/toggle-tournament`
**Access:** Super Admin only
**Method:** POST
**Headers:** `X-Requested-With: XMLHttpRequest` (for AJAX)

**Response (JSON):**
```json
{
  "success": true,
  "message": "Tournament status message",
  "new_status": "open" | "closed"
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error description"
}
```

## Troubleshooting

### Tournament button not working?
1. Check browser console for JavaScript errors
2. Verify admin has super admin level
3. Check Flask logs for backend errors

### Participants not downgraded?
1. Check `tournament_settings` table: `is_open` should be FALSE
2. Check `users` table: `is_paid` should be FALSE for ex-participants
3. Check `admin_logs` for error messages

### Payment history not showing?
1. Run migration script: `python create_tournament_settings.py`
2. Check `payment_history` table exists
3. Verify foreign key constraints

## Future Enhancements

- [ ] Tournament session tracking (tournament #1, #2, etc.)
- [ ] Automatic tournament close on end date
- [ ] Email notifications to participants when status changes
- [ ] Tournament archive (history of all tournaments)
- [ ] Refund mechanism for early closure
- [ ] Grace period before downgrade
- [ ] Partial refunds for tournament cancellation

## Files Modified

### Backend
- `app.py` - Added `admin_toggle_tournament()` route
- `app.py` - Modified `admin_dashboard()` to include tournament status
- `create_tournament_settings.py` - Database setup script

### Frontend
- `templates/admin/dashboard.html` - Added tournament control panel
- `templates/admin/dashboard.html` - Added JavaScript for toggle confirmation

### Database
- `tournament.db` - Added/modified tables as described above

## Support

For issues or questions about the tournament toggle feature, check:
1. Admin logs in database
2. Flask console output
3. Browser developer console
4. This documentation file

---
**Last Updated:** 2025-11-09
**Version:** 1.0.0
**Author:** SectionduWeb Development Team
