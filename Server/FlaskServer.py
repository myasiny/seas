from flask import Flask, request, jsonify
from Models import MySQLdb, Password, Credential

app = Flask(__name__)
db = MySQLdb("TestDB", app)


@app.route("/")
def test_connection():
    return "I am alive!"


@app.route("/organizations", methods= ["PUT"])
def signUpOrganization():
    return jsonify(db.initialize_organization(request.form["data"]))

@app.route("/organizations/<string:organization>", methods=["GET", "PUT"])
def signUpUser(organization):
    if request.method == "GET":
        organization = organization.replace(" ", "_").lower()
        return jsonify(db.execute("SELECT * FROM %s.members" %organization))
    else:
        command = "Insert into %s.members(ID, Role, Name, Surname, Username, Password, Email, Department) " \
                  "values(%s, '%d', '%s', '%s', '%s', '%s', '%s', '%s')" \
                  %(organization.replace(" ", "_").lower(),
                    request.form["ID"],
                    int(db.execute("SELECT ID FROM %s.roles WHERE Role = '%s'" %(organization, request.form["Role"].lower()))[0]),
                    request.form["Name"],
                    request.form["Surname"],
                    request.form["Username"],
                    Password().hashPassword(request.form["Password"]),
                    request.form["Email"],
                    request.form["Department"]
                    )

        return jsonify(db.execute(command))


@app.route("/organizations/<string:organization>/<string:username>", methods= ["GET"])
def signInUser(organization, username):
    organization = organization.replace(" ", "_").lower()
    try:
        passwd = db.execute("select Password from %s.members where Username = '%s'" % (organization, username))[0]
        if Password().verify_password_hash(request.form["Password"], passwd):
            rtn = list(db.execute("select Username, Name, Surname, ID, Role, Email, Department "
                                  "from %s.members where Username=('%s')" % (organization, request.form["Username"])))
            rtn[4] = db.execute("SELECT Role FROM %s.roles WHERE ID = '%s'" % (organization, rtn[4]))[0]
            rtn.append(organization)
            return jsonify(rtn)
        else:
            return jsonify("Wrong Password")
    except IndexError:
        return jsonify(None)
    except TypeError:
        return jsonify("Wrong Username!")


@app.route("/organizations/<string:organization>/<string:username>/edit_password", methods=["PUT"])
def changePassword(organization, username):
    pass

if __name__ == "__main__":
    app.run(host="10.50.81.24", port=8888)