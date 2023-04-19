# Web Server is used to accept incoming request 
# 1. GET - going to page
# 2. POST - Receive data and use it and data come with it
# 3. DELETE - remove data
# 4. PUT - update and add data 
# 5. HEAD AND MUCH MORE

from flask import Flask,jsonify,request
import git
# Created an Object of Flask with a unique name
app=Flask(__name__)  

stores=[
    {
        "name":"Amazon",
        "items":[
            {
                "item":"Earphone",
                "price":"560"
            },
            {
                "item":"Laptop",
                "price":"56000"
            }
        ]
    },
    {
        "name":"Flipkart",
        "items":[
            {
                "item":"Phone",
                "price":"15600"
            },
            {
                "item":"Charger",
                "price":"400"
            }
        ]
    }
]

# @app.route('/update_server', methods=['POST'])
# def webhook():
#   if request.method == 'POST':
#     # repo = git.Repo('./Dummy-app')
#     repo = git.Repo('/home/Pranav2003/Dummy-app')
#     origin = repo.remotes.origin
#     # repo.create_head('main',origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
#     origin.pull()
#     return 'Updated PythonAnywhere successfully', 200



@app.route('/update_server', methods=['POST'])
def webhook():
  if request.method == 'POST':
    repo = git.Repo('/home/Pranav2003/Dummy-app')
    # Clone the repository to a local directory
    # repo = git.Repo.clone_from('https://github.com/malpani2003/Dummy-app.git', '/home/Pranav2003/Dummy-app')
    # Fetch and merge the latest changes from the remote repository
    repo.git.stash()
    repo.remotes.origin.fetch()
    repo.remotes.origin.pull()
    repo.git.stash('apply')
    # Restart the server to apply the changes
    # Replace this line with code to restart your specific server
    return 'Server updated successfully', 200

# By default route requets are GET in nature
@app.route("/")
def home():
    return jsonify("Hello")

# / is the index route or home route
@app.route("/store",methods=["POST"])
def create_store():
    request_data=request.get_json()
    new_store={
        "name":request_data['name'],
        "items":[]
    }
    stores.append(new_store)
    return jsonify(new_store)

    pass

@app.route("/store/<string:name>")  # /store/some_name then some_name will be assigned to name variable in function
def get_store(name):
    Found=0
    for ele in stores:
        if ele["name"].lower()==name.lower():
            Found=1
            return jsonify(ele)
        else:
            continue
    if(Found==0):
        return jsonify({
            "Error":"No Store Found"
        })


@app.route("/store")
def get_all_store():
    return jsonify({"stores":stores})  # jsonify convert list to json data
    # pass


@app.route("/store/<string:name>/item")
def get_item_in_store(name):
    Found=0
    for ele in stores:
        if ele["name"].lower()==name.lower():
            Found=1
            return jsonify({"Items":ele["items"]})
        else:
            continue
    if(Found==0):
        return jsonify({
            "Error":"No Store Found"
        })


@app.route("/store/<string:name>/item",methods=["POST"])
def create_item_store(name):
    request_data=request.get_json() # to get json data from api request
    for ele in stores:
        if ele["name"].lower()==name.lower():
            new_item={
        "item":request_data["name"],
        "price":request_data["price"]
    }
            ele["items"].append(new_item)
            return jsonify({"Items":ele["items"]})
    return jsonify({
            "Error":"No Store Found"
        })

if __name__=="__main__":
    app.run()


# {  "name": "Test",
#      "username": "TheTestUser123",
#      "email": "TheTestUser123@gmail.com",
#      "oldPassword":"testcbv323",
#      "password":"testcbv"
# }