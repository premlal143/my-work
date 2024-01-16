from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail
from django.db.models import Sum
from django.contrib import messages
import random
from django.db import IntegrityError, transaction
from django.conf import settings
from .models import labor_register
from parties.models import parties_detail,task, payment_installment

def labor_id_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        labor_id = request.session.get('labor_id', None)
        if not labor_id:
            return redirect('login_view')
        else:
            try:
                get_labor_data =labor_register.objects.get(labor_id=request.session.get('labor_id'))
            except labor_register.DoesNotExist:
                messages.info(request, 'User does not exist.')
            else:
                request.session['first_name'] = get_labor_data.first_name
                request.session['last_name'] = get_labor_data.last_name
                request.session['email'] = get_labor_data.email
                request.session['mobile'] = get_labor_data.mobile


                return view_func(request, *args, **kwargs)
    return _wrapped_view

def login_view(request):
    if request.method == 'POST':
        labor_id_ =request.POST['labor_id']
        password_ =request.POST['password']

        try:
            check_user = labor_register.objects.get(labor_id=labor_id_)
        except labor_register.DoesNotExist:
            messages.info(request, 'User does not exist.')
        else:
            if check_user:
                if check_user.password == password_:
                    request.session['labor_id'] = labor_id_
                    print("now you are logged in")
                    return redirect('dashboard_view')
                else:
                        messages.info(request, 'labor id or password does not match.')
    return render(request, 'login.html')

def register_request_view(request):
    if request.method == 'POST':
        labor_id_ = request.POST['laborid']
        first_name_ = request.POST['firstname']
        last_name_ = request.POST['lastname']
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        password_ = request.POST['password']

        if labor_id_ and first_name_ and last_name_ and email_ and mobile_ and password_:
            new_labor = labor_register.objects.create(
                labor_id_ = labor_id_,
                first_name = first_name_,
                last_name = last_name_,
                email = email_,
                mobile = mobile_,
                password = password_
                
            )
            new_labor.save()
            messages.success(request, 'Labor Register successfully')
            return redirect('login_view')


    return render(request, 'register-request.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        try:
            check_user = labor_register.objects.get(email=email_)
        except labor_register.DoesNotExist:
            messages.info(request, 'User does not exist.')
        else:
            if check_user:
                otp_ =random.randint(000000, 999999)


                subject = 'OTP Verification | MY-WORK'
                message = f"Your OTP is : {otp_}"
                from_email= settings.EMAIL_HOST_USER
                recipient_list = [f'{email_}']

                print(subject, message, from_email, recipient_list)
                send_mail(subject, message, from_email, recipient_list)
                check_user.otp = otp_
                check_user.save()
                context = {
                    'email':email_
                }

                return render(request, 'otp-verification.html', context)
    return render(request, 'forgot-password.html')

def otp_verify_view(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        otp_ = request.POST['otp']
        new_password_ = request.POST['new_password']
        confirm_password_ = request.POST['confirm_password']
        try:
            check_user = labor_register.objects.get(email=email_)
        except labor_register.DoesNotExist:
            messages.info(request, 'User does not exist.')
        else:
            if check_user:
                if check_user.otp == otp_:
                    if new_password_ == confirm_password_:
                        check_user.password = new_password_
                        check_user.save()
                        messages.success('password updated successfully')
                    else:
                        messages.warning("New password and Confirm password doesn't match")
                        return redirect('otp_verify_view')
                else:
                    messages.info(request, "Invalid otp")
                    return redirect('otp_verify_view')
    return render(request, 'otp-verification.html')

@labor_id_required
def logout(request):
    if 'labor_id' in request.session:
        del request.session['labor_id']
        messages.success(request, 'Now you are logged out.')
        return redirect('login_view')
    messages.info(request, 'You are not logged in yet.')
    return render(request, 'login_view')


@labor_id_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@labor_id_required
def tasks_view(request):
    labor_id_ = request.session.get('labor_id')
    parties_ = parties_detail.objects.filter(labor_id=labor_id_)
    tasks_ = task.objects.filter(labor_id=labor_id_).order_by('-Created_at')
    context = {
        'parties':parties_,
        'tasks':tasks_
    }
    return render(request, 'tasks.html', context)


@labor_id_required
def update_task(request, task_id):
    get_task_details = task.objects.get(task_id=task_id)
    labor_id_ = request.session.get('labor_id')
    parties_ = parties_detail.objects.filter(labor_id=labor_id_)
    instance = get_object_or_404(task, task_id=task_id)

    if request.method == 'POST':
        firmname_ = request.POST['firmname']
        title_ = request.POST['title']
        content_ = request.POST['content']
        task_status_ = request.POST['task_status']

        get_task_details.party_id_id = firmname_
        get_task_details.title = title_
        get_task_details.content = content_
        get_task_details.task_status = task_status_

        get_task_details.save()
        messages.success(request, f"{task_id} is updated.")
        return redirect('tasks_view')


    context = {
        'task':get_task_details,
        'parties':parties_,
        'TASK_STATUS': instance.TASK_STATUS,
        'task_status': get_task_details.task_status
    }
    return render(request, 'update-task.html', context)

@labor_id_required
def delete_task(request, task_id):
    delete_task_ = task.objects.get(task_id=task_id)
    delete_task_.delete()
    messages.success(request, f'{task_id} is deleted.')
    return redirect('tasks_view')

@labor_id_required
def payment_entry(request, task_id):
    # Use get_object_or_404 to handle the case where the task_id does not exist
    get_task_details = get_object_or_404(task, task_id=task_id)
    
    # Use select_related to fetch related labor data in a single query
    get_all_installment = payment_installment.objects.filter(task_id=task_id).select_related('labor_id')

    if request.method == 'POST':
        payment_installment_ = float(request.POST.get('payment_entry', 0))
        payment_date_ = request.POST.get('payment_date', '')

        if payment_installment_ != 0:
            if payment_installment_ <= get_task_details.remaining_payment:
                try:
                    with transaction.atomic():
                        get_task_details.remaining_payment -= payment_installment_
                        get_task_details.paid_payment += payment_installment_

                        if get_task_details.total_payment == get_task_details.paid_payment:
                            get_task_details.payment_status = 'Done'
                        else:
                            get_task_details.payment_status = 'Partially Paid'
                        get_task_details.save()

                        new_payment_entry = payment_installment.objects.create(
                            task_id_id=task_id,
                            labor_id=get_task_details.labor_id,
                            payment_entry=payment_installment_,
                            paid_date=payment_date_
                        )
                        messages.success(request, f'{payment_installment_} added')
                        return redirect('payment_entry', task_id=task_id)

                except IntegrityError as e:
                    messages.warning(request, 'Database error. Please try again.')
                    # Log the error or handle it appropriately

            else:
                messages.warning(request, 'Invalid installment amount')
        else:
            messages.warning(request, 'You cannot add a 0 installment')

    context = {
        'task': get_task_details,
        'installments': get_all_installment,
    }
    return render(request, 'task-payment.html', context)

@labor_id_required
def parties_view(request):
    if request.method == 'POST':
        firm_name_ = request.POST['firmname']
        first_name_ = request.POST['firstname']
        last_name_ = request.POST['lastname']
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        address_ = request.POST['address']

        new_party = parties_detail.objects.create(
            labor_id_id=request.session.get('labor_id'),
            firm_name=firm_name_,
            first_name=first_name_,
            last_name=last_name_,
            email=email_,
            mobile=mobile_,
            address=address_

        )
        new_party.save()
        messages.success(request, 'Party added')
        return redirect('parties_view')
    
    parties_ = parties_detail.objects.filter(labor_id=request.session.get('labor_id')).order_by('-id')
    context = {
        'parties':parties_
    }
    return render(request, 'parties.html', context)

@labor_id_required
def update_party_details(request,id):
    get_party = parties_detail.objects.get(id=id)
    if request.method == 'POST':
        firm_name_ = request.POST['firmname']
        first_name_ = request.POST['firstname']
        last_name_ = request.POST['lastname']
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        address_ = request.POST['address']
        get_party.firm_name = firm_name_
        get_party.first_name = first_name_
        get_party.last_name = last_name_
        get_party.email = email_
        get_party.mobile = mobile_
        get_party.address = address_
        get_party.save()
        messages.success(request, 'Party details updated')
        return redirect('parties_view')
    

    context = {
        'get_party':get_party
    }
    return render(request, 'update-party.html', context)

@labor_id_required
def delete_party(request,id):
    get_party = parties_detail.objects.get(id=id)
    get_party.delete()
    print("party delete")
    return redirect( 'parties_view')

@labor_id_required
def payments_view(request):
    labor_id_ = request.session.get('labor_id')
    print(labor_id_)
    total_amount = task.objects.filter(labor_id=labor_id_).aggregate(total=Sum('total_payment'))
    paid_amount = task.objects.filter(labor_id=labor_id_).aggregate(total=Sum('paid_payment'))
    remaining_amount = task.objects.filter(labor_id=labor_id_).aggregate(total=Sum('remaining_payment'))
    print(total_amount, paid_amount, remaining_amount)
    context = {
        'total_amount':total_amount['total'],
        'paid_amount':paid_amount['total'],
        'remaining_amount':remaining_amount['total']
    }
    return render(request, 'payments.html', context)

@labor_id_required
def profile_view(request):
    return render(request, 'profile.html')