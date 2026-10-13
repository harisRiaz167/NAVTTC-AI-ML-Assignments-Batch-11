print("==============================================")
print("     SERVER & DATABASE COST CALCULATOR")
print("==============================================")
name = input("Please enter your name: ")
servers = []
servers_price = []
while(True):
    server = input("Please input server name : ")
    server_cost = float(input(f"Please enter cost for {server} :"))
    servers.append(server)
    servers_price.append(server_cost)
    another = input("Do you want to add another server ? (Y/N) : ")
    if(another.lower() == "y"):
        continue
    else:
        break


databases = []
databases_price = []
while(True):
    database = input("Please input database name : ")
    database_cost = float(input(f"Please enter cost for {database} : "))
    databases.append(database)
    databases_price.append(database_cost)
    another = input("Do you want to add another server ? (Y/N) : ")
    if(another.lower() == "y"):
        continue
    else:
        break 

storage = float(input("Please enter the storage required in GB : "))
storage_cost_per_GB = float(input("Please enter the storage cost per GB : "))
storage_cost = storage * storage_cost_per_GB

backup = float(input("Please enter the backup required in GB : "))
backup_cost_per_GB = float(input("Please enter the backup cost per GB : "))
backup_cost = backup * backup_cost_per_GB

server_costs = sum(servers_price)
database_costs = sum(databases_price)
monthly_cost = server_cost + database_cost + storage_cost + backup_cost 
yearly_cost = monthly_cost * 12

if(monthly_cost < 100):
    deployment_level = "BUDGET"
elif(monthly_cost < 200):
    deployment_level = "STANDARD"
elif(monthly_cost >= 200):
    deployment_level = "PERFORMANCE"

discount = 0
annual_discount_confirmation = input("\nDo you want to pay annual price and get a discount? (Y/N) : ")
if(annual_discount_confirmation.lower() == "y"):
    discount = yearly_cost * 0.15
    final_yearly_cost = yearly_cost - discount
else:
    final_yearly_cost = yearly_cost 


print("\n\n")
print("==============================================")
print("           CLOUD INFRASTRUCTURE BILL")
print("==============================================")
print(f"\nDeveloper name : {name}")
print("\n--------------- SERVERS ---------------------")
for i in range(len(servers)):
    print(f"{i + 1}. {servers[i]} - ${servers_price[i]:.2f}")
print("\n--------------- DATABASES -------------------")
for i in range(len(databases)):
    print(f"{i + 1}. {databases[i]} - ${databases_price[i]:.2f}")
print("\n--------------- COST SUMMARY ----------------")
print(f"Server Cost       : ${server_cost:.2f}")
print(f"Database Cost     : ${database_cost:.2f}")
print(f"Storage Cost      : ${storage_cost:.2f}")
print(f"Backup Cost       : ${backup_cost:.2f}")
print("----------------------------------------------")
print(f"Monthly Cost      : ${monthly_cost:.2f}")
print(f"Yearly Cost       : ${yearly_cost:.2f}")
print(f"Deployment Level  : {deployment_level}")

if annual_discount_confirmation.lower() == "y":
    print(f"Annual Discount   : ${discount:.2f}")
    print(f"Final Yearly Cost : ${final_yearly_cost:.2f}")
else:
    print("Annual Discount   : $0.00")
    print(f"Final Yearly Cost : ${final_yearly_cost:.2f}")
print("\n==============================================")
print("       THANK YOU FOR USING THE CALCULATOR")
print("==============================================")
