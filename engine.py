from connect import get_cursor
from heapq import heappush
from datetime import datetime, timedelta
from random import randint


class Course():
    def __init__(self):
        self.TypeID=0
        self.modules=[]
class DataBase():
    def __init__(self):
        self.cursor=get_cursor()
        query="SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='u_magorski'"
        self.cursor.execute(query)
        self.table_names=[x[0] for x in self.cursor.fetchall()]
        self.table_names.remove('sysdiagrams')
        self.table_dict={}
    def get_table(self,table):
        self.cursor.execute("select * from {}".format(table))
        return self.cursor.fetchall()
    def load(self):
        for table in self.table_names:
            self.table_dict[table]=self.get_table(table)
    def sort_mod(self):
        self.cursor.execute("select ModuleID,m.CourseID,TypeID from Modules as m inner join Courses as c on m.CourseID=c.CourseID order by m.CourseID")
        self.courseModules=[Course() for _ in range(21)]
        for m_id,c_id,t_id in self.cursor.fetchall():
            self.courseModules[c_id].TypeID=t_id
            self.courseModules[c_id].modules.append(m_id)
    def generate_mod_table(self):
        self.sort_mod()
        f=open('modtab','r')
        cal=[]
        mod_id=1
        for id in range(1,21):
            c_id,begin,duration=f.readline().split(',')
            begin=datetime.strptime(begin,"%Y-%m-%d %H:%M:%S")
            duration=datetime.strptime(duration,"%H:%M\n").time()
            for i,module in enumerate(self.courseModules[id].modules):
                cal.append((mod_id,begin+timedelta(days=i),module,duration))
                mod_id+=1
        f.close()
        return cal
    def load_products(self):
        self.products=[set() for _ in range(1001)]
        p=[0 for _ in range(121)]
        f=open('prodsum_man','r')
        for _ in range(2100):
            stud,prod=f.readline().split(',')
            stud,prod=int(stud),int(prod)
            self.products[stud].add(prod)
            p[prod]+=1
        print(p)
    def generate_payments(self):
        f1=open('q1','w')
        f2=open('q2','w')
        f3=open('q3','w')

        self.load_products()
        self.course_payment=[]
        self.webinar_payment=[]
        self.event_payment=[]
        for s_i in range(1001):
            for p_id in self.products[s_i]:
                type=self.table_dict['Products'][p_id-1][1]
                if type==1:
                    self.cursor.execute("select WebinarID, Price, DateTimeOfWebinar from Webinars where ProductID="+str(p_id))
                    w_id,price, date = self.cursor.fetchone()
                    # new_date=min(datetime.now()+timedelta(days=1),(date-timedelta(days=randint(1,3))))
                    new_date=date-timedelta(days=randint(1,3))

                    self.webinar_payment.append((new_date,s_i,w_id,1))
                    query="insert into WebinarPurchase values ({},'{}',{},{},{});".format(len(self.webinar_payment),new_date,s_i,w_id,1)
                    f1.write("({},'{}',{},{},{}),\n".format(len(self.webinar_payment),new_date,s_i,w_id,1))
                elif type==2:
                    query="select m.CourseID,LimitOfParticipants,Price,Advance,EventDate from Courses as c inner join Modules as m on c.CourseID = m.CourseID inner join CourseTimetable as ct on m.ModuleID = ct.ModuleID  where c.ProductID="+str(p_id)
                    self.cursor.execute(query)
                    earliest_date=datetime(2025,1,1,1,1,1)
                    for c_id,oulimit,price,advance,date in self.cursor.fetchall():
                        earliest_date=min(earliest_date,date)
                    # new_date=min(datetime.now()+timedelta(days=1),earliest_date-timedelta(days=randint(4,7)))
                    new_date=earliest_date-timedelta(days=randint(4,7))

                    self.course_payment.append((s_i,c_id,new_date,1))
                    query="insert into CoursePayment values ({},{},{},'{}',{});".format(len(self.course_payment),s_i,c_id,new_date,1)
                    f2.write("({},{},{},'{}',{}),\n".format(len(self.course_payment),s_i,c_id,new_date,1))
                elif type==3:
                    query="select EventID,s.LimitOfParticipants, EventDate, PriceRegular,EntryFee from StudyTimetable as st inner join StudySubjectCourses as c on st.CourseID = c.CourseID inner join Studies S on c.StudyID = S.StudyID where s.ProductID="+str(p_id)
                    self.cursor.execute(query)
                    earliest_date=datetime(2025,1,1,1,1,1)
                    for e_id,limit,date, price,entry in self.cursor.fetchall():
                        # new_date=min(datetime.now()+timedelta(days=1),date-timedelta(days=randint(4,7)))
                        new_date=date-timedelta(days=randint(4,7))
                        self.event_payment.append((new_date,1,e_id,s_i))
                
                        query="insert into StudyEventPayment values ({},'{}',{},{},{});".format(len(self.event_payment),new_date,1,e_id,s_i)
                        f3.write("({},'{}',{},{},{}),\n".format(len(self.event_payment),new_date,1,e_id,s_i))
                elif type==4:
                    query="select EventID,LimitOfParticipants, EventDate, PriceSingle from StudyTimetable as st inner join StudySubjectCourses as c on st.CourseID = c.CourseID where st.ProductID="+str(p_id)
                    self.cursor.execute(query)
                    e_id,limit,date,price = self.cursor.fetchone()
                    # new_date=min(datetime.now()+timedelta(days=1),date-timedelta(days=randint(3,7)))
                    new_date=date-timedelta(days=randint(4,7))

                    self.event_payment.append((new_date,1,e_id,s_i))
                    query="insert into StudyEventPayment values ({},'{}',{},{},{});".format(len(self.event_payment),new_date,1,e_id,s_i)
                    f3.write("({},'{}',{},{},{}),\n".format(len(self.event_payment),new_date,1,e_id,s_i))
        f1.close()
        f2.close()
        f3.close()
    def generate_enroll(self):
        self.load_products()
        f2=open('e2','w')
        f3=open('e3','w')
        f4=open('e4','w')
        c_1=1
        c_2=1
        c_3=1
        for s_id,products in enumerate(self.products):
            for p_id in products:
                type=self.table_dict['Products'][p_id-1][1]
                if type==2:
                    query="select DateOfPayment,Paid from CoursePayment where StudentID={} and CourseID={}".format(s_id,p_id-50)
                    self.cursor.execute(query)
                    date,paid=self.cursor.fetchone()
                    if paid or (not paid and p_id%2):
                        f2.write("({},'{}',{},{}),\n".format(c_1,date,p_id-50,s_id))
                        c_1+=1
                if type==3:
                    query="select top 1 EventDate from StudyTimetable as st inner join StudySubjectCourses as sc on st.CourseID=sc.CourseID inner join Studies as s on sc.StudyID=s.StudyID where s.ProductID={} order by EventDate".format(p_id)
                    self.cursor.execute(query)
                    date=self.cursor.fetchone()[0]
                    f3.write("({},{},{},{}),\n".format(c_2,date-timedelta(days=7),s_id,p_id-70))
                    c_2+=1
                if type==4:
                    query="select PaymentDate,Paid from StudyEventPayment where EventID={} and StudentID={}".format(p_id-80,s_id)
                    self.cursor.execute(query)
                    date,paid=self.cursor.fetchone()
                    if paid or (not paid and p_id%2):
                        f4.write("({},{}),\n".format(s_id,p_id-80))
                        c_3+=1
        f2.close()
        f3.close()
        f4.close()
    def generate_practise(self):
        f=open('practise','w')
        dates=open('sampledates','r')
        for row in self.table_dict['StudyEnrollment']:
            operator=randint(1,10)
            id,d,s_id,c_id=row
            if operator<9:
                date = dates.readline()
                if date=='':
                    dates.close()
                    dates=open('sampledates','r')
                    date=dates.readline()

                date=datetime.strptime(date,"%Y-%m-%d\n")
                f.write("({},{},'{}','{}'),\n".format(c_id,s_id,date,date+timedelta(days=randint(7,14))))
            if operator<7:
                date = dates.readline()
                if date=='':
                    dates.close()
                    dates=open('sampledates','r')
                    date=dates.readline()

                date=datetime.strptime(date,"%Y-%m-%d\n")
                f.write("({},{},'{}','{}'),\n".format(c_id,s_id,date,date+timedelta(days=randint(7,14))))
            
        f.close()

    def generate_course_attendace(self):
        f=open('c_at','w')
        query="select CourseID,StudentID from CourseEnrollment"
        self.cursor.execute(query)
        rows=self.cursor.fetchall()
        for c_id,s_id in rows:
            query="select EventID from CourseTimetable as ct inner join Modules as m on ct.ModuleID=m.ModuleID where CourseID="+str(c_id)
            self.cursor.execute(query)
            
            for e_id in self.cursor.fetchall():
                operator=randint(1,10)
                if operator<9:
                    f.write("({},{}),\n".format(s_id,e_id[0]))
        f.close()
    def generate_study_attendace(self):
        f=open('s_at','w')
        query="select StudentID,StudyID from StudyEnrollment"
        self.cursor.execute(query)
        rows=self.cursor.fetchall()
        for s_id,c_id in rows:
            query="select EventID from StudyTimetable as st inner join StudySubjectCourses as sc on st.CourseID=sc.CourseID where StudyID="+str(c_id)
            self.cursor.execute(query)
            
            for e_id in self.cursor.fetchall():
                operator=randint(1,10)
                if operator<9:
                    f.write("({},{}),\n".format(e_id[0],s_id))
        query="select * from EventGuest"
        self.cursor.execute(query)
        s_id,e_id=self.cursor.fetchone()
        operator=randint(1,10)
        if operator<9:
            f.write("({},{}),\n".format(e_id,s_id))
        f.close()


        



                    

               
def check_cal_web(baza):
    cal=[]
    for log in baza.table_dict['Webinars']:
        id, title, link, price, id2, date, duration, id3, id4 = log
        end=date+timedelta(hours=duration.hour, minutes=duration.minute)
        cal.append((date,id,1))
        cal.append((end,id,-1))
    cal.sort(key=lambda x:x[0])
    sum=0
    for x,y,z in cal:
        sum+=z
        if sum>1:
            print(x,y,z)
def check_cal_courses(baza):

    cal=[]
    for log in baza.table_dict['CourseTimetable']:
        id, date,id2,duration = log
        end=date+timedelta(hours=duration.hour, minutes=duration.minute)
        cal.append((date,id,1))
        cal.append((end,id,-1))
    cal.sort(key=lambda x:x[0])
    sum=0
    for x,y,z in cal:
        sum+=z
        if sum>1:
            print(x,y,z)       

baza=DataBase()
baza.load()
# baza.generate_study_attendace()
foo=0
# baza.generate_enroll()
# baza.load_products()







# baza.generate_payments()
# baza.cursor.execute("select PaymentID, DateOfPayment from CoursePayment where PaymentID in (50,100,150,200,250);")
# for id,row in enumerate(baza.cursor.fetchall()):
#     print("({},'{}',{}),".format(id+1,row[1],row[0]))