from tkinter import *
from projectoxford.speech import SpeechClient
import shelve
import CreateProfile
import EnrollProfile
import VerifyFile
import recording
#import random
#import tkinter as tk

d = shelve.open("projectDatabase")
#Initialise the votes if there are none stored
if (not "Trump" in d) or (not "Hillary" in d):
    d["Trump"] = 0
    d["Hillary"] = 0

verifKey = "b59409633b324dd183ee08edb6e498f2"
sc = SpeechClient("7f94930a0af8458aaf9e58e189d4d32f", gender='Female', locale='en-US')

TITLE_FONT = ("Helvetica", 18, "bold")

class Prog:
    def __init__(self, master):
        self.master = master
        self.count = 0
        self.name = ""
        self.entryFrame = Frame(master)
        EnrolFrame1 = Frame(master)
        self.EnrolFrame2 = Frame(master)
        NameExistsFrame = Frame(master)
        VerifyFrame1 = Frame(master)
        VerifyFrame2 = Frame(master)
        self.VoteFrame1 = Frame(master)
        self.VoteFrame2 = Frame(master)

        frames = (self.entryFrame, EnrolFrame1, self.EnrolFrame2, NameExistsFrame, VerifyFrame1, VerifyFrame2, self.VoteFrame1, self.VoteFrame2)

        for frame in frames:
            frame.grid(row=0, column = 0, sticky = 'news')

        #Populate Entry Frame
        Label(self.entryFrame, text = "Enrolment and Verification", font = TITLE_FONT).pack()
        Button(self.entryFrame, text="ENROL NEW USER", fg="red", command=lambda: self.raise_frame(EnrolFrame1)).pack(side=LEFT)
        Button(self.entryFrame, text="VERIFY USER FOR VOTE", fg="blue", command=lambda: self.raise_frame(VerifyFrame1)).pack(side=RIGHT)
        Button(self.entryFrame, text="SEE VOTES", command=lambda: self.updateVotes()).pack()

        #Populate Enrolment Frame
        self.e = Entry(EnrolFrame1)
        self.e.delete(0,END)
        self.e.insert(0,"Type name to enrol")
        self.e.pack()
        Button(EnrolFrame1, text="Create Profile", fg="red", command=self.createProfile).pack()
        Button(EnrolFrame1, text="Back to start", command= lambda:self.raise_frame(self.entryFrame)).pack()

        #Populate Verify Frame
        self.a = Entry(VerifyFrame1)
        self.a.delete(0, END)
        self.a.insert(0, "Type name to verify")
        self.a.pack()
        Button(VerifyFrame1, text="Verify", fg="red", command=self.getName).pack()
        Button(VerifyFrame1, text="Back to start", command=lambda: self.raise_frame(self.entryFrame)).pack()

        #Populate Vote Frame
        Button(self.VoteFrame1, text="Vote Trump!", fg="red", command=lambda: self.v1(True, self.name)).pack()
        Button(self.VoteFrame1, text="Vote Hillary!", fg="blue", command=lambda: self.v1(False, self.name)).pack()

        #Populate Results Frame
        Label(self.VoteFrame2, text="Trump Votes: "+str(d["Trump"])).pack()
        Label(self.VoteFrame2, text="Hillary Votes: "+str(d["Hillary"])).pack()
        Button(self.VoteFrame2, text="Back to start", command=lambda: self.raise_frame(self.entryFrame)).pack()

        self.raise_frame(self.entryFrame)

    def raise_frame(self, frame):
        frame.tkraise()

    def createProfile(self):
        name = self.e.get()
        name = name.strip().lower()
        if name == "type name to enrol":
            sc.print("Please enter a valid name.")
        elif name in d:
            #Prevents 2 people from having the same name.
            sc.print("That name already exists, please use another.")
        else:
            #Creates a profile***
            self.profileId = CreateProfile.create_profile(verifKey, 'en-us')
            #Start the enrolment process.
            self.enrolVoice(name)

    def enrolVoice(self, name):
        #Enrol 3 times.
        sc.print("You will be asked to repeat a passphrase three times for enrolment")
        while self.count < 3:
            sc.print("Please say; You can get in without your password")
            #Record the user to a file
            recording.record_to_file('enrol.wav')
            #Enrol using the file recorded, update the count***
            self.count = EnrollProfile.enroll_profile(verifKey, self.profileId, 'enrol.wav')
            #print(self.count)
            #self.count += 1
            sc.print("Voice recorded.")
        #Save the name and profile ID in the database
        d[name] = [self.profileId, 0]
        sc.print("Enrolment completed, thank you.")
        self.count = 0
        self.raise_frame(self.entryFrame)

    def getName(self):
        name = self.a.get()
        name = name.strip().lower()

        if name in d:
            profileId = d[name][0]
            if d[name][1] > 0:
                sc.print("Your name is in the database, but you have already voted.")
                return
            sc.print("Name found in database, please say; You can get in without your password")
            #Record the user to a file
            recording.record_to_file('verify.wav')
            #Verify using the file recorded***
            verified = VerifyFile.verify_file(verifKey, 'verify.wav', profileId)
            #print(verified)
            #verified = True
            if verified:
                sc.print("Verification successful, please follow the on-screen prompts to submit your vote.")
                self.raise_frame(self.VoteFrame1)
                self.name = name
            else:
                sc.print("Sorry, your voice does not match the name provided.")
        else:
            sc.print("Sorry, your name was not found in the database, please enrol first or double check the name you entered.")

    def v1(self, vote, name):
        if vote:
            sc.print("Thank you for voting Trump, have a nice day.")
            self.raise_frame(self.entryFrame)
            d[name] = [d[name][0], d[name][1]+1]
            print(d[name][1])
            d["Trump"] += 1
        else:
            sc.print("Thank you for voting Hillary, have a nice day.")
            self.raise_frame(self.entryFrame)
            d[name][1] = 1
            d["Hillary"] += 1
        #Update the results frame
        self.updateVotes()

    def updateVotes(self):
        self.raise_frame(self.VoteFrame2)
        self.VoteFrame2.destroy
        self.VoteFrame2 = Frame(self.master)
        self.VoteFrame2.grid(row=0, column = 0, sticky = 'news')
        Label(self.VoteFrame2, text="Trump Votes: " + str(d["Trump"])).pack()
        Label(self.VoteFrame2, text="Hillary Votes: " + str(d["Hillary"])).pack()
        Button(self.VoteFrame2, text="Back to start", command=lambda: self.raise_frame(self.entryFrame)).pack()


if __name__ == '__main__':
    root = Tk()
    prog = Prog(root)
    root.mainloop()