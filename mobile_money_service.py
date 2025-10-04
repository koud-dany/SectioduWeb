import requests
import uuid
import json
from datetime import datetime
import hashlib
import base64

class MobileMoneyService:
    """Mobile Money Payment Service Handler"""
    
    def __init__(self, config):
        self.config = config
        
    def generate_transaction_id(self):
        """Generate unique transaction ID"""
        return str(uuid.uuid4())
    
    def format_phone_number(self, phone_number):
        """Format phone number for mobile money APIs"""
        # Remove all non-digits
        cleaned = ''.join(filter(str.isdigit, phone_number))
        
        # For MTN test numbers, they should be in format: 46733123450
        # For real numbers, format based on country code
        if cleaned.startswith('46733123'):  # MTN test numbers
            return cleaned
        elif cleaned.startswith('237'):  # Cameroon
            return cleaned
        elif cleaned.startswith('256'):  # Uganda
            return cleaned
        elif cleaned.startswith('233'):  # Ghana
            return cleaned
        else:
            # Default: remove leading + or 0 and ensure proper format
            if cleaned.startswith('0'):
                cleaned = cleaned[1:]
            return cleaned
    
    def is_demo_mode(self):
        """Check if running in demo mode (no real API credentials)"""
        # Check if we have placeholder credentials
        api_user = self.config.get('mtn_momo', {}).get('api_user', '')
        api_key = self.config.get('mtn_momo', {}).get('api_key', '')
        
        placeholder_users = [
            'sandbox_api_user_123', 
            '00000000-0000-0000-0000-000000000000', 
            'your-mtn-api-user-id',
            'bcf6b5d8-5a06-4f33-af77-7b8c9e2f1a3d'  # Test UUID for development
        ]
        placeholder_keys = [
            'sandbox_api_key_456', 
            'your-generated-api-key-here', 
            'your-mtn-api-key',
            'test-api-key-for-development-2024'  # Test API key for development
        ]
        
        return api_user in placeholder_users or api_key in placeholder_keys
    
    def mock_payment_response(self, phone_number, amount, currency):
        """Generate mock payment response for demo mode"""
        transaction_ref = self.generate_transaction_id()
        formatted_phone = self.format_phone_number(phone_number)
        
        print(f"🎭 DEMO MODE: Mock payment initiated")
        print(f"   Phone: {formatted_phone}")
        print(f"   Amount: {amount} {currency}")
        print(f"   Transaction ID: {transaction_ref}")
        
        # For demo purposes, always simulate successful payment
        return {
            'success': True,
            'transaction_id': transaction_ref,
            'status': 'successful',  # Changed to successful for immediate access
            'message': '� DEMO MODE: Payment successful! Tournament access granted.'
        }
    
    def mtn_momo_request_payment(self, phone_number, amount, currency="USD"):
        """Request payment via MTN Mobile Money"""
        try:
            # Check if using mock/demo mode for testing
            if self.is_demo_mode():
                return self.mock_payment_response(phone_number, amount, currency)
            
            # Validate and format phone number
            formatted_phone = self.format_phone_number(phone_number)
            
            # Check if using test environment with test phone numbers
            test_numbers = ["46733123450", "46733123451", "46733123452"]
            if formatted_phone not in test_numbers:
                print(f"Warning: {formatted_phone} is not a valid test number. Use one of: {test_numbers}")
            
            # Generate transaction reference
            transaction_ref = self.generate_transaction_id()
            
            # Get access token
            try:
                access_token = self.get_mtn_access_token()
            except Exception as token_error:
                return {
                    'success': False,
                    'error': f'Failed to get access token: {str(token_error)}',
                    'message': 'MTN MoMo authentication failed. Please check API credentials or enable demo mode.'
                }
            
            # MTN MoMo API headers
            headers = {
                'Authorization': f'Bearer {access_token}',
                'X-Reference-Id': transaction_ref,
                'X-Target-Environment': 'sandbox',  # Change to 'live' for production
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': self.config['mtn_momo']['subscription_key']
            }
            
            # Payment request payload
            payload = {
                'amount': str(amount),
                'currency': currency,
                'externalId': transaction_ref,
                'payer': {
                    'partyIdType': 'MSISDN',
                    'partyId': formatted_phone
                },
                'payerMessage': self.config['payment']['description'],
                'payeeNote': 'Video Tournament Entry Payment'
            }
            
            print(f"MTN MoMo Payment Request:")
            print(f"  Phone: {formatted_phone}")
            print(f"  Amount: {amount} {currency}")
            print(f"  Transaction ID: {transaction_ref}")
            
            # Make payment request
            url = f"{self.config['mtn_momo']['base_url']}/collection/v1_0/requesttopay"
            print(f"Making request to: {url}")
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 202:
                return {
                    'success': True,
                    'transaction_id': transaction_ref,
                    'status': 'pending',
                    'message': 'Payment request sent. Please check your phone to complete payment.'
                }
            else:
                error_detail = "Unknown error"
                try:
                    error_response = response.json()
                    error_detail = error_response.get('message', str(error_response))
                except:
                    error_detail = response.text or f"HTTP {response.status_code}"
                
                print(f"MTN MoMo Error Response: {error_detail}")
                
                return {
                    'success': False,
                    'error': f'MTN MoMo API error: {response.status_code} - {error_detail}',
                    'message': 'Failed to initiate payment. Please check your credentials and try again.'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Payment request failed'
            }
    
    def get_mtn_access_token(self):
        """Get MTN MoMo access token"""
        try:
            url = f"{self.config['mtn_momo']['base_url']}/collection/token/"
            
            # Create credentials string for base64 encoding
            credentials = f"{self.config['mtn_momo']['api_user']}:{self.config['mtn_momo']['api_key']}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Ocp-Apim-Subscription-Key': self.config['mtn_momo']['subscription_key'],
                'Authorization': f"Basic {encoded_credentials}"
            }
            
            response = requests.post(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('access_token')
            else:
                raise Exception(f"Failed to get access token: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Token generation failed: {str(e)}")
    
    def check_mtn_payment_status(self, transaction_id):
        """Check MTN MoMo payment status"""
        try:
            # Demo mode simulation
            if self.is_demo_mode():
                print(f"🎭 DEMO MODE: Checking payment status for {transaction_id}")
                # Simulate successful payment after some time
                return {
                    'success': True,
                    'status': 'successful',
                    'transaction_id': transaction_id,
                    'amount': '35',
                    'currency': 'USD'
                }
            
            headers = {
                'Authorization': f'Bearer {self.get_mtn_access_token()}',
                'X-Target-Environment': 'sandbox',
                'Ocp-Apim-Subscription-Key': self.config['mtn_momo']['subscription_key']
            }
            
            url = f"{self.config['mtn_momo']['base_url']}/collection/v1_0/requesttopay/{transaction_id}"
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                payment_data = response.json()
                return {
                    'success': True,
                    'status': payment_data.get('status', 'unknown').lower(),
                    'transaction_id': transaction_id,
                    'amount': payment_data.get('amount'),
                    'currency': payment_data.get('currency')
                }
            else:
                return {
                    'success': False,
                    'error': f'Status check failed: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def orange_money_request_payment(self, phone_number, amount, currency="USD"):
        """Request payment via Orange Money"""
        try:
            # Demo mode - simulate successful payment
            transaction_ref = self.generate_transaction_id()
            
            print(f"🧡 DEMO MODE: Orange Money payment initiated")
            print(f"   Phone: {phone_number}")
            print(f"   Amount: {amount} {currency}")
            print(f"   Transaction ID: {transaction_ref}")
            
            return {
                'success': True,
                'transaction_id': transaction_ref,
                'status': 'successful',  # Changed to successful for demo
                'message': '🧡 DEMO MODE: Orange Money payment successful! Tournament access granted.',
                'provider': 'orange_money'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Orange Money payment failed'
            }
    
    def airtel_money_request_payment(self, phone_number, amount, currency="USD"):
        """Request payment via Airtel Money"""
        try:
            # Demo mode - simulate successful payment
            transaction_ref = self.generate_transaction_id()
            
            print(f"📱 DEMO MODE: Airtel Money payment initiated")
            print(f"   Phone: {phone_number}")
            print(f"   Amount: {amount} {currency}")
            print(f"   Transaction ID: {transaction_ref}")
            
            return {
                'success': True,
                'transaction_id': transaction_ref,
                'status': 'successful',  # Changed to successful for demo
                'message': '📱 DEMO MODE: Airtel Money payment successful! Tournament access granted.',
                'provider': 'airtel_money'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Airtel Money payment failed'
            }
    
    def process_mobile_payment(self, provider, phone_number, amount, currency="USD"):
        """Process payment based on selected provider"""
        if provider == 'mtn_momo':
            return self.mtn_momo_request_payment(phone_number, amount, currency)
        elif provider == 'orange_money':
            return self.orange_money_request_payment(phone_number, amount, currency)
        elif provider == 'airtel_money':
            return self.airtel_money_request_payment(phone_number, amount, currency)
        else:
            return {
                'success': False,
                'error': 'Unsupported payment provider',
                'message': 'Please select a valid mobile money provider'
            }
