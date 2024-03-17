from formula.models import *



class CategoryDummy():
    CATEGORIES = [
        (ENGINEERING := 'Engineering Project', Category.EVEHICLE),
        (DESIGN := 'Design', Category.GENERAL),
        (SOFTWARE := 'Software Development', Category.EVEHICLE),
        (BUSINESS := 'Business Operations', Category.OPERATION),
        (RESEARCH := 'Research and Development', Category.EVEHICLE),
        (TESTING := 'Testing', Category.EVEHICLE),
        (MARKETING := 'Marketing', Category.OPERATION),
        (FINANCE := 'Finance', Category.OPERATION),
        (EVENTS := 'Events', Category.OPERATION),
        (EDUCATION := 'Education', Category.GENERAL),
        (OUTREACH := 'Community Outreach', Category.OPERATION),
    ]


class TopicDummy():
    TOPICS = [
        (VEHICLE_DESIGN := 'Vehicle Design', CategoryDummy.DESIGN),
        (GRAPHIC_DESIGN := 'Graphic Design', CategoryDummy.DESIGN),
        (AERODYNAMICS := 'Aerodynamics', CategoryDummy.ENGINEERING),
        (CHASSIS_DESIGN := 'Chassis Design', CategoryDummy.ENGINEERING),
        (POWERTRAIN := 'Powertrain', CategoryDummy.ENGINEERING),
        (SUSPENSION := 'Suspension', CategoryDummy.ENGINEERING),
        (ELECTRONICS := 'Electronics', CategoryDummy.ENGINEERING),
        (MATERIALS := 'Materials', CategoryDummy.ENGINEERING),
        (TESTING_SIMULATION := 'Testing and Simulation', CategoryDummy.ENGINEERING),
        (SPONSORSHIP := 'Sponsorship', CategoryDummy.BUSINESS),
        (EVENT_MANAGEMENT := 'Event Management', CategoryDummy.BUSINESS),
        (MARKET_RESEARCH := 'Market Research', CategoryDummy.RESEARCH),
        (PRODUCT_DEVELOPMENT := 'Product Development', CategoryDummy.RESEARCH),
        (FINANCIAL_PLANNING := 'Financial Planning', CategoryDummy.FINANCE),
        (BUDGETING := 'Budgeting', CategoryDummy.FINANCE),
        (ADVERTISING := 'Advertising', CategoryDummy.MARKETING),
        (PUBLIC_RELATIONS := 'Public Relations', CategoryDummy.MARKETING),
        (SOFTWARE_ENGINEERING := 'Software Engineering', CategoryDummy.SOFTWARE),
        (DATA_ANALYSIS := 'Data Analysis', CategoryDummy.SOFTWARE),
        (COMMUNITY_OUTREACH := 'Community Outreach', CategoryDummy.OUTREACH),
        (EDUCATIONAL_PROGRAMS := 'Educational Programs', CategoryDummy.EDUCATION),
        (VOLUNTEER_MANAGEMENT := 'Volunteer Management', CategoryDummy.EDUCATION),
        (SALES := 'Sales', CategoryDummy.BUSINESS),
        (CUSTOMER_SERVICE := 'Customer Service', CategoryDummy.BUSINESS),
        (PROJECT_MANAGEMENT := 'Project Management', CategoryDummy.BUSINESS),
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
    USER_PROFILE = {
        UserDummy.BOBBYKEREN['username']: {
            'student_id': 2347773,
        },
        UserDummy.JEFFREYMULLOC['username']: {
            'student_id': 2748235,
        },
        UserDummy.ALICEWOND['username']: {
            'student_id': 2018551,
        },
        UserDummy.DANNYBOY['username']: {
            'student_id': 2345678,
        },
        UserDummy.SARAHJANE['username']: {
            'student_id': 2980477,
        },
        UserDummy.MICHAELSCOTT['username']: {
            'student_id': 2348778,
        }
    }
