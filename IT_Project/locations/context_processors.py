from .models import Vehicle, Order, Location, CustomUser, User, VehicleType

def message_processor(request):
    if not request.user.username:
         return {
        'unreturned' : None
    }
    username = request.user.username
    logged_user  = CustomUser.objects.get(user = User.objects.get(username = username))
    unreturned_order = Order.objects.filter(customer = logged_user, final_time = None).first()
    return {
        'unreturned' : unreturned_order
    }