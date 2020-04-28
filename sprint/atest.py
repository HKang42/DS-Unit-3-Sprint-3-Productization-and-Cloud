import openaq 
api = openaq.OpenAQ()
status, body = api.cities()
print("\nStatus", status)
#print("\nBody",body)

for item in body:
    print(item)

print("\nmeta")
print("length of meta", len(body["meta"]), "\n")
for item in body["meta"]:
    print(item)


print("\nresults")
print("length of results", len(body["results"]), "\n" )
print("results keys", body["results"][0].keys(), '\n')
print("first 5 items in results")
for item in body["results"][0:5]:
    print(item)


print("\n\nCity = LA, Param = pm25")
status, body = api.measurements(city='Los Angeles', parameter='pm25')

print("\nresults")
print("length of results", len(body["results"]), "\n" )
print("results keys", body["results"][0].keys(), '\n')
print("first 5 items in results")
for item in body["results"][0:5]:
    print(item)


data = body["results"]
time_list = []

for point in data:
    time = point["date"]["utc"]
    value = point["value"]
    time_list.append((time, value))

print("\nsample utc_datetime and value")
print("date:", time_list[0][0], "\t\ttype:", type(time_list[0][0]))
print("value:", time_list[0][1], "\ttype:", type(time_list[0][1]))