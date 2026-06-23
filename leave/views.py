from django.shortcuts import render,redirect,get_object_or_404
from leave.models import Leave
from django.contrib.auth.decorators import login_required

# Create your views here.
def apply_leave(request):
    if request.method == "POST":
        Leave.objects.create(
            user  = request.user,
            leave_type = request.POST['leave_type'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            reason = request.POST['reason'],
            status = "Pending"
        )
        return redirect('staff_dashboard')
    return render(request,'apply_leave.html')

@login_required
def my_leaves(request):
    leaves = Leave.objects.filter(user = request.user)
    return render(request, 'my_leaves.html', {'leaves':leaves})

@login_required
def view_leaves(request):
    if request.user.profile.role != "admin":
        return redirect('staff_dashboard')
    leaves =  Leave.objects.all()
    return render(request,'view_leaves.html',{'leaves':leaves})

@login_required
def approve_leave(request,id):
    if request.user.profile.role != "admin":
        return redirect('staff_dashboard')
    # leave = Leave.objects.get(id=id)   another way to get the leave object
    # leave = Leave.objects.filter(id=id).update(status = "approved")  # another way to get the leave object
    leave = get_object_or_404(Leave,id=id)
    leave.status = "Approved"
    leave.save()
    return redirect('view_leaves')

@login_required
def reject_leave(request,id):
    if request.user.profile.role != "admin":
        return redirect('staff_dashboard')
    leave = get_object_or_404(Leave, id=id)
    leave.status = "Rejected"
    leave.save()
    return redirect('view_leaves')