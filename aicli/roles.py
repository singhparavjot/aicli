roles_permissions = {
    'admin': ['execute', 'explain'],
    'user': ['execute']
}

# Simulating user roles for the purpose of this example
# In a real-world scenario, this information should be securely managed and retrieved
user_roles = {
    'alice': 'admin',
    'bob': 'user'
}

def get_user_role(username):
    return user_roles.get(username, 'user')

def has_permission(username, command):
    role = get_user_role(username)
    return command in roles_permissions.get(role, [])

