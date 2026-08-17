import pymysql
#  pip install pymysql

# host/url = aws.cskgskg.com localhost
# user = root
# password = 
# port = 3306

connection = pymysql.connect( host="localhost", user="root", password="15081947", port=3306, database="gen_ai_b2_db" )

# insert_query = "insert into users(name, email, interested_course) values( %s, %s, %s);"

# cursor = connection.cursor()

# cursor.execute( insert_query, ('c', 'c@b.com', 'ccom') )

# connection.commit() # insert, update, delete
# connection.close()

get_query = "select * from users;"

cursor = connection.cursor()

cursor.execute(get_query)

data = cursor.fetchall()

connection.close()

print( data )



















