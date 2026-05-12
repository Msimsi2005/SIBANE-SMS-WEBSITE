"""
Sibane ECD Academy — Forms
Bootstrap 5 styled forms for all models.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import (
    Student, Staff, Attendance, Payment, MealRecord, Expense,
    InventoryItem, InventoryTransaction, Book, BookBorrow,
    Timetable, SupervisorVisit, SalesContribution
)

# Reusable widget class for Bootstrap
BS = 'form-control'
BS_SEL = 'form-select'
BS_CHK = 'form-check-input'


class LoginForm(AuthenticationForm):
    """Styled login form."""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': BS, 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': BS, 'placeholder': 'Password'}))


# ─────────────────────────────────────────────────────────────
#  STUDENT
# ─────────────────────────────────────────────────────────────
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'class_level', 'parent_name', 'parent_contact',
            'parent_email', 'address', 'is_active',
        ]
        widgets = {
            'first_name':     forms.TextInput(attrs={'class': BS}),
            'last_name':      forms.TextInput(attrs={'class': BS}),
            'date_of_birth':  forms.DateInput(attrs={'class': BS, 'type': 'date'}),
            'gender':         forms.Select(attrs={'class': BS_SEL}),
            'class_level':    forms.Select(attrs={'class': BS_SEL}),
            'parent_name':    forms.TextInput(attrs={'class': BS}),
            'parent_contact': forms.TextInput(attrs={'class': BS}),
            'parent_email':   forms.EmailInput(attrs={'class': BS}),
            'address':        forms.Textarea(attrs={'class': BS, 'rows': 3}),
            'is_active':      forms.CheckboxInput(attrs={'class': BS_CHK}),
        }


# ─────────────────────────────────────────────────────────────
#  STAFF
# ─────────────────────────────────────────────────────────────
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'first_name', 'last_name', 'role', 'contact',
            'email', 'qualification', 'join_date', 'is_active',
        ]
        widgets = {
            'first_name':    forms.TextInput(attrs={'class': BS}),
            'last_name':     forms.TextInput(attrs={'class': BS}),
            'role':          forms.Select(attrs={'class': BS_SEL}),
            'contact':       forms.TextInput(attrs={'class': BS}),
            'email':         forms.EmailInput(attrs={'class': BS}),
            'qualification': forms.TextInput(attrs={'class': BS}),
            'join_date':     forms.DateInput(attrs={'class': BS, 'type': 'date'}),
            'is_active':     forms.CheckboxInput(attrs={'class': BS_CHK}),
        }


# ─────────────────────────────────────────────────────────────
#  ATTENDANCE
# ─────────────────────────────────────────────────────────────
class AttendanceFilterForm(forms.Form):
    """Filter form for attendance list."""
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': BS, 'type': 'date'})
    )
    class_level = forms.ChoiceField(
        required=False,
        choices=[('', 'All Classes')] + [
            ('toddlers', 'Toddlers'), ('ecd_a', 'ECD A'), ('ecd_b', 'ECD B')
        ],
        widget=forms.Select(attrs={'class': BS_SEL})
    )


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status', 'notes']
        widgets = {
            'student': forms.Select(attrs={'class': BS_SEL}),
            'date':    forms.DateInput(attrs={'class': BS, 'type': 'date'}),
            'status':  forms.Select(attrs={'class': BS_SEL}),
            'notes':   forms.TextInput(attrs={'class': BS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active students
        self.fields['student'].queryset = Student.objects.filter(is_active=True)


# ─────────────────────────────────────────────────────────────
#  PAYMENT
# ─────────────────────────────────────────────────────────────
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'payment_type', 'amount', 'date', 'reference', 'notes']
        widgets = {
            'student':      forms.Select(attrs={'class': BS_SEL}),
            'payment_type': forms.Select(attrs={'class': BS_SEL}),
            'amount':       forms.NumberInput(attrs={'class': BS, 'step': '0.01'}),
            'date':         forms.DateInput(attrs={'class': BS, 'type': 'date'}),
            'reference':    forms.TextInput(attrs={'class': BS}),
            'notes':        forms.TextInput(attrs={'class': BS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(is_active=True)


# ─────────────────────────────────────────────────────────────
#  MEALS
# ─────────────────────────────────────────────────────────────
class MealRecordForm(forms.ModelForm):
    class Meta:
        model = MealRecord
        fields = ['date', 'class_level', 'breakfast_count', 'lunch_count', 'snack_count', 'notes']
        widgets = {
            'date':            forms.DateInput(attrs={'class': BS, 'type': 'date'}),
            'class_level':     forms.Select(attrs={'class': BS_SEL}),
            'breakfast_count': forms.NumberInput(attrs={'class': BS}),
            'lunch_count':     forms.NumberInput(attrs={'class': BS}),
            'snack_count':     forms.NumberInput(attrs={'class': BS}),
            'notes':           forms.Textarea(attrs={'class': BS, 'rows': 2}),
        }


# ─────────────────────────────────────────────────────────────
#  EXPENSES
# ─────────────────────────────────────────────────────────────
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'date', 'receipt_number']
        widgets = {
            'category':       forms.Select(attrs={'class': BS_SEL}),
            'description':    forms.TextInput(attrs={'class': BS}),
            'amount':         forms.NumberInput(attrs={'class': BS, 'step': '0.01'}),
            'date':           forms.DateInput(attrs={'class': BS, 'type': 'date'}),
            'receipt_number': forms.TextInput(attrs={'class': BS}),
        }


# ─────────────────────────────────────────────────────────────
#  INVENTORY
# ─────────────────────────────────────────────────────────────
class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'quantity', 'unit', 'minimum_quantity', 'notes']
        widgets = {
            'name':             forms.TextInput(attrs={'class': BS}),
            'category':         forms.Select(attrs={'class': BS_SEL}),
            'quantity':         forms.NumberInput(attrs={'class': BS, 'step': '0.01'}),
            'unit':             forms.TextInput(attrs={'class': BS}),
            'minimum_quantity': forms.NumberInput(attrs={'class': BS, 'step': '0.01'}),
            'notes':            forms.Textarea(attrs={'class': BS, 'rows': 2}),
        }


class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = ['item', 'transaction_type', 'quantity', 'date', 'notes']
        widgets = {
            'item':             forms.Select(attrs={'class': BS_SEL}),
            'transaction_type': forms.Select(attrs={'class': BS_SEL}),
            'quantity':         forms.NumberInput(attrs={'class': BS, 'step': '0.01'}),
            'date':             forms.DateInput(attrs={'class': BS, 'type': 'date'}),
            'notes':            forms.TextInput(attrs={'class': BS}),
        }


# ─────────────────────────────────────────────────────────────
#  LIBRARY
# ─────────────────────────────────────────────────────────────
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'total_copies', 'available_copies']
        widgets = {
            'title':            forms.TextInput(attrs={'class': BS}),
            'author':           forms.TextInput(attrs={'class': BS}),
            'isbn':             forms.TextInput(attrs={'class': BS}),
            'category':         forms.TextInput(attrs={'class': BS}),
            'total_copies':     forms.NumberInput(attrs={'class': BS}),
            'available_copies': forms.NumberInput(attrs={'class': BS}),
        }


class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = BookBorrow
        fields = ['book', 'student', 'borrow_date', 'due_date', 'notes']
        widgets = {
            'book':        forms.Select(attrs={'class': BS_SEL}),
            'student':     forms.Select(attrs={'class': BS_SEL}),
            'borrow_date': forms.DateInput(attrs={'class': BS, 'type': 'date'}),
            'due_date':    forms.DateInput(attrs={'class': BS, 'type': 'date'}),
            'notes':       forms.TextInput(attrs={'class': BS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(is_active=True)
        # Only show books with available copies
        self.fields['book'].queryset = Book.objects.filter(available_copies__gt=0)


# ─────────────────────────────────────────────────────────────
#  TIMETABLE
# ─────────────────────────────────────────────────────────────
class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['class_level', 'day', 'period', 'subject', 'teacher']
        widgets = {
            'class_level': forms.Select(attrs={'class': BS_SEL}),
            'day':         forms.Select(attrs={'class': BS_SEL}),
            'period':      forms.Select(attrs={'class': BS_SEL}),
            'subject':     forms.TextInput(attrs={'class': BS}),
            'teacher':     forms.Select(attrs={'class': BS_SEL}),
        }


# ─────────────────────────────────────────────────────────────
#  SUPERVISOR VISIT
# ─────────────────────────────────────────────────────────────
class SupervisorVisitForm(forms.ModelForm):
    class Meta:
        model = SupervisorVisit
        fields = ['date', 'supervisor', 'class_visited', 'week_number', 'notes', 'recommendations']
        widgets = {
            'date':            forms.DateInput(attrs={'class': BS, 'type': 'date'}),
            'supervisor':      forms.Select(attrs={'class': BS_SEL}),
            'class_visited':   forms.Select(attrs={'class': BS_SEL}),
            'week_number':     forms.Select(attrs={'class': BS_SEL}),
            'notes':           forms.Textarea(attrs={'class': BS, 'rows': 4}),
            'recommendations': forms.Textarea(attrs={'class': BS, 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supervisor'].queryset = Staff.objects.filter(
            role='supervisor', is_active=True
        )


# ─────────────────────────────────────────────────────────────
#  SALES & CONTRIBUTIONS
# ─────────────────────────────────────────────────────────────
class SalesContributionForm(forms.ModelForm):
    class Meta:
        model = SalesContribution
        fields = ['student', 'contribution_type', 'description', 'amount', 'date']
        widgets = {
            'student':           forms.Select(attrs={'class': BS_SEL}),
            'contribution_type': forms.Select(attrs={'class': BS_SEL}),
            'description':       forms.TextInput(attrs={'class': BS}),
            'amount':            forms.NumberInput(attrs={'class': BS, 'step': '0.01'}),
            'date':              forms.DateInput(attrs={'class': BS, 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(is_active=True)
        self.fields['student'].required = False
