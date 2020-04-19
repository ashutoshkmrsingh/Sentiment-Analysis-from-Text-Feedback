import pymongo


class Db:

    def __init__(self,r,d,p):
        self.review = r
        self.domain = d
        self.polarity = p
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        # creating data base
        self.mydb = myclient['sih2020']
        print(myclient.list_database_names())
        dblist = myclient.list_database_names()
        if "sih2020" in dblist:
            print("The database exists.")
        # creating collection (table) called "customer"
        self.mycol = self.mydb["infomobile"]
        print(self.mydb.list_collection_names())
        self.collist = self.mydb.list_collection_names()
        if "infomobile" in self.collist:
            
            print("The collection infomobile exists.")

    def Insert(self):
    # creating field before insert
        self.myfield = { "Domain": self.domain.lower(), "Review": self.review, "Polarity":self.polarity}
        x = self.mycol.insert_one(self.myfield)
        # print(x.inserted_id)
        # print(x1.inserted_id)
        # print(x.inserted_id)

    # y = mycol.find_one()
    # print(y)

    def Display(self):
        l=[]
        print("________db_Display______________")
        myquery = {"Domain":"mobile"}
        mydoc = self.mycol.find(myquery)
        for _ in mydoc:
            l.append(_)
            print(_)
        print("_____________db_display end_____________")
        return l
        # print("List")
        # print(l[1])

    def Delete(self):

        x = self.mycol.delete_many({})

        print(x.deleted_count, " documents deleted.")

    def Insert_Aspect(self):
        # take input dict as ver. temp
        temp = {('camera'):[0.4, 0, 0.6],('battery'):[0.3, 0, 0.5],('display'):[0.4, 0.6, 0],
                 ('charging'):[0, 0, 0],
                 ('sound'):[0, 0, 0],('processor'):[0,0,0],
                 ('price'):[0,0,0],('security'):[0,0,0]}
        for _ in temp.keys():
            self.myfield = { "Aspect": _, "Polarity":temp[_]}
            x = self.mycol.insert_one(self.myfield)

    def Display_Aspect(self):
        # take inpute of Aspect as ver. temp2
        temp2 = 'camera'
        l3=[]
        print("________db_Display_Aspect______________")
        myquery = {"Aspect":temp2}
        mydoc = self.mycol.find(myquery)
        for _ in mydoc: 
            l3.append(_)
            print(_)
        print("_____________db_display_Aspect end_____________")
        return l3 
        # print("List")
        # print(l[1])