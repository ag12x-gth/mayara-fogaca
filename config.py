import os
import re
from typing import Optional

class Config:
    """
    Configuration class for managing environment variables
    Enhanced with better error handling and default values
    """
    
    # Default phone number for development/testing (can be overridden by env var)
    DEFAULT_LEAD_PHONE = '+1-555-0123'
    
    def __init__(self, require_env_var: bool = True):
        # Get the lead phone number from environment variable with optional fallback
        self.lead_phone_number: Optional[str] = os.getenv('LEAD_PHONE_NUMBER')
        
        if not self.lead_phone_number:
            if require_env_var:
                raise ValueError(
                    'LEAD_PHONE_NUMBER environment variable is required. '
                    'Please set it to your lead contact phone number.'
                )
            else:
                # Use default value for development
                self.lead_phone_number = self.DEFAULT_LEAD_PHONE
                print(f'Warning: Using default phone number {self.DEFAULT_LEAD_PHONE}. '
                      'Set LEAD_PHONE_NUMBER environment variable for production.')
    
    def get_lead_phone_number(self) -> str:
        """
        Returns the lead phone number from environment variable or default
        
        Returns:
            str: The lead phone number
        """
        return self.lead_phone_number
    
    def get_formatted_phone_number(self, format_type: str = 'standard') -> str:
        """
        Returns formatted phone number in different formats
        
        Args:
            format_type: 'standard', 'international', 'digits_only'
            
        Returns:
            str: Formatted phone number
        """
        if not self.lead_phone_number:
            return ''
            
        # Clean the number first
        clean_number = re.sub(r'[^\d]', '', self.lead_phone_number)
        
        if format_type == 'digits_only':
            return clean_number
        elif format_type == 'international' and len(clean_number) >= 10:
            if len(clean_number) == 10:
                return f'+1-{clean_number[:3]}-{clean_number[3:6]}-{clean_number[6:]}'
            else:
                return f'+{clean_number[0]}-{clean_number[1:4]}-{clean_number[4:7]}-{clean_number[7:]}'
        elif format_type == 'standard' and len(clean_number) >= 10:
            if len(clean_number) == 10:
                return f'({clean_number[:3]}) {clean_number[3:6]}-{clean_number[6:]}'
            else:
                # International number
                return f'+{clean_number[0]} ({clean_number[1:4]}) {clean_number[4:7]}-{clean_number[7:]}'
        
        return self.lead_phone_number  # Return original if formatting fails
    
    def validate_phone_number(self) -> bool:
        """
        Enhanced validation for phone number format using regex
        
        Returns:
            bool: True if phone number is valid, False otherwise
        """
        if not self.lead_phone_number:
            return False
            
        # Remove all non-digit characters for validation
        clean_number = re.sub(r'[^\d]', '', self.lead_phone_number)
        
        # Check if it's all digits and has appropriate length (10 or 11 digits)
        return clean_number.isdigit() and len(clean_number) in [10, 11]
    
    def is_us_number(self) -> bool:
        """
        Check if the phone number is a US number
        
        Returns:
            bool: True if US number, False otherwise
        """
        if not self.validate_phone_number():
            return False
            
        clean_number = re.sub(r'[^\d]', '', self.lead_phone_number)
        
        # US numbers are 10 digits or 11 digits starting with 1
        return len(clean_number) == 10 or (len(clean_number) == 11 and clean_number.startswith('1'))

# Usage example
if __name__ == '__main__':
    print('=== Production Mode (requires LEAD_PHONE_NUMBER env var) ===')
    try:
        config_prod = Config(require_env_var=True)
        print(f'Lead phone number: {config_prod.get_lead_phone_number()}')
        print(f'Formatted (standard): {config_prod.get_formatted_phone_number("standard")}')
        print(f'Formatted (international): {config_prod.get_formatted_phone_number("international")}')
        print(f'Digits only: {config_prod.get_formatted_phone_number("digits_only")}')
        print(f'Is valid: {config_prod.validate_phone_number()}')
        print(f'Is US number: {config_prod.is_us_number()}')
    except ValueError as e:
        print(f'Production Error: {e}')
        
        print('\n=== Development Mode (uses default if env var missing) ===')
        config_dev = Config(require_env_var=False)
        print(f'Lead phone number: {config_dev.get_lead_phone_number()}')
        print(f'Formatted (standard): {config_dev.get_formatted_phone_number("standard")}')
        print(f'Formatted (international): {config_dev.get_formatted_phone_number("international")}')
        print(f'Digits only: {config_dev.get_formatted_phone_number("digits_only")}')
        print(f'Is valid: {config_dev.validate_phone_number()}')
        print(f'Is US number: {config_dev.is_us_number()}')
