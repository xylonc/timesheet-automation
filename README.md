# Field-Service Management System

A Django web application for a Singapore field-service SME , replacing a manual workflow in which technicians filled out paper service reports that office staff then re-keyed into separate software to generate invoices. The system centralises job records, enforces who can see and do what, and governs each service report through a controlled lifecycle.

 This README focuses on the design decisions rather than a feature list, since those decisions are the point.

---

## Status

**Implemented:** custom user model, role groups (Admin / Technician), default-deny authentication, role-based authorization, customer / technician / service-report models, the service-report state machine, and a test suite covering authorization, transaction atomicity, and state-machine legality.

**In progress:** invoice generation from approved service reports (the next module — the service-report lifecycle terminates at `signed`, which is the handoff point into invoicing).

---

## Running locally

```bash
git clone https://github.com/xylonc/timesheet-automation.git
cd timesheet-automation
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
```

Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The role groups (Admin, Technician) are created automatically by a data migration, so they exist as soon as you migrate.

---

## Architecture & design decisions

### Authorization is enforced at the data layer, not in views

Each model exposes a `visible_to(user)` method on a custom `QuerySet` manager. A technician querying customers gets only the customers tied to service reports assigned to them; an admin gets everything:

```python
class CustomerQuerySet(models.QuerySet):
    def visible_to(self, user):
        if user.is_superuser or user.groups.filter(name=Roles.ADMIN).exists():
            return self
        return self.filter(servicereport__technician__user=user).distinct()
```

**Why this way:** the alternative is to filter inside each view. That works until someone adds a new view and forgets the check — and now data leaks silently. Pushing the scoping into the queryset means the *default* way of fetching data is already scoped; a developer has to go out of their way to bypass it. Authorization becomes a property of the data access layer rather than something re-implemented (and occasionally forgotten) per view.

### Two-layer middleware: authenticate, then authorize

`LoginRequiredMiddleware` enforces default-deny authentication — every route requires login except an explicit allowlist (login, password reset). `RoleRequiredMiddleware` then checks the authenticated user's role groups against a central `ROLE_RULES` table mapping view names to allowed roles.

**Why a central table:** keeping the route-to-role mapping in one dictionary (`core/permissions.py`) means the access policy is auditable in a single place, instead of being scattered across view decorators. If a route isn't in the table, the middleware denies it — unknown routes fail closed, not open.

### The service report is a state machine

A service report moves through `dispatched → submitted → approved → emailed → signed` (with `cancelled` reachable from `dispatched`). Transitions are defined declaratively:

```python
ALLOWED_TRANSITIONS = {
    Status.DISPATCHED: [Status.SUBMITTED, Status.CANCELLED],
    Status.SUBMITTED:  [Status.APPROVED],
    Status.APPROVED:   [Status.EMAILED],
    Status.EMAILED:    [Status.SIGNED],
    Status.SIGNED:     set(),   # terminal
    Status.CANCELLED:  set(),   # terminal
}
```

`transition_to(new_status, actor)` rejects any move not in the table, then runs a precondition check for the target state (e.g. a report can't be *submitted* until issue, actions, serial, and times are filled; can't be *approved* by a non-admin; can't be *emailed* without a customer email on file).

**Why a state machine:** the business process has real rules — you cannot email a report before it's approved, you cannot approve one with missing fields. Encoding those as a transition table plus precondition methods makes illegal transitions structurally impossible rather than relying on UI discipline or scattered `if` checks. The preconditions are resolved by deferred lookup (`getattr(self, method_name)`) so the table can reference methods defined later in the class.

### Atomic user + technician creation

Creating a technician creates *two* rows: a `User` (for auth) and a `Technician` (the domain record), linked one-to-one. This happens inside `transaction.atomic()`:

```python
with transaction.atomic():
    user = user_form.save()
    tech = tech_form.save(commit=False)
    tech.user = user
    tech.save()
    user.groups.add(Group.objects.get(name=Roles.TECHNICIAN))
```

**Why:** without the transaction, a failure after the user is created but before the technician is saved leaves an orphaned user account with no domain record and no role — a corrupt half-state. The atomic block guarantees both rows commit or neither does. This is tested explicitly (see below).

---

## Testing

The test suite targets correctness and security boundaries, not trivial assertions:

- **Authorization boundaries** — technicians cannot see customers or service reports not assigned to them, in both the queryset and the rendered view; admins and superusers see everything.
- **Default-deny auth** — anonymous users are redirected to login with the destination preserved; static files are exempt; a technician hitting an admin-only route gets 403.
- **Transaction atomicity** — an invalid technician form creates no orphaned user; a simulated DB failure mid-creation (patched to raise) rolls back both rows.
- **State-machine legality** — every legal transition is allowed, every illegal skip (e.g. dispatched → signed) is rejected, terminal states have no exits, and every precondition name in the dispatch table resolves to a real method.

```bash
python manage.py test
```

---

## Stack

Python · Django · SQLite (development) · `python-decouple` for configuration.

Designed for a local, single-admin office deployment — see `design-v2.md` for the threat model and the full design rationale.
