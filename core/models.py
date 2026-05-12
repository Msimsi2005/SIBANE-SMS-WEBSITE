"""
Sibane ECD Academy — Database Models
All models are in a single file for simplicity.
"""
from django.db import models
from django.contrib.auth.models import User
from datetime import date

# ─────────────────────────────────────────────────────────────
#  SHARED CONSTANTS
# ─────────────────────────────────────────────────────────────
CLASS_LEVELS = [
    ('toddlers', 'Toddlers'),
    ('ecd_a',    'ECD A'),
    ('ecd_b',    'ECD B'),
]

STAFF_ROLES = [
    ('teacher',      'Teacher (TR)'),
    ('general_hand', 'General Hand'),
    ('supervisor',   'Supervisor'),
    ('admin',        'Admin'),
    ('cook',         'Cook'),
    ('driver',       'Driver'),
]

DAYS_OF_WEEK = [
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
]


# ─────────────────────────────────────────────────────────────
#  STUDENT
# ─────────────────────────────────────────────────────────────
class Student(models.Model):
    first_name     = models.CharField(max_length=100)
    last_name      = models.CharField(max_length=100)
    date_of_birth  = models.DateField()
    gender         = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    class_level    = models.CharField(max_length=20, choices=CLASS_LEVELS)
    parent_name    = models.CharField(max_length=200)
    parent_contact = models.CharField(max_length=30)
    parent_email   = models.EmailField(blank=True)
    address        = models.TextField(blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    is_active      = models.BooleanField(default=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def total_paid(self):
        from django.db.models import Sum
        result = self.payments.aggregate(total=Sum('amount'))
        return result['total'] or 0


# ─────────────────────────────────────────────────────────────
#  STAFF
# ─────────────────────────────────────────────────────────────
class Staff(models.Model):
    # Link to Django user account (optional — for login access)
    user          = models.OneToOneField(User, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='staff_profile')
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    role          = models.CharField(max_length=20, choices=STAFF_ROLES)
    contact       = models.CharField(max_length=30)
    email         = models.EmailField(blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    join_date     = models.DateField()
    is_active     = models.BooleanField(default=True)

    class Meta:
        ordering = ['role', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.get_role_display()}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# ─────────────────────────────────────────────────────────────
#  ATTENDANCE
# ─────────────────────────────────────────────────────────────
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent',  'Absent'),
        ('late',    'Late'),
    ]
    student     = models.ForeignKey(Student, on_delete=models.CASCADE,
                                    related_name='attendance_records')
    date        = models.DateField()
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes       = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('student', 'date')  # one record per student per day
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} | {self.date} | {self.get_status_display()}"


# ─────────────────────────────────────────────────────────────
#  PAYMENT
# ─────────────────────────────────────────────────────────────
class Payment(models.Model):
    PAYMENT_TYPES = [
        ('school_fees', 'School Fees'),
        ('levy',        'Levy'),
        ('bus_fare',    'Bus Fare'),
        ('uniform',     'Uniform'),
        ('other',       'Other'),
    ]
    student      = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount       = models.DecimalField(max_digits=10, decimal_places=2)
    date         = models.DateField()
    recorded_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reference    = models.CharField(max_length=100, blank=True, help_text='Receipt / reference no.')
    notes        = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} | {self.get_payment_type_display()} | ${self.amount}"


# ─────────────────────────────────────────────────────────────
#  MEAL RECORD
# ─────────────────────────────────────────────────────────────
class MealRecord(models.Model):
    date            = models.DateField()
    class_level     = models.CharField(max_length=20, choices=CLASS_LEVELS)
    breakfast_count = models.IntegerField(default=0)
    lunch_count     = models.IntegerField(default=0)
    snack_count     = models.IntegerField(default=0)
    notes           = models.TextField(blank=True)
    recorded_by     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('date', 'class_level')
        ordering = ['-date']

    def __str__(self):
        return f"Meals {self.date} — {self.get_class_level_display()}"


# ─────────────────────────────────────────────────────────────
#  EXPENSE
# ─────────────────────────────────────────────────────────────
class Expense(models.Model):
    CATEGORIES = [
        ('fuel',        'Fuel'),
        ('food',        'Food'),
        ('general',     'General'),
        ('maintenance', 'Maintenance'),
        ('utilities',   'Utilities'),
        ('salaries',    'Salaries'),
        ('other',       'Other'),
    ]
    category       = models.CharField(max_length=20, choices=CATEGORIES)
    description    = models.CharField(max_length=300)
    amount         = models.DecimalField(max_digits=10, decimal_places=2)
    date           = models.DateField()
    recorded_by    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    receipt_number = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_category_display()} | ${self.amount} | {self.date}"


# ─────────────────────────────────────────────────────────────
#  INVENTORY
# ─────────────────────────────────────────────────────────────
class InventoryItem(models.Model):
    CATEGORIES = [
        ('furniture',  'Furniture'),
        ('food',       'Food / Groceries'),
        ('stationery', 'Stationery'),
        ('cleaning',   'Cleaning Supplies'),
        ('equipment',  'Equipment'),
        ('toys',       'Toys / Learning Materials'),
        ('other',      'Other'),
    ]
    name             = models.CharField(max_length=200)
    category         = models.CharField(max_length=20, choices=CATEGORIES)
    quantity         = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit             = models.CharField(max_length=50, default='units')
    minimum_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           help_text='Alert when stock falls below this')
    notes            = models.TextField(blank=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_quantity


class InventoryTransaction(models.Model):
    TRANS_TYPES = [
        ('in',         'Stock In'),
        ('out',        'Stock Out'),
        ('adjustment', 'Adjustment'),
    ]
    item             = models.ForeignKey(InventoryItem, on_delete=models.CASCADE,
                                         related_name='transactions')
    transaction_type = models.CharField(max_length=15, choices=TRANS_TYPES)
    quantity         = models.DecimalField(max_digits=10, decimal_places=2)
    date             = models.DateField()
    notes            = models.CharField(max_length=300, blank=True)
    recorded_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        # Automatically update item quantity on transaction save
        if self.transaction_type == 'in':
            self.item.quantity += self.quantity
        elif self.transaction_type == 'out':
            self.item.quantity = max(0, self.item.quantity - self.quantity)
        else:
            # Adjustment: set absolute value
            self.item.quantity = self.quantity
        self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name} | {self.transaction_type} | {self.quantity}"


# ─────────────────────────────────────────────────────────────
#  LIBRARY
# ─────────────────────────────────────────────────────────────
class Book(models.Model):
    title            = models.CharField(max_length=200)
    author           = models.CharField(max_length=200)
    isbn             = models.CharField(max_length=20, blank=True)
    category         = models.CharField(max_length=100, blank=True)
    total_copies     = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author}"


class BookBorrow(models.Model):
    book         = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    student      = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='borrows')
    borrow_date  = models.DateField()
    due_date     = models.DateField()
    return_date  = models.DateField(null=True, blank=True)
    recorded_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes        = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.book.title} → {self.student.full_name}"

    @property
    def is_overdue(self):
        return self.return_date is None and date.today() > self.due_date

    @property
    def is_returned(self):
        return self.return_date is not None


# ─────────────────────────────────────────────────────────────
#  TIMETABLE
# ─────────────────────────────────────────────────────────────
class Timetable(models.Model):
    PERIOD_CHOICES = [
        ('1', 'Period 1 (07:30–08:15)'),
        ('2', 'Period 2 (08:15–09:00)'),
        ('3', 'Period 3 (09:00–09:45)'),
        ('4', 'Period 4 (10:00–10:45)'),
        ('5', 'Period 5 (10:45–11:30)'),
        ('6', 'Period 6 (11:30–12:15)'),
    ]
    class_level = models.CharField(max_length=20, choices=CLASS_LEVELS)
    day         = models.CharField(max_length=5, choices=DAYS_OF_WEEK)
    period      = models.CharField(max_length=2, choices=PERIOD_CHOICES)
    subject     = models.CharField(max_length=100)
    teacher     = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True,
                                    limit_choices_to={'role': 'teacher', 'is_active': True})

    class Meta:
        unique_together = ('class_level', 'day', 'period')
        ordering = ['class_level', 'day', 'period']

    def __str__(self):
        return f"{self.get_class_level_display()} | {self.day} P{self.period}: {self.subject}"


# ─────────────────────────────────────────────────────────────
#  SUPERVISOR VISIT
# ─────────────────────────────────────────────────────────────
class SupervisorVisit(models.Model):
    WEEK_CHOICES = [(2, 'Week 2'), (4, 'Week 4')]

    date          = models.DateField()
    supervisor    = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='visits')
    class_visited = models.CharField(max_length=20, choices=CLASS_LEVELS)
    week_number   = models.IntegerField(choices=WEEK_CHOICES)
    notes         = models.TextField()
    recommendations = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Visit {self.date} | {self.get_class_visited_display()} | Week {self.week_number}"


# ─────────────────────────────────────────────────────────────
#  SALES & CONTRIBUTIONS
# ─────────────────────────────────────────────────────────────
class SalesContribution(models.Model):
    TYPES = [
        ('uniform_sale',       'Uniform Sale'),
        ('grocery_submission', 'Grocery Submission'),
        ('relish_contribution','Relish Contribution'),
    ]
    student           = models.ForeignKey(Student, on_delete=models.SET_NULL,
                                          null=True, blank=True, related_name='contributions')
    contribution_type = models.CharField(max_length=30, choices=TYPES)
    description       = models.CharField(max_length=300, blank=True)
    amount            = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date              = models.DateField()
    recorded_by       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='recorded_contributions')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_contribution_type_display()} | {self.date}"
