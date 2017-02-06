from tables import SchoolAccount

def verifyLink(request_user, request_school):
    return True if len(SchoolAccount.query(SchoolAccount.user_id == request_user, SchoolAccount.school_uuid == request_school).fetch()) > 0 else False
