from governance_platform import db
from datetime import datetime, date

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100))
    password = db.Column("password", db.String(100))

    #curr_time = db.Column("time", db.DateTime, default = today.strftime("%H:%M:%S"))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Project(db.Model):
    project_id = db.Column("project_id", db.Integer,
                           primary_key=True, autoincrement=True)
    project_name = db.Column("project_name", db.String(100))
    database_dialect = db.Column("database_dialect", db.String(100))
    file = db.Column("base_directory", db.String(100))
    curr_date = db.Column("date", db.DateTime, default=datetime.utcnow)
    audits = db.relationship('ProjectAudit', backref='proj', lazy=True)
    
    def __init__(self, pname, database_dialect, base_dir):
        #self.project_id = random.randint(0,1000)
        self.project_name = pname
        self.database_dialect = database_dialect
        self.base_dir = base_dir

class ProjectAudit(db.Model):
    auditid = db.Column("project_id", db.Integer,
                           primary_key=True, autoincrement=True)
    projid = db.Column(db.Integer, db.ForeignKey('project.project_id'),   
        nullable=False)    
    auditModuleName = db.Column("auditModuleName", db.String(20))
    auditDocumentName = db.Column("auditDocumentName", db.String(20))
    operation = db.Column("operation", db.String(10))
    userName = db.Column("userName", db.String(30))
    timestamp = db.Column("timestamp", db.String(40))


# class ProjectMetrics(db.Model):
#     peformance_id = db.Column("project_id", db.Integer,
#                            primary_key=True, autoincrement=True)
#     projid = db.Column(db.Integer, db.ForeignKey('project.project_id'),   
#         nullable=False)    
#     maxiumumMemory = db.Column("maxiumumMemory", db.String(100))
#     freeMemory = db.Column("freeMemory", db.String(100))
#     availableProcessors = db.Column("availableProcessors", db.String(100))
#     totalMemory = db.Column("totalMemory", db.String(100))



    # def __init__(self, project_id, auditModuleName, auditDocumentName,operation,userName,timestamp):
    #     #self.project_id = random.randint(0,1000)
    #     self.projid = project_id    
    #     self.auditModuleName =auditModuleName
    #     self.auditDocumentName = auditDocumentName
    #     self.operation = operation
    #     self.userName = userName
    #     self.timestamp = timestamp

