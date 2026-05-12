"""
Sibane ECD Academy — Django Admin configuration
Registers all models with useful list_display and filters.
"""
from django.contrib import admin
from .models import (
    Student, Staff, Attendance, Payment, MealRecord, Expense,
    InventoryItem, InventoryTransaction, Book, BookBorrow,
    Timetable, SupervisorVisit, SalesContribution
)

# ── Customise admin site headers ──────────────────────────────
admin.site.site_header = 'Sibane ECD Academy — Admin'
admin.site.site_title  = 'Sibane Admin'
admin.site.index_title = 'Management Portal'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display   = ['full_name', 'class_level', 'age', 'gender', 'parent_name', 'parent_contact', 'is_active']
    list_filter    = ['class_level', 'gender', 'is_active']
    search_fields  = ['first_name', 'last_name', 'parent_name', 'parent_contact']
    list_per_page  = 30


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'role', 'contact', 'email', 'join_date', 'is_active']
    list_filter   = ['role', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display  = ['student', 'date', 'status', 'notes']
    list_filter   = ['status', 'student__class_level']
    date_hierarchy = 'date'
    search_fields = ['student__first_name', 'student__last_name']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ['student', 'payment_type', 'amount', 'date', 'reference']
    list_filter   = ['payment_type']
    date_hierarchy = 'date'
    search_fields = ['student__first_name', 'student__last_name', 'reference']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display  = ['category', 'description', 'amount', 'date', 'receipt_number']
    list_filter   = ['category']
    date_hierarchy = 'date'


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'unit', 'minimum_quantity', 'is_low_stock', 'last_updated']
    list_filter  = ['category']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'total_copies', 'available_copies']
    search_fields = ['title', 'author', 'isbn']


@admin.register(BookBorrow)
class BookBorrowAdmin(admin.ModelAdmin):
    list_display = ['book', 'student', 'borrow_date', 'due_date', 'return_date', 'is_overdue']
    list_filter  = ['return_date']


@admin.register(SupervisorVisit)
class SupervisorVisitAdmin(admin.ModelAdmin):
    list_display = ['date', 'week_number', 'class_visited', 'supervisor']
    list_filter  = ['week_number', 'class_visited']
    date_hierarchy = 'date'


# Register remaining models simply
admin.site.register(MealRecord)
admin.site.register(InventoryTransaction)
admin.site.register(Timetable)
admin.site.register(SalesContribution)
