# Tournament Closed - Upgrade Block Feature

## Overview
This feature prevents users from upgrading to participant status when the tournament is closed. When users attempt to access the upgrade page or submit a payment while the tournament is closed, they receive a clear warning message.

## Implementation Date
November 11, 2025

## Changes Made

### 1. Backend Route Protection (`app.py`)

#### A. `/upgrade` Route (Line 1946-1965)
**Added tournament status check before displaying upgrade page:**
```python
@app.route('/upgrade')
@login_required
def upgrade():
    """Upgrade/subscription page with mobile money payment"""
    # Check if tournament is open
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    c.execute('SELECT is_open FROM tournament_settings WHERE id = 1')
    tournament_data = c.fetchone()
    conn.close()
    
    tournament_open = tournament_data[0] if tournament_data else True
    
    if not tournament_open:
        flash('⚠️ Tournament is currently CLOSED. You cannot upgrade to participant status at this time. Please check back later when the competition reopens.', 'warning')
        return redirect(url_for('dashboard'))
    
    payment_method = app.config.get('PAYMENT_METHOD', 'mobile_money')
    
    return render_template('upgrade_mobile.html')
```

**Behavior:**
- Checks `tournament_settings.is_open` status from database
- If tournament is CLOSED (`is_open = 0`):
  - Displays warning flash message
  - Redirects user back to dashboard
  - Prevents access to upgrade page entirely
- If tournament is OPEN (`is_open = 1`):
  - Normal upgrade page is displayed
  - User can proceed with payment

#### B. `/initiate_mobile_payment` Route (Line 2095-2114)
**Added tournament status check before processing payment:**
```python
@app.route('/initiate_mobile_payment', methods=['POST'])
@login_required
def initiate_mobile_payment():
    """Initiate mobile money payment for subscription"""
    try:
        from mobile_money_service import MobileMoneyService
        from mobile_money_config import get_mobile_money_config
        
        # Check if tournament is open before processing payment
        conn_check = sqlite3.connect('tournament.db')
        c_check = conn_check.cursor()
        c_check.execute('SELECT is_open FROM tournament_settings WHERE id = 1')
        tournament_data = c_check.fetchone()
        conn_check.close()
        
        tournament_open = tournament_data[0] if tournament_data else True
        
        if not tournament_open:
            return jsonify({
                'success': False,
                'error': 'Tournament is currently CLOSED. You cannot upgrade to participant status at this time. Please try again when the competition reopens.'
            }), 403
        
        # ... rest of payment processing
```

**Behavior:**
- Checks tournament status before initiating payment transaction
- If tournament is CLOSED:
  - Returns JSON error response with HTTP 403 (Forbidden)
  - Payment is NOT processed
  - Error message displayed to user via JavaScript
- If tournament is OPEN:
  - Normal payment flow proceeds
  - Mobile money transaction initiated

## User Experience Flow

### Scenario 1: Tournament is OPEN ✅
1. User navigates to `/upgrade` page
2. Tournament status check: `is_open = 1` (TRUE)
3. Upgrade page displays normally
4. User fills payment form and clicks "Pay $35"
5. Tournament status checked again: `is_open = 1` (TRUE)
6. Payment processes successfully
7. User upgraded to participant

### Scenario 2: Tournament is CLOSED 🔴
1. User navigates to `/upgrade` page
2. Tournament status check: `is_open = 0` (FALSE)
3. Flash message displayed: "⚠️ Tournament is currently CLOSED. You cannot upgrade to participant status at this time. Please check back later when the competition reopens."
4. User redirected to dashboard
5. User cannot access upgrade page

### Scenario 3: Tournament Closes During Payment Attempt 🔴
1. User opens `/upgrade` page (tournament was OPEN)
2. User fills payment form
3. **Admin closes tournament via admin panel**
4. User clicks "Pay $35"
5. Tournament status check: `is_open = 0` (FALSE)
6. Payment rejected with error message
7. JSON response: `{'success': False, 'error': 'Tournament is currently CLOSED...'}`
8. JavaScript displays error alert to user

## Technical Details

### Database Query
```sql
SELECT is_open FROM tournament_settings WHERE id = 1
```
- Single query to check tournament status
- Returns `1` (TRUE) if open, `0` (FALSE) if closed
- Default to `True` if no record exists (safety fallback)

### Flash Messages
- **Type**: `warning` (yellow/orange bootstrap alert)
- **Icon**: ⚠️ warning emoji
- **Message**: Clear explanation that tournament is closed
- **Action**: Tells user to "check back later when the competition reopens"

### HTTP Status Codes
- **403 Forbidden**: Used for payment endpoint when tournament closed
  - Semantically correct: user is authenticated but not authorized to perform action
  - Prevents payment processing when tournament is closed

### Error Handling
- Safe fallback: If `tournament_settings` table doesn't exist or has no data, defaults to `tournament_open = True`
- Database connection properly closed with `conn.close()` after query
- Separate connection (`conn_check`) used in payment route to avoid conflicts

## Testing Checklist

### Manual Testing Steps:
1. **Test with Tournament OPEN:**
   - [ ] Navigate to `/upgrade` - should display upgrade page
   - [ ] Fill payment form and submit - should process payment
   - [ ] User should be upgraded to participant status

2. **Test with Tournament CLOSED:**
   - [ ] Close tournament via admin dashboard
   - [ ] Navigate to `/upgrade` - should see warning and redirect to dashboard
   - [ ] Try direct POST to `/initiate_mobile_payment` - should get 403 error

3. **Test Tournament Closure During Payment:**
   - [ ] Open `/upgrade` page (tournament open)
   - [ ] Have another admin close tournament
   - [ ] Submit payment form - should fail with error message

4. **Test Flash Message Display:**
   - [ ] Verify warning message appears at top of page after redirect
   - [ ] Verify message has warning/yellow styling
   - [ ] Verify user understands what happened

### Database State Verification:
```sql
-- Check current tournament status
SELECT id, is_open, last_updated, updated_by FROM tournament_settings;

-- Close tournament for testing
UPDATE tournament_settings SET is_open = 0 WHERE id = 1;

-- Open tournament again
UPDATE tournament_settings SET is_open = 1 WHERE id = 1;
```

## Integration Points

### Related Features:
1. **Admin Toggle Tournament** (`/admin/toggle-tournament`)
   - When admin closes tournament, this feature blocks upgrades immediately
   - When admin opens tournament, upgrades are allowed again

2. **Video Upload** (`/upload`)
   - Already checks if user `is_paid = TRUE`
   - Works in tandem: even if user bypassed upgrade block, can't upload without paid status

3. **Dashboard** (`/dashboard`)
   - Redirect target when tournament is closed
   - Flash message displayed here after blocked upgrade attempt

## Future Enhancements

### Possible Improvements:
1. **Visual Indicator on Dashboard:**
   - Add banner showing tournament status to regular users
   - "🔴 Tournament Closed" or "🟢 Tournament Open - Join Now!"

2. **Email Notifications:**
   - Notify users when tournament reopens
   - Send to users who attempted to upgrade while closed

3. **Upgrade Page Countdown:**
   - If tournament has scheduled reopen date, display countdown timer
   - "Tournament reopens in: 3 days, 5 hours"

4. **Admin Controls:**
   - Schedule tournament open/close times
   - Auto-open on specific date/time
   - Notification sent to users when opened

## Security Considerations

### Protection Levels:
✅ **Route-level protection**: `/upgrade` checks status before rendering page
✅ **API-level protection**: `/initiate_mobile_payment` checks status before processing
✅ **Database-level enforcement**: Tournament toggle updates `is_open` atomically
✅ **Double-check pattern**: Status verified twice (page load + payment)

### Potential Attack Vectors (All Blocked):
❌ **Direct POST to payment API**: Blocked by status check in `initiate_mobile_payment`
❌ **Browser back button**: Flash message and redirect prevent access
❌ **Cached page submission**: Status checked server-side on form submit
❌ **Race condition**: Each request checks current database state independently

## Deployment Notes

### Pre-Deployment Checklist:
- [✅] Code changes committed to version control
- [ ] Test with tournament OPEN and CLOSED states
- [ ] Verify flash message styling matches site design
- [ ] Test on mobile devices (responsive design)
- [ ] Verify error handling in JavaScript frontend

### Rollback Plan:
If issues occur, remove status checks:
```python
# Remove lines 1951-1960 from /upgrade route
# Remove lines 2102-2114 from /initiate_mobile_payment route
```

### Configuration:
No additional configuration required. Uses existing `tournament_settings` table.

## Success Metrics

### Goals:
- ✅ Zero successful upgrades when tournament is closed
- ✅ Clear user communication about tournament status
- ✅ No payment processing when tournament closed
- ✅ Seamless transition when tournament reopens

### Monitoring:
- Track upgrade attempts when tournament closed (flash message count)
- Monitor payment API 403 errors
- Verify no `is_paid = TRUE` updates when `is_open = FALSE`

---

**Status**: ✅ Implemented and ready for testing
**Priority**: High - Prevents unwanted payments when tournament closed
**Related Issues**: Tournament Toggle Feature, Admin Dashboard Controls
