from .base import ObservableModel
from .database import Database
import bcrypt

class Auth(ObservableModel):
    def __init__(self,model):
        super().__init__()
        self.is_logged_in = False
        self.current_user = None
        self.model = model
        self.latestFinancialInfo = None
        self.currentProd= None
        self.selectedSupp = None

    def login(self, user):
        
        self.current_user = user
        self.model.database.initializeFinancial_details(self.current_user['UserID'])
        finance = self.model.database.get_financialDetails(self.current_user["UserID"])
        self.latestFinancialInfo = finance
        self.is_logged_in = True
        self.trigger_event("auth_changed")

    def logout(self):
        self.current_user = None
        self.financialInfo = None
        self.is_logged_in = False
        self.trigger_event("auth_changed")

    def authenticate_user(self, data):
        email = data["email"]
        password = data["password"]
        self.user_info = self.model.database.getUser_fromEmail(email)
        
        
        if self.user_info:
            real_password_hash = self.user_info["PasswordHash"]
            input_password = password.encode('utf-8')

            # Check if the input password matches the stored hash
            if bcrypt.checkpw(input_password, real_password_hash):
               
                return True
            else:
                return False
        else:
            return False
        
    def updateDashboard(self):
        self.latestFinancialInfo = self.model.database.get_financialDetails(self.current_user["UserID"])
        self.trigger_event("dashboardChanged")

    def updateProductName(self,productId):
        name = self.model.database.fetchProductName(productId)
        self.currentProd= {"name":name,
                           "id":productId}
        self.trigger_event("currentProduct")

    def order_created(self):
        self.trigger_event("order_created")
    

    def selectSupplier(self,email):
               
        print(f"selectSupplier called with email: {email}")
    
        self.selectedSupp = self.model.database.getUser_fromEmail(email)
        self.trigger_event("selectSupplier")

    

# def authenticate_user(self, data):
#     email = data["email"]
#     password = data["password"]
#     user_info = self.model.database.getUser_fromEmail(email)
    
#     if user_info:
#         real_password_hash = user_info["PasswordHash"]
#         input_password = password.encode('utf-8')

#         # Check if the input password matches the stored hash
#         if bcrypt.checkpw(input_password, real_password_hash):
#             self.user_info = user_info  # Set user_info upon successful login
#             return True
#         else:
#             return False
#     else:
#         return False


        
     
