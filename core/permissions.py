class Roles:
    ADMIN = 'Admin'
    TECHNICIAN = 'Technician'
    
ROLE_RULES = {
        'technicians_list':{Roles.ADMIN,Roles.TECHNICIAN},
        'create_technician':{Roles.ADMIN},
        'customer_list':{Roles.ADMIN,Roles.TECHNICIAN},
        'create_customer':{Roles.ADMIN},
        'home':{Roles.ADMIN,Roles.TECHNICIAN},
        'create_timesheet':{Roles.ADMIN},
        'timesheet_list':{Roles.ADMIN , Roles.TECHNICIAN}
}