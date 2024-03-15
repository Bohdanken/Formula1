from formula.models import Category

class CategoryDummy():
    ROOT_PARENT = Category

    CATEGORIES = [
        ENGINEERING := {
            'name': 'Engineering Project',
            'parent': ROOT_PARENT.EVEHICLE
        },
        DESIGN := {
            'name': 'Design',
            'parent': ROOT_PARENT.GENERAL
        },
        SOFTWARE := {
            'name': 'Software Development',
            'parent': ROOT_PARENT.EVEHICLE
        },
        BUSINESS := {
            'name': 'Business Operations',
            'parent': ROOT_PARENT.OPERATION
        },
        RESEARCH := {
            'name': 'Research and Development',
            'parent': ROOT_PARENT.EVEHICLE
        },
        TESTING := {
            'name': 'Testing',
            'parent': ROOT_PARENT.EVEHICLE
        },
        MARKETING := {
            'name': 'Marketing',
            'parent': ROOT_PARENT.OPERATION
        },
        FINANCE := {
            'name': 'Finance',
            'parent': ROOT_PARENT.OPERATION
        },
        EVENTS := {
            'name': 'Events',
            'parent': ROOT_PARENT.OPERATION
        },
        EDUCATION := {
            'name': 'Education',
            'parent': ROOT_PARENT.GENERAL
        },
        OUTREACH := {
            'name': 'Community Outreach',
            'parent': ROOT_PARENT.OPERATION
        },
    ]

class TopicDummy():
    CAT_CALL_KEY = 'name'

    TOPICS = [
        VEHICLE_DESIGN := {
            'name': 'Vehicle Design',
            'category': CategoryDummy.DESIGN[CAT_CALL_KEY]
        },
        GRAPHIC_DESIGN := {
            'name': 'Graphic Design',
            'category': CategoryDummy.DESIGN[CAT_CALL_KEY]
        },
        AERODYNAMICS := {
            'name': 'Aerodynamics',
            'category': CategoryDummy.ENGINEERING[CAT_CALL_KEY]
        },
        VEHICLE_DESIGN := {
            'name': 'Vehicle Design',
            'category': CategoryDummy.DESIGN[CAT_CALL_KEY]
        },
        GRAPHIC_DESIGN := {
            'name': 'Graphic Design',
            'category': CategoryDummy.DESIGN[CAT_CALL_KEY]
        },
        AERODYNAMICS := {
            'name': 'Aerodynamics',
            'category': CategoryDummy.ENGINEERING[CAT_CALL_KEY]
        },
        CHASSIS_DESIGN := {
            'name': 'Chassis Design',
            'category': CategoryDummy.ENGINEERING[CAT_CALL_KEY]
        },
        POWERTRAIN := {
            'name': 'Powertrain',
            'category': CategoryDummy.ENGINEERING[CAT_CALL_KEY]
        },
        SUSPENSION := {
            'name': 'Suspension',
            'category': CategoryDummy.ENGINEERING[CAT_CALL_KEY]
        },
        ELECTRONICS := {
            'name': 'Electronics',
            'category': CategoryDummy.ENGINEERING[CAT_CALL_KEY]
        },
        MATERIALS := {
            'name': 'Materials',
            'category': CategoryDummy.ENGINEERING[CAT_CALL_KEY]
        },
        TESTING_SIMULATION := {
            'name': 'Testing and Simulation',
            'category': CategoryDummy.ENGINEERING[CAT_CALL_KEY]
        },
        SPONSORSHIP := {
            'name': 'Sponsorship',
            'category': CategoryDummy.BUSINESS[CAT_CALL_KEY]
        },
        EVENT_MANAGEMENT := {
            'name': 'Event Management',
            'category': CategoryDummy.BUSINESS[CAT_CALL_KEY]
        },
        MARKET_RESEARCH := {
            'name': 'Market Research',
            'category': CategoryDummy.RESEARCH[CAT_CALL_KEY]
        },
        PRODUCT_DEVELOPMENT := {
            'name': 'Product Development',
            'category': CategoryDummy.RESEARCH[CAT_CALL_KEY]
        },
        FINANCIAL_PLANNING := {
            'name': 'Financial Planning',
            'category': CategoryDummy.FINANCE[CAT_CALL_KEY]
        },
        BUDGETING := {
            'name': 'Budgeting',
            'category': CategoryDummy.FINANCE[CAT_CALL_KEY]
        },
        ADVERTISING := {
            'name': 'Advertising',
            'category': CategoryDummy.MARKETING[CAT_CALL_KEY]
        },
        PUBLIC_RELATIONS := {
            'name': 'Public Relations',
            'category': CategoryDummy.MARKETING[CAT_CALL_KEY]
        },
        SOFTWARE_ENGINEERING := {
            'name': 'Software Engineering',
            'category': CategoryDummy.SOFTWARE[CAT_CALL_KEY]
        },
        DATA_ANALYSIS := {
            'name': 'Data Analysis',
            'category': CategoryDummy.SOFTWARE[CAT_CALL_KEY]
        },
        COMMUNITY_OUTREACH := {
            'name': 'Community Outreach',
            'category': CategoryDummy.OUTREACH[CAT_CALL_KEY]
        },
        EDUCATIONAL_PROGRAMS := {
            'name': 'Educational Programs',
            'category': CategoryDummy.EDUCATION[CAT_CALL_KEY]
        },
        VOLUNTEER_MANAGEMENT := {
            'name': 'Volunteer Management',
            'category': CategoryDummy.EDUCATION[CAT_CALL_KEY]
        },
        SALES := {
            'name': 'Sales',
            'category': CategoryDummy.BUSINESS[CAT_CALL_KEY]
        },
        CUSTOMER_SERVICE := {
            'name': 'Customer Service',
            'category': CategoryDummy.BUSINESS[CAT_CALL_KEY]
        },
        PROJECT_MANAGEMENT := {
            'name': 'Project Management',
            'category': CategoryDummy.BUSINESS[CAT_CALL_KEY]
        },
    ]

class UserDummy():
    USERS = [
        JEFFREYMULLOC := {
            'username': 'jeffreymulloc',
            'email': 'jeffr4y@gmail.com',
            'first_name': 'Jeffrey',
            'last_name': 'Mulloc',
        },
        BOBBYKEREN := {
            'username': 'bobbykeren',
            'email': 'bob@ed.uk',
            'first_name': 'Bob',
            'last_name': 'Keren',
        },
        ALICEWOND := {
            'username': 'alicewond',
            'email': 'alice@gmail.com',
            'first_name': 'Alice',
            'last_name': 'Wond',
        },
        DANNYBOY := {
            'username': 'dannyboy',
            'email': 'danny@web.com',
            'first_name': 'Danny',
            'last_name': 'Boy',
        },
        SARAHJANE := {
            'username': 'sarahjane',
            'email': 'sarah@gmail.com',
            'first_name': 'Sarah',
            'last_name': 'Jane',
        },
        MICHAELSCOTT := {
            'username': 'michaelscott',
            'email': 'michael@dundermifflin.com',
            'first_name': 'Michael',
            'last_name': 'Scott',
        }
    ]
    
class UserProfileDummy():
    USR_CALL_KEY = 'username'
    
    USER_PROFILES = [
        P_BOBBYKEREN := {
            'username': UserDummy.BOBBYKEREN[USR_CALL_KEY],
            'student_id': 2347773
        },
        P_JEFFREYMULLOC := {
            'username': UserDummy.JEFFREYMULLOC[USR_CALL_KEY],
            'student_id': 2748235
        },
        P_ALICEWOND := {
            'username': UserDummy.ALICEWOND[USR_CALL_KEY],
            'student_id': 2018551
        },
        P_DANNYBOY := {
            'username': UserDummy.DANNYBOY[USR_CALL_KEY],
            'student_id': 2345678
        },
        P_SARAHJANE := {
            'username': UserDummy.SARAHJANE[USR_CALL_KEY],
            'student_id': 2980477
        },
        P_MICHAELSCOTT := {
            'username': UserDummy.MICHAELSCOTT[USR_CALL_KEY],
            'student_id': 2348778
        },
    ]

class TeamDummy():
    TEAMS = [
        VENCERA := {
            'name':'Vencera Racing',
        },
        ALUSIS := {
            'name':'Alusis Motor Team'
        },
        SPEEDFORCE := {
            'name': 'Speedforce Racing',
        },
        TITANMOTORS := {
            'name': 'Titan Motorsport',
        },
        CRIMSONRACING := {
            'name': 'Crimson Racing',
        },
        BLAZESPEED := {
            'name': 'Blaze Speedsters',
        },
        THUNDERBOLT := {
            'name': 'Thunderbolt Racing',
        },
        NOVAVELOCITY := {
            'name': 'Nova Velocity Racing',
        },
        AURORARACING := {
            'name': 'Aurora Racing',
        },
        DRAGONFURY := {
            'name': 'Dragon Fury Racing',
        },
    ]

class PostDummy():
    GENERIC_CONTENT = 'This is a generic content. Please delete before deployment.'
    TOP_CALL_KEY = 'name'
    USR_CALL_KEY = 'username'

    POSTS = [
        HELP_ERROR := {
            'title':'Help! Error in Git Push',
            'topic': TopicDummy.DATA_ANALYSIS[TOP_CALL_KEY],
            'author': UserDummy.JEFFREYMULLOC[USR_CALL_KEY],
        },
        CONTEST_WIN := {
            'title':'Vencera Wins F1inSchool',
            'topic':TopicDummy.EDUCATIONAL_PROGRAMS[TOP_CALL_KEY],
            'author':UserDummy.ALICEWOND[USR_CALL_KEY],
        },
        TEAM_RECRUITMENT := {
            'title': 'Join Our Racing Team!',
            'topic': TopicDummy.COMMUNITY_OUTREACH[TOP_CALL_KEY],
            'author': UserDummy.MICHAELSCOTT[USR_CALL_KEY],
        },
        DESIGN_CHALLENGE := {
            'title': 'Design Challenge Announcement',
            'topic': TopicDummy.VEHICLE_DESIGN[TOP_CALL_KEY],
            'author': UserDummy.JEFFREYMULLOC[USR_CALL_KEY],
        },
        NEW_SOFTWARE_RELEASE := {
            'title': 'Announcing Our New Software Release',
            'topic': TopicDummy.SOFTWARE_ENGINEERING[TOP_CALL_KEY],
            'author': UserDummy.BOBBYKEREN[USR_CALL_KEY],
        },
        PROMOTION_EVENT := {
            'title': 'Promotion Event Tomorrow!',
            'topic': TopicDummy.EVENT_MANAGEMENT[TOP_CALL_KEY],
            'author': UserDummy.SARAHJANE[USR_CALL_KEY],
        },
        DATA_ANALYSIS_WORKSHOP := {
            'title': 'Data Analysis Workshop Registration Open',
            'topic': TopicDummy.EDUCATIONAL_PROGRAMS[TOP_CALL_KEY],
            'author': UserDummy.JEFFREYMULLOC[USR_CALL_KEY],
        },
        SOFTWARE_BUG_FIX := {
            'title': 'Critical Bug Fix Released',
            'topic': TopicDummy.SOFTWARE_ENGINEERING[TOP_CALL_KEY],
            'author': UserDummy.JEFFREYMULLOC[USR_CALL_KEY],
        },
        MARKET_RESEARCH_SURVEY := {
            'title': 'Participate in Our Market Research Survey',
            'topic': TopicDummy.MARKET_RESEARCH[TOP_CALL_KEY],
            'author': UserDummy.SARAHJANE[USR_CALL_KEY],
        },
        DESIGN_COMPETITION := {
            'title': 'Design Competition Announcement',
            'topic': TopicDummy.GRAPHIC_DESIGN[TOP_CALL_KEY],
            'author': UserDummy.MICHAELSCOTT[USR_CALL_KEY],
        },
        NEW_PRODUCT_LAUNCH := {
            'title': 'Exciting News: New Product Launch!',
            'topic': TopicDummy.PRODUCT_DEVELOPMENT[TOP_CALL_KEY],
            'author': UserDummy.ALICEWOND[USR_CALL_KEY],
        },
        FINANCIAL_REPORT := {
            'title': 'Quarterly Financial Report Released',
            'topic': TopicDummy.FINANCIAL_PLANNING[TOP_CALL_KEY],
            'author': UserDummy.MICHAELSCOTT[USR_CALL_KEY],
        }
    ]

class TeamMemberDummy():
    TEM_CALL_KEY = 'name'
    USR_CALL_KEY = 'username'

    TEAM_MEMBERS = [
        BOBBYKEREN_VENCERA := {
            'user': UserDummy.BOBBYKEREN[USR_CALL_KEY],
            'team': TeamDummy.VENCERA[TEM_CALL_KEY],
        },
        MICHAELSCOTT_ALUSIS := {
            'user': UserDummy.MICHAELSCOTT[USR_CALL_KEY],
            'team': TeamDummy.ALUSIS[TEM_CALL_KEY],
        },
        ALICEWOND_SPEEDFORCE := {
            'user': UserDummy.ALICEWOND[USR_CALL_KEY],
            'team': TeamDummy.SPEEDFORCE[TEM_CALL_KEY],
        },
        DANNYBOY_BLAZESPEED := {
            'user': UserDummy.DANNYBOY[USR_CALL_KEY],
            'team': TeamDummy.BLAZESPEED[TEM_CALL_KEY],
        },
        ALICEWOND_THUNDERBOLT := {
            'user': UserDummy.ALICEWOND[USR_CALL_KEY],
            'team': TeamDummy.THUNDERBOLT[TEM_CALL_KEY],
        },
    ]
