import argparse
from datetime import date

from bots import Bot1
from students import Student
from dataVisualizers import dataVisualizer

if __name__ == '__main__':  
    parser = argparse.ArgumentParser(
        description = "CLI to check the attendance!",
        epilog = "Created with ❤ by Jaidheer"
    )
    parser.add_argument(
        '--userid', '--uid', '-u', 
        metavar = 'User ID', 
        nargs = '?',
        type = str,
        default = 'Add default user id', 
        required = False,
        help = 'User ID',
    )
    parser.add_argument(
        '--password', '--pwd', '-p', 
        metavar = 'password', 
        nargs = '?',
        default = 'add default password', 
        required = False,
        help = 'Password',
    )

    parser.add_argument(
        '--today', '--td', '-t', 
        metavar = 'today', 
        nargs = '?',
        type = bool,
        const = True,
        default = False, 
        required = False,
        help = 'Get present day attendance',
    )

    args = parser.parse_args()
    # print(args.today)

    userData = {
        'uid': args.userid,
        'pwd': args.password
    }

    bot1 = Bot1(userData = userData)
    try:
        bot1.checkInternet()
        bot1.getVitalData()
        bot1.makeLogin()
        bot1.getAttendanceURL()
        
        if args.today:
            today = date.today().strftime(r"%d-%m-%Y")
            student1 = Student(rawData = bot1.getAttendanceRD(fDate = today, tDate = today))            
        else:
            student1 = Student(rawData = bot1.getAttendanceRD())
        
        dv1 = dataVisualizer(student = student1)
        dv1.printAttTable()

    except Exception as exp:
        print("Got an Error")
        print(exp)
