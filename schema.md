# Digtial transformation of company

## Manual process 
### Phase 1 
1. Call from customer 
2. Acquire customer details 
3. Check to see which servicemen is free before sending one down

### Phase 2 
1. Servicemen on site will access issue 
2. Take steps to service
3. Fill up form 
    - Steps taken
    - Problem
    - Customer location and name 
    - Hours there 
4. Sends information to company to be filled out manually

### Phase 3 
1. Company issues invoice via email and requires signature

# Design 
For the first MVP will be 3 relational tables(jobs , servicemen and customers)
Jobs will be centre of the data base, where customers and servicemen will have on to many relationship with 


## MVP 1
- Simple CRUD features
- Three models 
    1. Customer
    2. Technician
    3. Timesheet
- Must have a customer and technician alredy created -> then timesheet creation choose from already created customer and technician

### Next step 
- Next MVP focuses on the authentication 
- Also add on to the timesheet feature to see in more detail the issue reported etc 
- only allow admin create 
- technicians can only see what they are assigned to 
- Have a nav to admin 

### Unfinished potential add ons
- Status completion button 

