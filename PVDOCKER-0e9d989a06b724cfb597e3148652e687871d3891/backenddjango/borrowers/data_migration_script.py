"""
Data Migration Script for Unified Field Structure

This script helps migrate existing data from legacy fields to the new unified field structure
for both Borrower and Guarantor models.

Usage:
    python manage.py shell
    exec(open('borrowers/migrations/data_migration_script.py').read())
"""

from borrowers.models import Borrower, Guarantor
from django.db import transaction
import re


def migrate_borrower_phone_fields():
    """
    Migrate phone field to home_phone for borrowers
    """
    print("Migrating borrower phone fields...")
    
    borrowers_with_phone = Borrower.objects.filter(phone__isnull=False).exclude(phone='')
    count = 0
    
    for borrower in borrowers_with_phone:
        if not borrower.home_phone:  # Only migrate if home_phone is empty
            borrower.home_phone = borrower.phone
            borrower.save()
            count += 1
            print(f"Migrated phone for borrower {borrower.id}: {borrower.phone}")
    
    print(f"Migrated {count} borrower phone records")


def migrate_borrower_job_title_to_occupation():
    """
    Migrate job_title field to occupation for borrowers
    """
    print("Migrating borrower job_title to occupation...")
    
    borrowers_with_job_title = Borrower.objects.filter(job_title__isnull=False).exclude(job_title='')
    count = 0
    
    for borrower in borrowers_with_job_title:
        if not borrower.occupation:  # Only migrate if occupation is empty
            borrower.occupation = borrower.job_title
            borrower.save()
            count += 1
            print(f"Migrated job_title for borrower {borrower.id}: {borrower.job_title}")
    
    print(f"Migrated {count} borrower job_title records")


def migrate_guarantor_address_fields():
    """
    Migrate legacy address field to structured address fields for guarantors
    Note: This is a basic migration - address parsing would require more sophisticated logic
    """
    print("Migrating guarantor address fields...")
    
    guarantors_with_address = Guarantor.objects.filter(address__isnull=False).exclude(address='')
    count = 0
    
    for guarantor in guarantors_with_address:
        # Only migrate if structured address fields are empty
        if not any([
            guarantor.address_unit,
            guarantor.address_street_no,
            guarantor.address_street_name,
            guarantor.address_suburb,
            guarantor.address_state,
            guarantor.address_postcode
        ]):
            # Basic address parsing - this is a simplified example
            # In production, you might want to use a proper address parsing library
            address_parts = guarantor.address.split(',')
            
            if len(address_parts) >= 3:
                # Assume format: "123 Main St, Sydney, NSW 2000"
                street_part = address_parts[0].strip()
                suburb_part = address_parts[1].strip()
                state_postcode_part = address_parts[2].strip()
                
                # Extract street number and name
                street_match = re.match(r'(\d+)\s+(.+)', street_part)
                if street_match:
                    guarantor.address_street_no = street_match.group(1)
                    guarantor.address_street_name = street_match.group(2)
                
                guarantor.address_suburb = suburb_part
                
                # Extract state and postcode
                state_postcode_match = re.match(r'([A-Z]+)\s+(\d+)', state_postcode_part)
                if state_postcode_match:
                    guarantor.address_state = state_postcode_match.group(1)
                    guarantor.address_postcode = state_postcode_match.group(2)
                
                guarantor.save()
                count += 1
                print(f"Migrated address for guarantor {guarantor.id}: {guarantor.address}")
    
    print(f"Migrated {count} guarantor address records")


def validate_unified_structure():
    """
    Validate that the unified field structure is working correctly
    """
    print("Validating unified field structure...")
    
    # Check borrowers
    borrower_count = Borrower.objects.count()
    borrowers_with_title = Borrower.objects.filter(title__isnull=False).exclude(title='').count()
    borrowers_with_occupation = Borrower.objects.filter(occupation__isnull=False).exclude(occupation='').count()
    borrowers_with_structured_address = Borrower.objects.filter(
        address_street_no__isnull=False
    ).exclude(address_street_no='').count()
    
    print(f"Borrowers:")
    print(f"  Total: {borrower_count}")
    print(f"  With title: {borrowers_with_title}")
    print(f"  With occupation: {borrowers_with_occupation}")
    print(f"  With structured address: {borrowers_with_structured_address}")
    
    # Check guarantors
    guarantor_count = Guarantor.objects.count()
    guarantors_with_title = Guarantor.objects.filter(title__isnull=False).exclude(title='').count()
    guarantors_with_occupation = Guarantor.objects.filter(occupation__isnull=False).exclude(occupation='').count()
    guarantors_with_structured_address = Guarantor.objects.filter(
        address_street_no__isnull=False
    ).exclude(address_street_no='').count()
    
    print(f"Guarantors:")
    print(f"  Total: {guarantor_count}")
    print(f"  With title: {guarantors_with_title}")
    print(f"  With occupation: {guarantors_with_occupation}")
    print(f"  With structured address: {guarantors_with_structured_address}")


def run_full_migration():
    """
    Run the complete migration process
    """
    print("Starting unified field structure migration...")
    print("=" * 50)
    
    try:
        with transaction.atomic():
            # Migrate borrower fields
            migrate_borrower_phone_fields()
            migrate_borrower_job_title_to_occupation()
            
            # Migrate guarantor fields
            migrate_guarantor_address_fields()
            
            # Validate the migration
            validate_unified_structure()
            
        print("=" * 50)
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        raise


def show_migration_preview():
    """
    Show what would be migrated without actually performing the migration
    """
    print("Migration Preview - No changes will be made")
    print("=" * 50)
    
    # Preview borrower phone migration
    borrowers_with_phone = Borrower.objects.filter(phone__isnull=False).exclude(phone='')
    borrowers_needing_phone_migration = [
        b for b in borrowers_with_phone if not b.home_phone
    ]
    print(f"Borrowers needing phone migration: {len(borrowers_needing_phone_migration)}")
    
    # Preview borrower job_title migration
    borrowers_with_job_title = Borrower.objects.filter(job_title__isnull=False).exclude(job_title='')
    borrowers_needing_job_title_migration = [
        b for b in borrowers_with_job_title if not b.occupation
    ]
    print(f"Borrowers needing job_title migration: {len(borrowers_needing_job_title_migration)}")
    
    # Preview guarantor address migration
    guarantors_with_address = Guarantor.objects.filter(address__isnull=False).exclude(address='')
    guarantors_needing_address_migration = [
        g for g in guarantors_with_address if not any([
            g.address_unit, g.address_street_no, g.address_street_name,
            g.address_suburb, g.address_state, g.address_postcode
        ])
    ]
    print(f"Guarantors needing address migration: {len(guarantors_needing_address_migration)}")
    
    print("=" * 50)
    print("To run the actual migration, call: run_full_migration()")


# Main execution
if __name__ == "__main__":
    print("Unified Field Structure Migration Script")
    print("Available functions:")
    print("- show_migration_preview(): Preview what would be migrated")
    print("- run_full_migration(): Run the complete migration")
    print("- migrate_borrower_phone_fields(): Migrate phone fields only")
    print("- migrate_borrower_job_title_to_occupation(): Migrate job_title fields only")
    print("- migrate_guarantor_address_fields(): Migrate address fields only")
    print("- validate_unified_structure(): Validate the current state")
    print()
    print("Run show_migration_preview() to see what would be migrated") 