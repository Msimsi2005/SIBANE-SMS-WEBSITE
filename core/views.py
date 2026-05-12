"""
Sibane ECD Academy — Views
All views require login. Uses function-based views for clarity.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import date, timedelta

from .models import (
    Student, Staff, Attendance, Payment, MealRecord, Expense,
    InventoryItem, InventoryTransaction, Book, BookBorrow,
    Timetable, SupervisorVisit, SalesContribution,
    CLASS_LEVELS,
)
from .forms import (
    LoginForm, StudentForm, StaffForm, AttendanceForm, AttendanceFilterForm,
    PaymentForm, MealRecordForm, ExpenseForm,
    InventoryItemForm, InventoryTransactionForm,
    BookForm, BookBorrowForm, TimetableForm,
    SupervisorVisitForm, SalesContributionForm,
)


# ─────────────────────────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next', 'dashboard'))
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    today = date.today()
    this_month_start = today.replace(day=1)

    # Student stats
    total_students = Student.objects.filter(is_active=True).count()
    students_by_class = {
        label: Student.objects.filter(is_active=True, class_level=code).count()
        for code, label in CLASS_LEVELS
    }

    # Today's attendance
    attendance_today = Attendance.objects.filter(date=today)
    present_today = attendance_today.filter(status='present').count()
    absent_today  = attendance_today.filter(status='absent').count()

    # Fees this month
    fees_this_month = Payment.objects.filter(
        date__gte=this_month_start
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Expenses this month
    expenses_this_month = Expense.objects.filter(
        date__gte=this_month_start
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Low stock items
    low_stock = InventoryItem.objects.all()
    low_stock = [item for item in low_stock if item.is_low_stock]

    # Overdue books
    overdue_borrows = BookBorrow.objects.filter(
        return_date__isnull=True,
        due_date__lt=today
    ).count()

    # Recent payments
    recent_payments = Payment.objects.select_related('student').order_by('-date')[:5]

    # Recent expenses
    recent_expenses = Expense.objects.order_by('-date')[:5]

    context = {
        'total_students':       total_students,
        'students_by_class':    students_by_class,
        'present_today':        present_today,
        'absent_today':         absent_today,
        'total_marked_today':   attendance_today.count(),
        'fees_this_month':      fees_this_month,
        'expenses_this_month':  expenses_this_month,
        'low_stock_count':      len(low_stock),
        'low_stock_items':      low_stock[:5],
        'overdue_borrows':      overdue_borrows,
        'recent_payments':      recent_payments,
        'recent_expenses':      recent_expenses,
        'today':                today,
    }
    return render(request, 'dashboard.html', context)


# ─────────────────────────────────────────────────────────────
#  STUDENTS
# ─────────────────────────────────────────────────────────────
@login_required
def student_list(request):
    q           = request.GET.get('q', '')
    class_filter = request.GET.get('class_level', '')
    show_inactive = request.GET.get('inactive', '')

    students = Student.objects.all()
    if not show_inactive:
        students = students.filter(is_active=True)
    if class_filter:
        students = students.filter(class_level=class_filter)
    if q:
        students = students.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(parent_name__icontains=q)
        )

    return render(request, 'students/list.html', {
        'students': students,
        'q': q,
        'class_filter': class_filter,
        'class_levels': CLASS_LEVELS,
        'show_inactive': show_inactive,
    })


@login_required
def student_add(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student added successfully.')
        return redirect('student_list')
    return render(request, 'students/form.html', {'form': form, 'title': 'Add Student'})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated.')
        return redirect('student_detail', pk=pk)
    return render(request, 'students/form.html', {
        'form': form, 'title': f'Edit — {student.full_name}'
    })


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    payments = student.payments.order_by('-date')
    attendance = student.attendance_records.order_by('-date')[:30]
    borrows = student.borrows.order_by('-borrow_date')
    total_paid = student.total_paid()
    return render(request, 'students/detail.html', {
        'student': student,
        'payments': payments,
        'attendance': attendance,
        'borrows': borrows,
        'total_paid': total_paid,
    })


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.is_active = False
        student.save()
        messages.success(request, f'{student.full_name} has been deactivated.')
        return redirect('student_list')
    return render(request, 'confirm_delete.html', {
        'object': student,
        'cancel_url': 'student_list',
        'message': f'Deactivate student {student.full_name}?'
    })


# ─────────────────────────────────────────────────────────────
#  STAFF
# ─────────────────────────────────────────────────────────────
@login_required
def staff_list(request):
    staff = Staff.objects.filter(is_active=True).order_by('role', 'last_name')
    return render(request, 'staff/list.html', {'staff': staff})


@login_required
def staff_add(request):
    form = StaffForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Staff member added.')
        return redirect('staff_list')
    return render(request, 'staff/form.html', {'form': form, 'title': 'Add Staff Member'})


@login_required
def staff_edit(request, pk):
    member = get_object_or_404(Staff, pk=pk)
    form = StaffForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        messages.success(request, 'Staff updated.')
        return redirect('staff_list')
    return render(request, 'staff/form.html', {
        'form': form, 'title': f'Edit — {member.full_name}'
    })


@login_required
def staff_delete(request, pk):
    member = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        member.is_active = False
        member.save()
        messages.success(request, f'{member.full_name} deactivated.')
        return redirect('staff_list')
    return render(request, 'confirm_delete.html', {
        'object': member,
        'cancel_url': 'staff_list',
        'message': f'Deactivate {member.full_name}?'
    })


# ─────────────────────────────────────────────────────────────
#  ATTENDANCE
# ─────────────────────────────────────────────────────────────
@login_required
def attendance_mark(request):
    """Mark attendance for a whole class on a given date."""
    selected_date  = request.GET.get('date', str(date.today()))
    selected_class = request.GET.get('class_level', 'ecd_a')

    students = Student.objects.filter(is_active=True, class_level=selected_class)

    if request.method == 'POST':
        post_date  = request.POST.get('date')
        post_class = request.POST.get('class_level')
        saved = 0
        for student in Student.objects.filter(is_active=True, class_level=post_class):
            status = request.POST.get(f'status_{student.pk}', 'absent')
            notes  = request.POST.get(f'notes_{student.pk}', '')
            obj, created = Attendance.objects.update_or_create(
                student=student,
                date=post_date,
                defaults={
                    'status': status,
                    'notes': notes,
                    'recorded_by': request.user,
                }
            )
            saved += 1
        messages.success(request, f'Attendance saved for {saved} student(s).')
        return redirect(f"{request.path}?date={post_date}&class_level={post_class}")

    # Pre-fill existing records
    existing = {
        a.student_id: a
        for a in Attendance.objects.filter(
            date=selected_date,
            student__class_level=selected_class
        )
    }

    return render(request, 'attendance/mark.html', {
        'students':       students,
        'existing':       existing,
        'selected_date':  selected_date,
        'selected_class': selected_class,
        'class_levels':   CLASS_LEVELS,
    })


@login_required
def attendance_history(request):
    form = AttendanceFilterForm(request.GET or None)
    records = Attendance.objects.select_related('student').order_by('-date')

    if form.is_valid():
        if form.cleaned_data.get('date'):
            records = records.filter(date=form.cleaned_data['date'])
        if form.cleaned_data.get('class_level'):
            records = records.filter(student__class_level=form.cleaned_data['class_level'])

    records = records[:200]  # cap for performance
    return render(request, 'attendance/history.html', {
        'form': form, 'records': records
    })


# ─────────────────────────────────────────────────────────────
#  PAYMENTS
# ─────────────────────────────────────────────────────────────
@login_required
def payment_list(request):
    payments = Payment.objects.select_related('student').order_by('-date')
    q = request.GET.get('q', '')
    if q:
        payments = payments.filter(
            Q(student__first_name__icontains=q) | Q(student__last_name__icontains=q) |
            Q(reference__icontains=q)
        )
    total = payments.aggregate(t=Sum('amount'))['t'] or 0
    return render(request, 'payments/list.html', {
        'payments': payments[:100],
        'total': total,
        'q': q,
    })


@login_required
def payment_add(request):
    form = PaymentForm(request.POST or None, initial={'date': date.today()})
    if form.is_valid():
        payment = form.save(commit=False)
        payment.recorded_by = request.user
        payment.save()
        messages.success(request, 'Payment recorded.')
        return redirect('payment_list')
    return render(request, 'payments/form.html', {'form': form, 'title': 'Record Payment'})


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'Payment deleted.')
        return redirect('payment_list')
    return render(request, 'confirm_delete.html', {
        'object': payment,
        'cancel_url': 'payment_list',
        'message': f'Delete payment of ${payment.amount} for {payment.student.full_name}?'
    })


# ─────────────────────────────────────────────────────────────
#  MEALS
# ─────────────────────────────────────────────────────────────
@login_required
def meal_list(request):
    records = MealRecord.objects.order_by('-date')[:60]
    return render(request, 'meals/list.html', {'records': records})


@login_required
def meal_add(request):
    form = MealRecordForm(request.POST or None, initial={'date': date.today()})
    if form.is_valid():
        meal = form.save(commit=False)
        meal.recorded_by = request.user
        meal.save()
        messages.success(request, 'Meal record saved.')
        return redirect('meal_list')
    return render(request, 'meals/form.html', {'form': form, 'title': 'Record Meals'})


# ─────────────────────────────────────────────────────────────
#  EXPENSES
# ─────────────────────────────────────────────────────────────
@login_required
def expense_list(request):
    expenses = Expense.objects.order_by('-date')
    month = request.GET.get('month', '')
    if month:
        try:
            y, m = month.split('-')
            expenses = expenses.filter(date__year=y, date__month=m)
        except ValueError:
            pass
    total = expenses.aggregate(t=Sum('amount'))['t'] or 0
    return render(request, 'expenses/list.html', {
        'expenses': expenses[:100],
        'total': total,
        'month': month,
    })


@login_required
def expense_add(request):
    form = ExpenseForm(request.POST or None, initial={'date': date.today()})
    if form.is_valid():
        exp = form.save(commit=False)
        exp.recorded_by = request.user
        exp.save()
        messages.success(request, 'Expense added.')
        return redirect('expense_list')
    return render(request, 'expenses/form.html', {'form': form, 'title': 'Add Expense'})


@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        messages.success(request, 'Expense updated.')
        return redirect('expense_list')
    return render(request, 'expenses/form.html', {
        'form': form, 'title': 'Edit Expense'
    })


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted.')
        return redirect('expense_list')
    return render(request, 'confirm_delete.html', {
        'object': expense,
        'cancel_url': 'expense_list',
        'message': f'Delete expense: {expense.description} (${expense.amount})?'
    })


# ─────────────────────────────────────────────────────────────
#  INVENTORY
# ─────────────────────────────────────────────────────────────
@login_required
def inventory_list(request):
    items = InventoryItem.objects.all()
    cat = request.GET.get('category', '')
    if cat:
        items = items.filter(category=cat)
    return render(request, 'inventory/list.html', {
        'items': items,
        'category_filter': cat,
        'categories': InventoryItem.CATEGORIES,
    })


@login_required
def inventory_add(request):
    form = InventoryItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Item added to inventory.')
        return redirect('inventory_list')
    return render(request, 'inventory/form.html', {
        'form': form, 'title': 'Add Inventory Item'
    })


@login_required
def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    form = InventoryItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, 'Item updated.')
        return redirect('inventory_list')
    return render(request, 'inventory/form.html', {
        'form': form, 'title': f'Edit — {item.name}'
    })


@login_required
def inventory_transaction(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    form = InventoryTransactionForm(
        request.POST or None,
        initial={'item': item, 'date': date.today()}
    )
    if form.is_valid():
        tx = form.save(commit=False)
        tx.recorded_by = request.user
        tx.save()
        messages.success(request, f'Transaction recorded for {item.name}.')
        return redirect('inventory_list')
    return render(request, 'inventory/transaction.html', {
        'form': form, 'item': item
    })


# ─────────────────────────────────────────────────────────────
#  LIBRARY
# ─────────────────────────────────────────────────────────────
@login_required
def book_list(request):
    books = Book.objects.all()
    q = request.GET.get('q', '')
    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__icontains=q))
    return render(request, 'library/books.html', {'books': books, 'q': q})


@login_required
def book_add(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Book added to library.')
        return redirect('book_list')
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Add Book'})


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, 'Book updated.')
        return redirect('book_list')
    return render(request, 'library/book_form.html', {
        'form': form, 'title': f'Edit — {book.title}'
    })


@login_required
def borrow_list(request):
    borrows = BookBorrow.objects.select_related('book', 'student').order_by('-borrow_date')
    active_only = request.GET.get('active', '')
    if active_only:
        borrows = borrows.filter(return_date__isnull=True)
    return render(request, 'library/borrows.html', {
        'borrows': borrows,
        'active_only': active_only,
        'today': date.today(),
    })


@login_required
def borrow_book(request):
    form = BookBorrowForm(
        request.POST or None,
        initial={'borrow_date': date.today(), 'due_date': date.today() + timedelta(days=14)}
    )
    if form.is_valid():
        borrow = form.save(commit=False)
        borrow.recorded_by = request.user
        # Reduce available copies
        book = borrow.book
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()
            borrow.save()
            messages.success(request, f'"{book.title}" borrowed by {borrow.student.full_name}.')
        else:
            messages.error(request, 'No available copies of this book.')
        return redirect('borrow_list')
    return render(request, 'library/borrow_form.html', {
        'form': form, 'title': 'Borrow Book'
    })


@login_required
def return_book(request, pk):
    borrow = get_object_or_404(BookBorrow, pk=pk)
    if request.method == 'POST':
        borrow.return_date = date.today()
        borrow.save()
        # Increase available copies
        borrow.book.available_copies += 1
        borrow.book.save()
        messages.success(request, f'"{borrow.book.title}" returned.')
        return redirect('borrow_list')
    return render(request, 'library/return_confirm.html', {'borrow': borrow})


# ─────────────────────────────────────────────────────────────
#  TIMETABLE
# ─────────────────────────────────────────────────────────────
@login_required
def timetable_view(request):
    selected_class = request.GET.get('class_level', 'ecd_a')
    entries = Timetable.objects.filter(
        class_level=selected_class
    ).select_related('teacher').order_by('day', 'period')

    # Build a grid: {day: {period: entry}}
    days    = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    periods = ['1', '2', '3', '4', '5', '6']
    grid = {d: {p: None for p in periods} for d in days}
    for entry in entries:
        grid[entry.day][entry.period] = entry

    return render(request, 'timetable/view.html', {
        'grid':           grid,
        'days':           days,
        'periods':        Timetable.PERIOD_CHOICES,
        'selected_class': selected_class,
        'class_levels':   CLASS_LEVELS,
        'entries':        entries,
    })


@login_required
def timetable_add(request):
    form = TimetableForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Timetable entry added.')
        return redirect('timetable_view')
    return render(request, 'timetable/form.html', {'form': form, 'title': 'Add Timetable Entry'})


@login_required
def timetable_delete(request, pk):
    entry = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted.')
        return redirect('timetable_view')
    return render(request, 'confirm_delete.html', {
        'object': entry,
        'cancel_url': 'timetable_view',
        'message': f'Delete timetable entry: {entry}?'
    })


# ─────────────────────────────────────────────────────────────
#  SUPERVISOR VISITS
# ─────────────────────────────────────────────────────────────
@login_required
def visit_list(request):
    visits = SupervisorVisit.objects.select_related('supervisor').order_by('-date')
    return render(request, 'supervisor/list.html', {'visits': visits})


@login_required
def visit_add(request):
    form = SupervisorVisitForm(request.POST or None, initial={'date': date.today()})
    if form.is_valid():
        form.save()
        messages.success(request, 'Visit recorded.')
        return redirect('visit_list')
    return render(request, 'supervisor/form.html', {'form': form, 'title': 'Record Supervisor Visit'})


@login_required
def visit_edit(request, pk):
    visit = get_object_or_404(SupervisorVisit, pk=pk)
    form = SupervisorVisitForm(request.POST or None, instance=visit)
    if form.is_valid():
        form.save()
        messages.success(request, 'Visit updated.')
        return redirect('visit_list')
    return render(request, 'supervisor/form.html', {
        'form': form, 'title': 'Edit Visit'
    })


@login_required
def visit_delete(request, pk):
    visit = get_object_or_404(SupervisorVisit, pk=pk)
    if request.method == 'POST':
        visit.delete()
        messages.success(request, 'Visit deleted.')
        return redirect('visit_list')
    return render(request, 'confirm_delete.html', {
        'object': visit,
        'cancel_url': 'visit_list',
        'message': f'Delete visit record for {visit.date}?'
    })


# ─────────────────────────────────────────────────────────────
#  SALES & CONTRIBUTIONS
# ─────────────────────────────────────────────────────────────
@login_required
def contribution_list(request):
    contribs = SalesContribution.objects.select_related('student').order_by('-date')
    total = contribs.aggregate(t=Sum('amount'))['t'] or 0
    return render(request, 'contributions/list.html', {
        'contribs': contribs[:100],
        'total': total,
    })


@login_required
def contribution_add(request):
    form = SalesContributionForm(request.POST or None, initial={'date': date.today()})
    if form.is_valid():
        c = form.save(commit=False)
        c.recorded_by = request.user
        c.save()
        messages.success(request, 'Contribution recorded.')
        return redirect('contribution_list')
    return render(request, 'contributions/form.html', {
        'form': form, 'title': 'Record Contribution / Sale'
    })


@login_required
def contribution_delete(request, pk):
    c = get_object_or_404(SalesContribution, pk=pk)
    if request.method == 'POST':
        c.delete()
        messages.success(request, 'Contribution deleted.')
        return redirect('contribution_list')
    return render(request, 'confirm_delete.html', {
        'object': c,
        'cancel_url': 'contribution_list',
        'message': f'Delete {c.get_contribution_type_display()} record?'
    })


# ─────────────────────────────────────────────────────────────
#  HEALTH CHECK  (used by Render to verify app + DB are alive)
# ─────────────────────────────────────────────────────────────
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """
    Returns 200 + JSON if the web process AND database connection are healthy.
    Render polls /health/ every 30 s; a non-200 triggers an alert.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_ok = True
    except Exception as e:
        db_ok = False

    status = 200 if db_ok else 503
    return JsonResponse({
        "status": "ok" if db_ok else "db_error",
        "database": "connected" if db_ok else "unreachable",
        "app": "Sibane ECD Academy",
    }, status=status)
