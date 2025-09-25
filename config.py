import os
import re
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """
    Enhanced configuration class for managing environment variables
    with comprehensive validation, error handling, and phone number utilities
    """
    
    # Default phone number for development/testing (Brazilian format)
    DEFAULT_LEAD_PHONE = '5511999999999'
    
    # Supported phone number formats
    PHONE_PATTERNS = {
        'brazilian': re.compile(r'^55\d{10,11}$'),  # 55 + 10-11 digits
        'us': re.compile(r'^1?\d{10}$'),            # Optional 1 + 10 digits
        'international': re.compile(r'^\d{10,15}$') # 10-15 digits general
    }
    
    def __init__(self, require_env_var: bool = True):
        """
        Initialize configuration with enhanced error handling
        
        Args:
            require_env_var: Whether to require LEAD_PHONE_NUMBER env var
        """
        self.lead_phone_number: Optional[str] = os.getenv('LEAD_PHONE_NUMBER')
        
        if not self.lead_phone_number:
            if require_env_var:
                raise ValueError(
                    'LEAD_PHONE_NUMBER environment variable is required. '
                    'Please set it to your lead contact phone number. '
                    'Example: export LEAD_PHONE_NUMBER="5511999999999"'
                )
            else:
                # Use default value for development
                self.lead_phone_number = self.DEFAULT_LEAD_PHONE
                logger.warning(
                    f'Using default phone number {self._mask_phone_number(self.DEFAULT_LEAD_PHONE)}. '
                    'Set LEAD_PHONE_NUMBER environment variable for production.'
                )
        
        # Validate and clean phone number on initialization
        self._validate_and_clean_phone()
    
    def _mask_phone_number(self, phone_number: str) -> str:
        """
        Mask phone number for logging purposes to protect sensitive data
        
        Args:
            phone_number: The phone number to mask
            
        Returns:
            str: Masked phone number for safe logging
        """
        if not phone_number or len(phone_number) < 4:
            return "****"
        
        # Show only first 2 and last 2 digits
        return phone_number[:2] + "*" * (len(phone_number) - 4) + phone_number[-2:]
    
    def _validate_and_clean_phone(self) -> None:
        """
        Validates and cleans the phone number on initialization
        """
        if not self.lead_phone_number:
            return
            
        # Clean the number (remove all non-digits)
        clean_number = re.sub(r'[^\d]', '', self.lead_phone_number)
        
        # Basic validation
        if not clean_number or len(clean_number) < 10:
            logger.error(f'Invalid phone number format (length: {len(clean_number)})')
            if hasattr(self, 'DEFAULT_LEAD_PHONE'):
                self.lead_phone_number = self.DEFAULT_LEAD_PHONE
                logger.info(f'Fallback to default: {self._mask_phone_number(self.DEFAULT_LEAD_PHONE)}')
        else:
            self.lead_phone_number = clean_number
            logger.info(f'Phone number validated and cleaned: {self._mask_phone_number(clean_number)}')
    
    def get_lead_phone_number(self) -> str:
        """
        Returns the lead phone number from environment variable or default
        
        Returns:
            str: The lead phone number (digits only)
        """
        return self.lead_phone_number or self.DEFAULT_LEAD_PHONE
    
    def get_formatted_phone_number(self, format_type: str = 'standard') -> str:
        """
        Returns formatted phone number in different formats with better validation
        
        Args:
            format_type: 'standard', 'international', 'digits_only', 'whatsapp'
            
        Returns:
            str: Formatted phone number
        """
        if not self.lead_phone_number:
            return ''
            
        clean_number = re.sub(r'[^\d]', '', self.lead_phone_number)
        
        try:
            if format_type == 'digits_only':
                return clean_number
            elif format_type == 'whatsapp':
                # Format specifically for WhatsApp API (ensure country code)
                if len(clean_number) == 11 and clean_number.startswith('11'):
                    return f'55{clean_number}'  # Add Brazil country code
                return clean_number
            elif format_type == 'international':
                return self._format_international(clean_number)
            elif format_type == 'standard':
                return self._format_standard(clean_number)
            else:
                logger.warning(f'Unknown format type: {format_type}')
                return clean_number
                
        except Exception as e:
            logger.error(f'Error formatting phone number: {e}')
            return clean_number
    
    def _format_international(self, clean_number: str) -> str:
        """Format number for international display"""
        if len(clean_number) >= 12 and clean_number.startswith('55'):  # Brazilian
            return f'+55 ({clean_number[2:4]}) {clean_number[4:9]}-{clean_number[9:]}'
        elif len(clean_number) == 11 and clean_number.startswith('1'):  # US
            return f'+1 ({clean_number[1:4]}) {clean_number[4:7]}-{clean_number[7:]}'
        elif len(clean_number) == 10:  # US without country code
            return f'+1 ({clean_number[:3]}) {clean_number[3:6]}-{clean_number[6:]}'
        else:
            return f'+{clean_number}'
    
    def _format_standard(self, clean_number: str) -> str:
        """Format number for standard display"""
        if len(clean_number) >= 12 and clean_number.startswith('55'):  # Brazilian
            return f'({clean_number[2:4]}) {clean_number[4:9]}-{clean_number[9:]}'
        elif len(clean_number) >= 10:
            return f'({clean_number[:3]}) {clean_number[3:6]}-{clean_number[6:]}'
        else:
            return clean_number
    
    def validate_phone_number(self) -> Dict[str, Any]:
        """
        Enhanced validation for phone number format with detailed results
        
        Returns:
            dict: Validation results with details
        """
        if not self.lead_phone_number:
            return {
                'valid': False,
                'reason': 'No phone number provided',
                'format': None,
                'suggestions': ['Set LEAD_PHONE_NUMBER environment variable']
            }
            
        clean_number = re.sub(r'[^\d]', '', self.lead_phone_number)
        
        validation_result = {
            'valid': False,
            'reason': '',
            'format': None,
            'suggestions': [],
            'clean_number': clean_number
        }
        
        # Check minimum length
        if len(clean_number) < 10:
            validation_result.update({
                'reason': f'Too short: {len(clean_number)} digits (minimum 10)',
                'suggestions': ['Ensure the number includes area code and phone number']
            })
            return validation_result
        
        # Check maximum length
        if len(clean_number) > 15:
            validation_result.update({
                'reason': f'Too long: {len(clean_number)} digits (maximum 15)',
                'suggestions': ['Remove any extra digits or country codes']
            })
            return validation_result
        
        # Check for specific formats
        for format_name, pattern in self.PHONE_PATTERNS.items():
            if pattern.match(clean_number):
                validation_result.update({
                    'valid': True,
                    'format': format_name,
                    'reason': f'Valid {format_name} phone number'
                })
                return validation_result
        
        # If no specific pattern matches but length is valid
        validation_result.update({
            'valid': True,
            'format': 'generic_international',
            'reason': 'Valid international phone number format',
            'suggestions': ['Verify country code is correct']
        })
        
        return validation_result
    
    def is_brazilian_number(self) -> bool:
        """
        Check if the phone number is a Brazilian number
        
        Returns:
            bool: True if Brazilian number, False otherwise
        """
        if not self.lead_phone_number:
            return False
            
        clean_number = re.sub(r'[^\d]', '', self.lead_phone_number)
        return self.PHONE_PATTERNS['brazilian'].match(clean_number) is not None
    
    def is_us_number(self) -> bool:
        """
        Check if the phone number is a US number
        
        Returns:
            bool: True if US number, False otherwise
        """
        if not self.lead_phone_number:
            return False
            
        clean_number = re.sub(r'[^\d]', '', self.lead_phone_number)
        return self.PHONE_PATTERNS['us'].match(clean_number) is not None
    
    def get_whatsapp_url(self, message: str = '') -> str:
        """
        Generate a WhatsApp URL for the configured phone number
        
        Args:
            message: Optional message to include
            
        Returns:
            str: WhatsApp API URL
        """
        whatsapp_number = self.get_formatted_phone_number('whatsapp')
        base_url = f'https://api.whatsapp.com/send/?phone={whatsapp_number}'
        
        if message:
            # URL encode message for safety
            import urllib.parse
            encoded_message = urllib.parse.quote(message)
            base_url += f'&text={encoded_message}'
            
        return base_url
    
    def export_config(self) -> Dict[str, Any]:
        """
        Export configuration as dictionary for use in other systems
        
        Returns:
            dict: Configuration data
        """
        validation = self.validate_phone_number()
        
        return {
            'phone_number': {
                'raw': self.lead_phone_number,
                'clean': validation.get('clean_number', ''),
                'formatted': {
                    'standard': self.get_formatted_phone_number('standard'),
                    'international': self.get_formatted_phone_number('international'),
                    'whatsapp': self.get_formatted_phone_number('whatsapp')
                }
            },
            'validation': validation,
            'whatsapp_url': self.get_whatsapp_url(),
            'metadata': {
                'is_brazilian': self.is_brazilian_number(),
                'is_us': self.is_us_number(),
                'default_used': self.lead_phone_number == self.DEFAULT_LEAD_PHONE
            }
        }

# Usage example and testing
if __name__ == '__main__':
    # Check if we're in production mode (reduce sensitive output)
    is_production = os.getenv('ENVIRONMENT') == 'production'
    
    print('=' * 60)
    print('🧪 CONFIGURAÇÃO AVANÇADA - TESTE E VALIDAÇÃO')
    print('=' * 60)
    
    print('\n📋 Production Mode (requires LEAD_PHONE_NUMBER env var)')
    print('-' * 50)
    try:
        config_prod = Config(require_env_var=True)
        config_data = config_prod.export_config()
        
        print(f'✅ Lead phone: {config_prod._mask_phone_number(config_prod.get_lead_phone_number())}')
        
        if not is_production:
            print(f'📱 WhatsApp URL: {config_prod.get_whatsapp_url("Teste de mensagem")}')
        else:
            print('📱 WhatsApp URL: [masked in production]')
            
        print(f'🇧🇷 Brazilian number: {config_prod.is_brazilian_number()}')
        print(f'🇺🇸 US number: {config_prod.is_us_number()}')
        
        validation = config_prod.validate_phone_number()
        print(f'✅ Validation: {validation["valid"]} - {validation["reason"]}')
        
        if validation['suggestions']:
            print(f'💡 Suggestions: {", ".join(validation["suggestions"])}')
            
    except ValueError as e:
        print(f'❌ Production Error: {e}')
        
        print('\n🔧 Development Mode (uses default if env var missing)')
        print('-' * 50)
        config_dev = Config(require_env_var=False)
        config_data = config_dev.export_config()
        
        print(f'📞 Lead phone: {config_dev._mask_phone_number(config_dev.get_lead_phone_number())}')
        
        if not is_production:
            print(f'📝 Standard format: {config_dev.get_formatted_phone_number("standard")}')
            print(f'🌍 International format: {config_dev.get_formatted_phone_number("international")}')
            print(f'🔢 Digits only: {config_dev._mask_phone_number(config_dev.get_formatted_phone_number("digits_only"))}')
            print(f'📱 WhatsApp format: {config_dev._mask_phone_number(config_dev.get_formatted_phone_number("whatsapp"))}')
            print(f'\n📱 WhatsApp URL: {config_dev.get_whatsapp_url("Mensagem de teste")}')
        else:
            print('📝 Format details: [masked in production]')
            print('📱 WhatsApp URL: [masked in production]')
        
        validation = config_dev.validate_phone_number()
        print(f'✅ Validation: {validation["valid"]} - {validation["reason"]}')
        
        print(f'🇧🇷 Brazilian number: {config_dev.is_brazilian_number()}')
        print(f'🇺🇸 US number: {config_dev.is_us_number()}')
        
        if validation['suggestions']:
            print(f'💡 Suggestions: {", ".join(validation["suggestions"])}')
    
    print('\n' + '=' * 60)
    print('🎯 TESTE COMPLETO - CONFIGURAÇÃO VALIDADA')
    print('=' * 60)
