"""
Summary generation utility for job offers.

This module provides functions to generate concise, factual summaries
for job offers. Summaries are generated once and stored in the database.
"""

import re
from typing import Optional


def is_meaningful_description(description: Optional[str], min_length: int = 50) -> bool:
    """
    Check if a description is meaningful enough to use as a summary.
    
    Args:
        description: The description text to check
        min_length: Minimum length to consider meaningful
        
    Returns:
        True if description is meaningful, False otherwise
    """
    if not description:
        return False
    
    # Remove extra whitespace
    cleaned = ' '.join(description.split())
    
    # Check minimum length
    if len(cleaned) < min_length:
        return False
    
    # Check if it's just navigation text or common non-informative content
    non_informative_patterns = [
        r'^(menu|kontakt|o nas|rejestracja|bip|intranet)',
        r'cookie',
        r'polityka prywatności',
        r'regulamin',
    ]
    
    cleaned_lower = cleaned.lower()
    for pattern in non_informative_patterns:
        if re.search(pattern, cleaned_lower):
            return False
    
    return True


def generate_summary(title: str, description: Optional[str], facility_name: str, city: str) -> str:
    """
    Generate a concise, factual summary for a job offer.
    
    If a meaningful description exists, it's used as the summary.
    Otherwise, a summary is generated from available information.
    
    Args:
        title: Job title
        description: Full job description (if available)
        facility_name: Name of the medical facility
        city: City where the job is located
        
    Returns:
        A concise summary (typically 100-200 characters)
    """
    # If we have a meaningful description, use the first part of it
    if is_meaningful_description(description):
        # Take first 2-3 sentences or first 200 characters, whichever is shorter
        cleaned_desc = ' '.join(description.split())
        
        # Try to find sentence boundaries
        sentences = re.split(r'[.!?]+\s+', cleaned_desc)
        if len(sentences) >= 2:
            # Take first 2-3 sentences
            summary = '. '.join(sentences[:3])
            if summary and not summary.endswith('.'):
                summary += '.'
        else:
            # No clear sentences, take first 200 chars
            summary = cleaned_desc[:200]
            # Try to cut at word boundary
            if len(cleaned_desc) > 200:
                last_space = summary.rfind(' ')
                if last_space > 150:  # Only if we have enough content
                    summary = summary[:last_space]
                summary += '...'
        
        return summary.strip()
    
    # Generate summary from available information
    # Format: "Position at Facility in City"
    parts = []
    
    # Extract role/position from title
    role_keywords = {
        'pielęgniarka': 'Pielęgniarka',
        'pielęgniarz': 'Pielęgniarz',
        'położna': 'Położna',
        'położny': 'Położny',
        'lekarz': 'Lekarz',
        'fizjoterapeuta': 'Fizjoterapeuta',
        'fizjoterapeutka': 'Fizjoterapeutka',
        'ratownik': 'Ratownik medyczny',
        'specjalista': 'Specjalista',
    }
    
    title_lower = title.lower()
    role = None
    for keyword, label in role_keywords.items():
        if keyword in title_lower:
            role = label
            break
    
    if role:
        parts.append(role)
    else:
        # Fallback: use first few words of title
        title_words = title.split()[:3]
        parts.append(' '.join(title_words))
    
    # Add facility
    if facility_name and facility_name.lower() not in ['medicover', 'lux med', 'szpital']:
        parts.append(f"w {facility_name}")
    else:
        parts.append("w placówce medycznej")
    
    # Add city
    if city:
        parts.append(f"w {city}")
    
    summary = ' '.join(parts) + '.'
    
    # If we have some description, add a brief note
    if description and len(description.strip()) > 20:
        # Take first meaningful sentence or phrase
        desc_cleaned = ' '.join(description.split()[:15])
        if len(desc_cleaned) < 100:
            summary += f" {desc_cleaned}..."
        else:
            summary += f" {desc_cleaned[:100]}..."
    
    return summary.strip()


def extract_summary(title: str, description: Optional[str], facility_name: str, city: str) -> str:
    """
    Extract or generate a summary for a job offer.
    
    This is the main entry point for summary generation.
    It decides whether to use existing description or generate a new one.
    
    Args:
        title: Job title
        description: Full job description (if available)
        facility_name: Name of the medical facility
        city: City where the job is located
        
    Returns:
        A concise summary suitable for display on job cards
    """
    return generate_summary(title, description, facility_name, city)
