ROLE_EMPLOYEE='employee'
ROLE_MANAGER='manager'
ROLE_ADMIN='admin'

ROLE_CHOICES=[
    (ROLE_EMPLOYEE,'Employee'),
    (ROLE_MANAGER,'Manager'),
    (ROLE_ADMIN,'Admin')
]


SICK_LEAVE='Sick'
CASUAL_LEAVE='Casual'
PAID_LEAVE='Paid'

LEAVE_TYPES=[
    (SICK_LEAVE,'sick'),
    (CASUAL_LEAVE,'Casual'),
    (PAID_LEAVE,'Paid')
]


STATUS_APPROVED='approved'
STATUS_REJECTED='rejected'
STATUS_PENDING='pending'

STATUS_TYPES=[
    (STATUS_APPROVED,'Approved'),
    (STATUS_REJECTED,'Rejected'),
    (STATUS_PENDING,'Pending')
]


ACTION_APPLIED='Applied'
ACTION_APPROVED='Approved'
ACTION_REJECTED='Rejected'

ACTION_TYPES=[
    (ACTION_APPLIED,'applied'),
    (ACTION_APPROVED,'approved'),
    (ACTION_REJECTED,'rejected')
]