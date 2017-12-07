from requests import put, get

def addOrganization(URL, Organization):
    Organization = Organization.replace(" ", "_").lower()
    url = URL+"/organizations"
    return put(url, data={"data": Organization}).json()

def addUser(URL, organization, id, name, surname, username, password, role="student"):
    url = URL+"/organizations/%s" %organization.replace(" ", "_").lower()
    return put(url,data={
                        "ID": id,
                        "Name": name,
                        "Surname": surname,
                        "Role": role,
                        "Username": username,
                        "Password": password
                        }).json()

def signIn(URL, organization, username, password):
    url = URL+"/organizations/%s/%s" %(organization.replace(" ", "_").lower(), username)
    return get(url, data={
                        "Username": username,
                        "Password": password
                        }).json()
