import mysql.connector
import UserManager

# connection = mysql.connector.connect(user = "YourAdventureAdmin",
#                         database = "YourAdventureDB",
#                         host = "localhost",
#                         password = "admin123321"
#                         )
def main():
    credentials = UserManager.get_credentials(input())
    if not credentials:
        return
    try: 
        connection = mysql.connector.connect(
        user = credentials["username"],
        database = credentials["database"],
        password = credentials["password"],
        host = credentials["host"]
        )
    except mysql.connector.Error as err:
        print("Error: " , err.msg)
        return
    cursor = connection.cursor()
    if connection.is_connected():
        print("Successful login.\n")

if __name__ == "__main__":
    main()