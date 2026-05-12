"""
Sibane ECD Academy — URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    # ── Auth ───────────────────────────────────────────────
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ── Dashboard ──────────────────────────────────────────
    path('', views.dashboard, name='dashboard'),

    # ── Students ───────────────────────────────────────────
    path('students/',                views.student_list,   name='student_list'),
    path('students/add/',            views.student_add,    name='student_add'),
    path('students/<int:pk>/',       views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/',  views.student_edit,   name='student_edit'),
    path('students/<int:pk>/delete/',views.student_delete, name='student_delete'),

    # ── Staff ──────────────────────────────────────────────
    path('staff/',                views.staff_list,   name='staff_list'),
    path('staff/add/',            views.staff_add,    name='staff_add'),
    path('staff/<int:pk>/edit/',  views.staff_edit,   name='staff_edit'),
    path('staff/<int:pk>/delete/',views.staff_delete, name='staff_delete'),

    # ── Attendance ─────────────────────────────────────────
    path('attendance/mark/',    views.attendance_mark,    name='attendance_mark'),
    path('attendance/history/', views.attendance_history, name='attendance_history'),

    # ── Payments ───────────────────────────────────────────
    path('payments/',                  views.payment_list,   name='payment_list'),
    path('payments/add/',              views.payment_add,    name='payment_add'),
    path('payments/<int:pk>/delete/',  views.payment_delete, name='payment_delete'),

    # ── Meals ──────────────────────────────────────────────
    path('meals/',      views.meal_list, name='meal_list'),
    path('meals/add/',  views.meal_add,  name='meal_add'),

    # ── Expenses ───────────────────────────────────────────
    path('expenses/',                 views.expense_list,   name='expense_list'),
    path('expenses/add/',             views.expense_add,    name='expense_add'),
    path('expenses/<int:pk>/edit/',   views.expense_edit,   name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),

    # ── Inventory ──────────────────────────────────────────
    path('inventory/',                        views.inventory_list,        name='inventory_list'),
    path('inventory/add/',                    views.inventory_add,         name='inventory_add'),
    path('inventory/<int:pk>/edit/',          views.inventory_edit,        name='inventory_edit'),
    path('inventory/<int:pk>/transaction/',   views.inventory_transaction, name='inventory_transaction'),

    # ── Library ────────────────────────────────────────────
    path('library/',                   views.book_list,    name='book_list'),
    path('library/add/',               views.book_add,     name='book_add'),
    path('library/<int:pk>/edit/',     views.book_edit,    name='book_edit'),
    path('library/borrows/',           views.borrow_list,  name='borrow_list'),
    path('library/borrow/',            views.borrow_book,  name='borrow_book'),
    path('library/return/<int:pk>/',   views.return_book,  name='return_book'),

    # ── Timetable ──────────────────────────────────────────
    path('timetable/',                 views.timetable_view,   name='timetable_view'),
    path('timetable/add/',             views.timetable_add,    name='timetable_add'),
    path('timetable/<int:pk>/delete/', views.timetable_delete, name='timetable_delete'),

    # ── Supervisor Visits ──────────────────────────────────
    path('visits/',                 views.visit_list,   name='visit_list'),
    path('visits/add/',             views.visit_add,    name='visit_add'),
    path('visits/<int:pk>/edit/',   views.visit_edit,   name='visit_edit'),
    path('visits/<int:pk>/delete/', views.visit_delete, name='visit_delete'),

    # ── Contributions ──────────────────────────────────────
    path('contributions/',                  views.contribution_list,   name='contribution_list'),
    path('contributions/add/',              views.contribution_add,    name='contribution_add'),
    path('contributions/<int:pk>/delete/',  views.contribution_delete, name='contribution_delete'),
    # ── Health check ──────────────────────────────────────────────
    path('health/', views.health_check, name='health_check'),
]
