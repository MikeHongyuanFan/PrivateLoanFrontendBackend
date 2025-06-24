#!/usr/bin/env python
"""
Test script for Celery tasks related to Active Loan alerts.

This script can be used to manually trigger the Celery tasks for testing purposes.
Run this script from the Django project root directory.
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_backend.settings')
django.setup()

from applications.tasks import (
    send_active_loan_payment_reminders,
    send_active_loan_expiry_warnings,
    send_critical_expiry_alerts,
    send_immediate_active_loan_alert,
    cleanup_old_active_loan_notifications
)
from applications.models import ActiveLoan
from django.contrib.auth import get_user_model

User = get_user_model()

def test_payment_reminders():
    """Test the payment reminders task."""
    print("Testing payment reminders task...")
    result = send_active_loan_payment_reminders.delay()
    print(f"Task ID: {result.id}")
    print("Task submitted successfully!")

def test_expiry_warnings():
    """Test the expiry warnings task."""
    print("Testing expiry warnings task...")
    result = send_active_loan_expiry_warnings.delay()
    print(f"Task ID: {result.id}")
    print("Task submitted successfully!")

def test_critical_alerts():
    """Test the critical alerts task."""
    print("Testing critical alerts task...")
    result = send_critical_expiry_alerts.delay()
    print(f"Task ID: {result.id}")
    print("Task submitted successfully!")

def test_immediate_alert(loan_id, alert_type="manual", message=None):
    """Test the immediate alert task."""
    print(f"Testing immediate alert task for loan {loan_id}...")
    result = send_immediate_active_loan_alert.delay(loan_id, alert_type, message)
    print(f"Task ID: {result.id}")
    print("Task submitted successfully!")

def test_cleanup():
    """Test the cleanup task."""
    print("Testing cleanup task...")
    result = cleanup_old_active_loan_notifications.delay()
    print(f"Task ID: {result.id}")
    print("Task submitted successfully!")

def list_active_loans():
    """List all active loans for reference."""
    print("Active Loans:")
    print("-" * 50)
    loans = ActiveLoan.objects.filter(is_active=True).select_related('application')
    for loan in loans:
        print(f"ID: {loan.id}")
        print(f"Application: {loan.application.reference_number}")
        print(f"Expiry Date: {loan.loan_expiry_date}")
        print(f"Interest Payments: {loan.interest_payments_required}")
        print("-" * 30)

def main():
    """Main function to run tests."""
    print("Active Loan Celery Tasks Test Script")
    print("=" * 50)
    
    while True:
        print("\nAvailable tests:")
        print("1. Test Payment Reminders")
        print("2. Test Expiry Warnings")
        print("3. Test Critical Alerts")
        print("4. Test Immediate Alert")
        print("5. Test Cleanup")
        print("6. List Active Loans")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            test_payment_reminders()
        elif choice == "2":
            test_expiry_warnings()
        elif choice == "3":
            test_critical_alerts()
        elif choice == "4":
            loan_id = input("Enter loan ID: ").strip()
            alert_type = input("Enter alert type (payment/expiry/manual): ").strip() or "manual"
            message = input("Enter custom message (optional): ").strip() or None
            test_immediate_alert(loan_id, alert_type, message)
        elif choice == "5":
            test_cleanup()
        elif choice == "6":
            list_active_loans()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 