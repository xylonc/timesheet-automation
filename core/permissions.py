class Roles:
    ADMIN = 'Admin'
    TECHNICIAN = 'Technician'
    
ROLE_RULES = {
        'technicians_list':{Roles.ADMIN},
        'create_technician':{Roles.ADMIN},
        'customer_list':{Roles.ADMIN,Roles.TECHNICIAN},
        'create_customer':{Roles.ADMIN},
        'home':{Roles.ADMIN,Roles.TECHNICIAN},
        'create_service_report':{Roles.ADMIN},
        'service_report_list':{Roles.ADMIN , Roles.TECHNICIAN},
        'users:create_admin':{Roles.ADMIN},
}