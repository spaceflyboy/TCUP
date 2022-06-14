# Timesheet Creation and Update Program (TCUP)
import io
import os
import json
from datetime import datetime, timedelta

class TCUP():
    days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    def __init__(self, config_filename: str="tcup-config.txt"):
        self.config_filename = config_filename
        self.config_data = None
        self.hasHeader = False
        self.activeTimesheet = False
    
    def loadConfig(self, 
                    config_filepath="./tcup_config.txt",
                    include_email=True,
                    include_day_name=True,
                    date_format="MLA",
                    include_entry_hours=True, 
                    entry_on_current_day=True,
                    default_name="Default Name"
                    default_email="Default Email"
                    ):
        #https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
        config_file = None
        try:
            config_file = open(self.config_filepath, "w")
        except Exception as e:
            raise e
        
        change_flag = False
        data = None
        if os.path.getsize(config_filepath) == 0: # Empty, brand new config file
            config_file.close()
            data = {"include_email": include_email, 
                    "include_day_name": include_day_name,
                    "date_format": date_format,
                    "include_entry_hours": include_entry_hours,
                    "entry_on_current_day": entry_on_current_day,
                    "default_name": default_name,
                    "default_email": default_email
                    }
            change_flag = True
        else: # Existing config. Make sure it has requisite info, if not add it.
            config_file.close()
            with open(self.config_filepath) as json_file:
                data = json.load(json_file)
            
            if "include_email" not in data:
                data["include_email"] = include_email
                change_flag = True
                
            if "include_day_name" not in data:
                data["include_day_name"] = include_day_name
                change_flag = True
        
            if "date_format" not in data:
                data["date_format"] = date_format
                change_flag = True
            
            if "include_entry_hours" not in data:
                data["include_entry_hours"] = include_entry_hours
                change_flag = True
                
            if "entry_on_current_day" not in data:
                data["entry_on_current_day"] = entry_on_current_day
                change_flag = True
                        
            if "default_name" not in data:
                data["default_name"] = default_name
                change_flag = True
                            
            if "default_name" not in data:
                data["default_name"] = default_name
                change_flag = True
            
            json_file.close()
            
        self.config_data = data
        
        if change_flag: # Need to overwrite config file with new data
            try:
                with open(config_filepath) as json_file:
                    assert isinstance(json_file, io.TextIOBase)
                    json_file.seek(0)
                    json.dump(json.dumps(self.config_data), json_file)
                    json_file.truncate()
                    json_file.close()
            except Exception as e:
                raise e
            
    def format_date(self, date):
        if self.config_data is None:
            self.loadConfig()
        
        assert isinstance(date, datetime.date)
        
        if self.config_data["date_format"] == "MLA":
            return f"{date.day} {months[date.month]}, {date.year}"
        else:
            raise Exception("format_date: Your config contains an unsupported date format")
        
    
    def checkOrCreateHeader(self, user=None, email=None, start_date=None):
        if user is not None:
            assert isinstance(user, str)
        
        if email is not None:
            assert isinstance(email, str)
        
        if start_date is not None: # May need to be adjusted later based on what can be provided as user input
            assert isinstance(start_date, datetime.date)
        
        if self.config_data is None:
            self.loadConfig()
    
        if not self.hasHeader:
        
            
            if self.config_data["include_email"] and email is None and self.config_data["default_email"] == "Default Email":
                raise Exception("Your config requires an email but you haven't set up a default or provided one.")
            
            name = ""
            if user is None:
                name = self.config_data["default_name"]
            else
                name = user
        
            email_ = ""
            if self.config_data["include_email"]:
                if self.config_data["default_email"] == "Default Email":
                    
            if len(email_) > 0:
                email_ = "(" + email_ + ")"
            s = f"Timesheet for {name} {email} starting on {self.format_date(start_date)}\n\n"  
            
            if self.activeTimesheet:
                
            self.hasHeader = True
        return True
        
    def createEntry(self, tasks: list, hours, times: list): # TODO: Edit to use formatDate()
        if self.config_data is None:
            self.loadConfig()
            
        if not self.hasHeader:
            self.checkOrCreateHeader()
        
        entry = "" 
                    
        s = ""
        year = month = day = None
        if self.config_data["include_day_name"]:
            
            if self.config_data["entry_on_current_day"]:
                s = days[datetime.today().weekday()]
                year = datetime.today().year
                month = datetime.today().month
                day = datetime.today().day
            else:
                yesterday = datetime.now() - timedelta(days=1)
                s = days[yesterday.weekday()]
                year = yesterday.year
                month = yesterday.month
                day = yesterday.day
        
        date_str = ""
        
        if self.config_data["date_format"] == "MLA":
            date_str = f"{day} {months[month]} {year}"
        else:
            #As yet unimplemented
            raise Exception("Your config contains a date format that is not currentlty supported. Please change it and try again")
        
        if self.config_data["include_day_name"]:
            date_string += f" ({s}):"
        
        entry = date_str + "\n"
        
        for task in tasks:
            assert isinstance(task, str)
            entry += task + "\n"
        
        entry += "-------------------------------------------------------------------\n"
        entry += f"{hours} hours"
        
        if self.config_data["include_entry_hours"]:
            if not times:
                raise Exception("Your config is set up to include entry hours but none were given")
            entry += "("
            idx = 0
            for time_tuple in times:
                start_time = time_tuple[0]
                end_time = time_tuple[1]
                entry += f"{start_time} - {end_time}"
                if idx != len(times) - 1:
                    entry += ", "

                idx += 1
            entry += ")"
        
        entry += "\n\n"
    
    #def finalize(self): # Sum hours for timesheet (thus preparing it to be sent)
    
    #def send(self, email_target):

    

def main():
    filename = "tcup-config.txt"
    
    tcup = TCUP()
    
    tcup.loadConfig()
    
    config_data = loadConfig(filename):

    config.close()

    timesheet = open("tcup-timesheet.txt", "w")
        
    timesheet.close()

if __name__ == "__main__":
    main()



