#Copyright by iiit-delhi for project IAP(Institute admission process) , Follows SRP,OCP,LSP principle, Done by subham nikhil and shubham mishra
# In this IAP user can have option to select multiple Branch and Course for which they want admission process to run. With integrated Payment mode.
import uuid
import datetime
import sqlite3
import math

#Controling attribute for selection 
total_seat=1
interview_sel_factor=3
final_sel_factor=3

#All Registration are in one class follow SRP principle and OCP principle
class Registration:

#default constructor
    def __init__(self,dbConn,BranchTableName,courese_name):
        self.db = dbConn
        self.dbTableName=BranchTableName
        self.courese_name=courese_name

#taking input and storing into database
    def set_Details(self):
        student_details={}
#generation of unique id as courese_name+year+randomnumber        
        student_details['id']=self.courese_name+str(datetime.date.today().year)+uuid.uuid4().hex[:5]
        print("Enter details for registration: ")
        student_details['name'] = input("Enter your Name*: ")
        student_details['address'] = input("Enter your address*: ") 
        student_details['ph_number'] = int(input("Enter your ph_number*: "))
        student_details['email'] = input("Enter your Email*: ")  
        student_details['degree_eligible'] = input("Enter your Degree Name as*: ") 
        student_details['degree_cgpa'] = float(input("Enter your degree Percentage*: "))  
        self.db.execute("CREATE TABLE IF NOT EXISTS '{}'(id TEXT,name TEXT, address TEXT, ph_number INT,email TEXT,degree_eligible TEXT,degree_cgpa REAL,status TEXT not null default 'TRUE',test_mark REAL not null default 0.0,interview_mark REAL not null default 0.0)".format(self.dbTableName))
        query = "insert into " +str(self.dbTableName)+ " " + str(tuple(student_details.keys())) + " values" + str(tuple(student_details.values())) + ";"
        self.db.execute(query)
        self.db.commit()
        #self.db.close()        

#All reports are in report class which follow SRP principle
class report:

#default constructor
    def __init__(self,dbConn,BranchTableName):
        self.db = dbConn
        self.dbTableName=BranchTableName


# displaying result of accepted candidates after checking of aplication
    def accepted_application(self):
        cursor = self.db.cursor()
        query="select * from '{}' where status='TRUE'".format(self.dbTableName)
        cursor.execute(query)
        rows = cursor.fetchall()
        print("#####This many Application selected for Test#####\n")
        for row in rows:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("ADDRESS = ", row[2])
            print("PHONE NUMBER = ", row[3],)
            print("EMAIL= ", row[4],"\n")
            
        cursor.close()
       # self.db.close()

#merit list method
    def merit_list(self):

        cursor = self.db.cursor()
        query="select test_mark,degree_cgpa,id from '{}' where status='TRUE'".format(self.dbTableName)
        cursor.execute(query)
        rows = cursor.fetchall()

    #aggregate marks calculation

        for row in rows:
            stage2_marks=round(0.1*row[1]+0.9*row[0],2)
            query="update '{}' set test_mark={} WHERE id='{}'".format(self.dbTableName,stage2_marks,row[2])
            self.db.execute(query)
            self.db.commit()

    #if candidate aggregate marks is less than required marking Flase or un selected
        query="select test_mark from '{}' where status='TRUE' order by test_mark DESC limit {}".format(self.dbTableName,interview_sel_factor)
        cursor.execute(query)
        rows = cursor.fetchall()
        print("cut-off marks for selection is:",rows[interview_sel_factor-1][0])
        query="update '{}' set status='FALSE' WHERE test_mark<{}".format(self.dbTableName,rows[interview_sel_factor-1][0])   
        self.db.execute(query)
        self.db.commit()

    # Display selected candidate after test
        query="select * from '{}' where status='TRUE' order by test_mark DESC limit {}".format(self.dbTableName,interview_sel_factor)
        cursor.execute(query)
        rows = cursor.fetchall()
        print("#####This many Application selected for Interview#####\n")
        for row in rows:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("ADDRESS = ", row[2])
            print("PHONE NUMBER = ", row[3],)
            print("EMAIL= ", row[4],) 
            print("Agregated_marks= ", row[8],"\n")
        cursor.close()
        #self.db.close()    

# final merit list methond after interview and cacluation for wait-list candidates
    def final_merit_list(self,Total_eligible_candidate):

        cursor = self.db.cursor()
        query="select interview_mark,test_mark,id from '{}' where status='TRUE'".format(self.dbTableName)
        cursor.execute(query)
        rows = cursor.fetchall()

    #aggregate marks calculation after interview
        for row in rows:
            stage3_marks=round(0.3*row[0]+0.7*row[1],2)
            query="update '{}' set interview_mark={} WHERE id='{}'".format(self.dbTableName,stage3_marks,row[2])
            self.db.execute(query)
            self.db.commit()

    #if candidate aggregate marks is less than required marking Flase or unselected    
        query="select interview_mark from '{}' where status='TRUE' order by interview_mark DESC limit {}".format(self.dbTableName,final_sel_factor)
        cursor.execute(query)
        rows = cursor.fetchall()
        print("cut-off marks for final selection is:",rows[final_sel_factor-1][0])
        query="update '{}' set status='FALSE' WHERE interview_mark<{}".format(self.dbTableName,rows[final_sel_factor-1][0])   
        self.db.execute(query)
        self.db.commit()

    # Display selected candidate after interview
        query="select * from '{}' where status='TRUE' order by interview_mark DESC limit {}".format(self.dbTableName,total_seat)
        cursor.execute(query)
        rows = cursor.fetchall()
        print("#####Selected candidate for our courese Programe:#####\n")
        for row in rows:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("ADDRESS = ", row[2])
            print("PHONE NUMBER = ", row[3],)
            print("EMAIL= ", row[4],) 
            print("Agregated_marks= ", row[9],"\n")

    #waitlist print
        waitlistNumber=int(math.ceil(((Total_eligible_candidate-total_seat)*0.5)))

        if waitlistNumber==0:
            print("#####There is No wait listed candidate#####\n")
        else:    
            query="select * from '{}' where status='TRUE' order by interview_mark DESC limit {} OFFSET {}".format(self.dbTableName,waitlistNumber,total_seat)
            cursor.execute(query)
            rows = cursor.fetchall()
            print("#####This many Application are wait listed candidate#####\n")
            for row in rows:
                print("ID = ", row[0])
                print("NAME = ", row[1])
                print("ADDRESS = ", row[2])
                print("PHONE NUMBER = ", row[3],)
                print("EMAIL= ", row[4],) 
                print("Agregated_marks= ", row[9],"\n")        
            cursor.close()
            #self.db.close() 

    # Admission letter method
    def Admissionletter(self,row):
        if row !='0':
            print("##### Congrats Your Provisanal offer letter for xyz program ################")
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("EMAIL = ", row[2])
            print("PHONE NUMBER = ", row[3],)
        else:
            print("")


#core logic of IAP are in application class which given work of relationship 
class application:

#default constructor
    def __init__(self,dbConn,BranchTableName):
        self.db = dbConn
        self.dbTableName=BranchTableName

# application checking process if any field is missing application is rejected
    def check_application(self):
        cursor = self.db.cursor()
        query="select * from '{}'".format(self.dbTableName)
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            if '' in row:
                query="update '{}' set status='FALSE' WHERE id='{}'".format(self.dbTableName,row[0])
                self.db.execute(query)
                self.db.commit()
        cursor.close()
      

# Test methond directly putting random value from 0 to 100 into database 
    def test(self):
        cursor = self.db.cursor()
        query="update '{}' set test_mark=abs(random() % 100) WHERE status='TRUE'".format(self.dbTableName)
        self.db.execute(query)
        self.db.commit()

        cursor.close()
        print("Test is Over")

# taking interview on random nature and allocating marks from 0 to 100
    def interview(self):
        cursor = self.db.cursor()
        query="update '{}' set interview_mark=abs(random() % 100) WHERE status='TRUE'".format(self.dbTableName)
        self.db.execute(query)
        self.db.commit()

        cursor.close()
        print("Interview is Over")


# method to check total number of selected candiates
    def Total_eligible_candidate(self):

        cursor = db.cursor()
        query="select count(*) from '{}' where status='TRUE'".format(self.dbTableName)
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print('')
        cursor.close()
        return row

# method to check total number of  candiates apply for program
    def Total_candidate(self):

        cursor = self.db.cursor()
        query="select count(*) from '{}'".format(self.dbTableName)
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print('')    
        cursor.close()
        return row


#payment class for fee related function
class payment():

#default constructor
    def __init__(self,dbConn,BranchTableName):
         #report.__init__(self,dbConn,BranchTableName)
         self.db = dbConn
         self.dbTableName=BranchTableName

    fid='0'
    AdmissionletterPrint='0'
    def getFeeId(self):
        return self.fid

    def setFeeId(self):
        self.fid=input("Enter ID for fee payment:")

    def getAdmissionletterPrint(self):
        return self.AdmissionletterPrint

    # fee payment method
    def fee(self):
        cursor = self.db.cursor()
        query="select id,name,email,ph_number from '{}' where status='TRUE' order by interview_mark DESC limit {}".format(self.dbTableName,total_seat)
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            if self.fid in row[0]:
                print("Payment sucessfull")
                # r2=report(self.db,self.dbTableName)
                # r2.Admissionletter(row)
                self.AdmissionletterPrint=row
            else:
                print("ID is not valid")
                self.AdmissionletterPrint='0'



#LSP principle inheritance of all class in one
class IAP(report,application,Registration,payment) :
    
#default constructor
    def __init__(self,dbConn,BranchTableName,courese_name):
        report.__init__(self,dbConn,BranchTableName)  
        application.__init__(self,dbConn,BranchTableName)
        payment.__init__(self,dbConn,BranchTableName)    
        Registration.__init__(self,dbConn,BranchTableName,courese_name)    

    def main_run(self):

        #object creation
        a1=application(self.db,self.dbTableName)
        r1=report(self.db,self.dbTableName)
        s1=Registration(self.db,self.dbTableName,self.courese_name)
        p1=payment(db,BranchName[1])

        #Multiple details capture
        operation=input("Registration Process select 1,for exit press 0:")
        while operation!='0':
            s1.set_Details() 
            operation=input("Press any number For continue Registration, for exit press 0 :")
        #print("Total Application of candidates are:\n")
        total_cand=a1.Total_candidate()[0]

        #checking if min candidate required for application
        if int(total_cand)>=total_seat and int(total_cand)>=interview_sel_factor and int(total_cand)>=final_sel_factor:
            
            #Now stage 1 Check Application of candidates:
            a1.check_application()
            r1.accepted_application()
            #Now stage 2 Test of candidates:
            a1.test()
            r1.merit_list()
            #Now stage 3 Interview of candidates:
            a1.interview()
            r1.final_merit_list(a1.Total_eligible_candidate()[0])
            #Now stage 4 Paymnet of fee for selected candidates:
            p1.setFeeId()
            p1.fee()
            r1.Admissionletter(p1.getAdmissionletterPrint())
        else:
            print("Not enough candiate apply hence cource cancelled")



#Main running of code begin down

#db connection
db = sqlite3.connect("IAddProcees.db")
# multiple branch and courese selection follow OCP principle
BranchName=["ECEV2020","CSEM2020","BIOM2020"]
Coursename=["MT","BT"]

i1 = IAP(db,BranchName[1],Coursename[0])
i1.main_run()

db.close()