import os
from typing import Optional

class Config:
    """
    Configuration class for managing environment variables
    """
    
    def __init__(self):
        # Get the lead phone number from environment variable
        self.lead_phone_number: Optional[str] = os.getenv('LEAD_PHONE_NUMBER')
        
        if not self.lead_phone_number:
            raise ValueError('LEAD_PHONE_NUMBER environment variable is required')
    
    def get_lead_phone_number(self) -> str:
        """
        Returns the lead phone number from environment variable
        
        Returns:
            str: The lead phone number
        """
        return self.lead_phone_number
    
    def validate_phone_number(self) -> bool:
        """
        Basic validation for phone number format
        
        Returns:
            bool: True if phone number is valid, False otherwise
        """
        if not self.lead_phone_number:
            return False
            
        # Remove common phone number separators
        clean_number = self.lead_phone_number.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        
        # Check if it's all digits and has appropriate length
        return clean_number.isdigit() and len(clean_number) >= 10

# Usage example
if __name__ == '__main__':
    try:
        config = Config()
        print(f'Lead phone number: {config.get_lead_phone_number()}')
        print(f'Is valid: {config.validate_phone_number()}')
    except ValueError as e:
        print(f'Error: {e}')
        print('Please set the LEAD_PHONE_NUMBER environment variable')
