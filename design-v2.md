# Digitalisation of company 
**Status:** Proposed | Author : Xylon 

## Context 
- The company provides computer servicing services. They have contracts and adhoc jobs that require technicians to go down on site to fix the issue reported. Whenever there is a job a technician is dispatched down to the site to service and has to come up with a service report.  
- The identified area for improvement is that this service reporting is separate from the current software they have to generate the other important documents from the service report (eg generating an invoice from the service report), this results in manual copying of the service report created by the technician back into the software again which can be automated if the service report was also handled by a central software
- The goal of this app is reduce the amount of manual labor needed and hence maximise efficiency of the company 

## Goals
1. Design an app that handles all the job information and document generation
2. Remove the need for manual entering of information that has already been keyed in by the technician
3. Migrating the company's document generation software to this new app that handles it 

## Non goals 
1. Not building a customer or technician facing portal 
2. Not in charge of payments 

## Threat model

| Internet scraper | Can probe public IPs | Find data to leak | Local-only deployment, no public endpoints |
| Rogue technician | Knows the admin uses this system | Steal customer list | No technician accounts; cannot reach the app |
| Competitor | May attempt phishing or physical access | Acquire customer/job data | Admin-only login + strong password; office machine physical security |

## Design 
### Stack 
- Will be using Django and postgreSQL 
### Models
1. Customer
2. Technician
3. Service report 
4. Invoices 
- (MVP 1)

#### Customers 
- Name
- Contact
- Email Address
- Address

#### Technicians 
- Name
- Contact
- Email Address
- Working status

#### Service report
- Customer (FK)
- Technician (FK)
- Time in
- Time out
- Issue reported 
- Actions taken 
- Serial number
- Warranty
- Service report number
- Status 

### Invoice
- Service report(FK)
- Rate 
- Invoice number


- Customer and technicians are OnetoOne fields with users 
- Service reports are OnetoMany fields with both customers and technicians
- Invoices will be OnetoMany field with the service report with status updates of which is the one currently in use 

### Deployment 
- Will be internal tool that is only available locally on admin machine 
- Only reachable from within the company office 

### Authentication 
Only admins have access to the platform


